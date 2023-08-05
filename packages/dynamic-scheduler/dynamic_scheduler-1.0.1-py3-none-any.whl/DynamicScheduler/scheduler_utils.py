# @Time    : 2021/9/30 18:17
# @Author  : wz
# File     : scheduler_utils.py
# Software : EngiPower.com
import pickle
import multiprocessing
import threading

from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.util import maybe_ref
from sqlalchemy import (
    create_engine, Table, Column, MetaData, Unicode, Float, LargeBinary, String)

from PoolDB import PoolDB

cpu_core_num = multiprocessing.cpu_count()
# scheduler_table = 'apscheduler_jobs'
# scheduler_schema = 'public'


class SQLAlchemyJobStoreWithResult(SQLAlchemyJobStore):
    def __init__(self, url=None, engine=None, tablename=None, metadata=None,
                 pickle_protocol=pickle.HIGHEST_PROTOCOL, tableschema=None, engine_options=None):
        super(SQLAlchemyJobStoreWithResult, self).__init__(url, engine, tablename, metadata, pickle_protocol,
                                                           tableschema, engine_options)
        self.pickle_protocol = pickle_protocol
        metadata = maybe_ref(metadata) or MetaData()
        if engine:
            self.engine = maybe_ref(engine)
        elif url:
            self.engine = create_engine(url, **(engine_options or {}))
        else:
            raise ValueError('Need either "engine" or "url" defined')
        self.jobs_t = Table(
            tablename, metadata,
            Column('id', Unicode(191, _warn_on_bytestring=False), primary_key=True),
            Column('next_run_time', Float(25), index=True),
            Column('job_state', LargeBinary, nullable=False),
            Column('result', String(255), nullable=True),
            schema=tableschema
        )


class SchedulerConfig:
    DEFAULT_DB_URL = 'to be rewrite'
    TIME_ZONE = 'Asia/Shanghai'
    IS_SAVE_JOB_RESULT = True
    IS_DYNAMIC = IS_DYNAMIC_UPDATE_CRON = True
    SCHEDULER_SCHEMA = 'public'
    SCHEDULER_TABLE = 'apscheduler_jobs'
    DEFAULT_TRIGGER = 'cron'
    CRON_TABLE = 'cron'
    SCHEMA_TABLE = ".".join([SCHEDULER_SCHEMA, CRON_TABLE])
    THREAD_POOL_NUM = 20
    PROCESS_POOL_NUM = cpu_core_num
    EXECUTORS = {
        'default': ThreadPoolExecutor(THREAD_POOL_NUM),
        'process': ProcessPoolExecutor(PROCESS_POOL_NUM)
    }
    JOB_DEFAULTS = {
        'coalesce': True,
        'max_instances': 3
    }

    def __init__(self):
        self.JOB_STORES = {
            'default': SQLAlchemyJobStoreWithResult(url=self.DEFAULT_DB_URL,
                                                    tableschema=self.SCHEDULER_SCHEMA,
                                                    tablename=self.SCHEDULER_TABLE)
        }


class SchedulerUtils:

    def __init__(self, scheduler, config_class):
        self.config = config_class()
        self.scheduler = scheduler
        self.db_pool = PoolDB.PoolDB(self.config.DEFAULT_DB_URL)
        self._atomic_action = threading.RLock()

    def is_db_expression_equals_cron_expression(self, job_id):
        with self._atomic_action:
            is_equal = True
            db_expression = self.db_expression(job_id)
            expression = self.cron_expression(job_id)
            if bool(db_expression):
                if db_expression != expression:
                    # self.db_pool.execute(
                    #     f'update {self.SCHEMA_TABLE} set expression = \'{expression}\' where job_id = \'{job_id}\'')
                    is_equal = False
            else:
                self.db_pool.execute(f"insert into {self.config.SCHEMA_TABLE} values(\'{job_id}\', '{expression}')")
            return is_equal

    def cron_expression(self, job_id, cron_dimension=3):
        """目前只处理 时 分 秒 ，三个维度的cron表达式"""
        with self._atomic_action:
            job = self.scheduler.get_job(job_id)
            expression = " ".join([str(i) for i in job.trigger.fields[-cron_dimension:]])
            return expression

    @staticmethod
    def translate_expression(expression):
        """目前只处理 时 分 秒 ，三个维度的cron表达式"""
        expression_list = expression.split(' ')
        cron = {'hour': expression_list[0], 'minute': expression_list[1], 'second': expression_list[2]}
        return cron

    def db_expression(self, job_id):
        with self._atomic_action:
            job_id_df = self.db_pool[f'select * from {self.config.SCHEMA_TABLE} where job_id = \'{job_id}\'']
            if not job_id_df.empty:
                expression = job_id_df.to_dict('records')[0].get('expression', '')
            else:
                expression = ''
            return expression
