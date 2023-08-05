# @Time    : 2021/9/30 18:17
# @Author  : wz
# File     : dynamic_scheduler.py

import datetime
import os
import threading
import time
from loguru import logger

from PoolDB.PoolDB import PoolDB
from apscheduler.events import EVENT_JOB_ADDED, EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.util import undefined
from scheduler_utils import SchedulerUtils, SchedulerConfig


class Listener(SchedulerUtils):
    scheduler_ = {}

    def __init__(self, scheduler, config_class):
        super().__init__(scheduler, config_class)

    def add_job_listener(self, Event):
        job_id = Event.job_id
        self.is_db_expression_equals_cron_expression(job_id)

    def execute_job_listener(self, Event):
        job_id = Event.job_id
        if not Event.exception:
            self.update_job(job_id)
            if self.config.IS_SAVE_JOB_RESULT:
                self.save_job_result(Event)

    def update_job(self, job_id):
        job = self.scheduler.get_job(job_id)
        if not self.is_db_expression_equals_cron_expression(job_id):
            db_expression = self.db_expression(job_id)
            if self.scheduler.get_job(job_id):
                self.scheduler.get_job(job_id).remove()
            self.scheduler.add_job(id=job_id, func=job.func, args=job.args, kwargs=job.kwargs,
                                   trigger=self.config.DEFAULT_TRIGGER,
                                   replace_existing=True, **self.translate_expression(db_expression))

    def save_job_result(self, Event):
        job_result = Event.retval  # job执行结果
        job_id = Event.job_id
        job_result = str(job_result) if job_result is not None else 'null'
        if job_result is not None:
            self.db_pool.execute(f'update {self.config.SCHEDULER_SCHEMA}.{self.config.SCHEDULER_TABLE} '
                                 f'set result = \'{job_result}\'  where id = \'{job_id}\'')
            logger.success("p-{}, t-{}: 存储定时任务结果成功， job_id: {}", os.getpid(), threading.current_thread().name, job_id)


class DynamicSchedulerProxy:

    def __init__(self, config_class):
        self.config = config_class()
        self.scheduler = BlockingScheduler(timezone=self.config.TIME_ZONE, jobstores=self.config.JOB_STORES,
                                           executors=self.config.EXECUTORS, job_defaults=self.config.JOB_DEFAULTS)
        self.listener = Listener(self.scheduler, config_class)
        self.scheduler.add_listener(self.listener.add_job_listener, EVENT_JOB_ADDED)
        self.db_pool = PoolDB(self.config.DEFAULT_DB_URL)

    def add_result_listener(self):
        if self.config.IS_DYNAMIC_UPDATE_CRON:  # 开启会耗时 降低性能
            self.scheduler.add_listener(self.listener.execute_job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        return self

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None,
                misfire_grace_time=undefined, coalesce=undefined, max_instances=undefined,
                next_run_time=undefined, jobstore='default', executor='default',
                replace_existing=False, **trigger_args):
        self.scheduler.add_job(func, trigger, args, kwargs, id, name,
                               misfire_grace_time, coalesce, max_instances,
                               next_run_time, jobstore, executor,
                               replace_existing, **trigger_args)

    def add_job_with_default(self, func, cron_str=None,trigger=None, args=None, kwargs=None, id=None, name=None,
                             misfire_grace_time=undefined, coalesce=True, max_instances=undefined,
                             next_run_time=undefined, jobstore='default', executor='default',
                             replace_existing=True, **trigger_args):
        """
        默认只需传入 func、id、cron表达式
        增加任务时设定一些默认选项，避免重复code, trigger 默认为 cron
        """
        trigger_ = self.config.DEFAULT_TRIGGER if trigger is None else trigger
        trigger_args_ = trigger_args
        if cron_str:
            trigger_args_.update(self.listener.translate_expression(cron_str))
        self.add_job(func, trigger_, args, kwargs, id, name,
                     misfire_grace_time, coalesce, max_instances,
                     next_run_time, jobstore, executor,
                     replace_existing, **trigger_args_)

    def start(self, *args, **kwargs):
        existed_jobs = self.scheduler.get_jobs(jobstore='default')
        if existed_jobs:
            self.scheduler.start(*args, **kwargs)

    def clear_history(self):
        self.db_pool.execute(f'delete from {self.config.SCHEDULER_SCHEMA}.{self.config.SCHEDULER_TABLE}')

    def set_cron_task(self, func):
        """
        1. 给默认 cron表中定时任务 进行启动
        2. 设置 不同的func 的定时任务，通过job_id关联，job_id可设置为func_name
        # 依赖self.insert_cron_table 方法，先执行完给每个方法设定初始值;
        # 现在不依赖了，添加不存在的任务会自动存入cron中
        """
        cron_task = self.db_pool[f'select * from {self.config_class.SCHEMA_TABLE} where state = 1']
        if not cron_task.empty:
            for index, row in cron_task.iterrows():
                self.add_job_with_default(func, self.listener.translate_expression(row['expression']), id=row['job_id'])
        self.add_result_listener()
        # self.start()

    def insert_cron_table(self, func_list, expression_list):
        """批量传入方法列表、表达式列表，后期可改为dict"""
        value_str = [f"('{func.__name__}', '{express}')" for func, express in zip(func_list, expression_list)]
        value_str = ", ".join(value_str)
        insert_sql = f"insert into {self.config.SCHEMA_TABLE} (job_id, expression) values {value_str}"
        self.db_pool.insert(insert_sql)
        logger.success("写入cron表成功")


class StaticSchedulerProxy(DynamicSchedulerProxy):
    def __init__(self, config_class):
        super(StaticSchedulerProxy, self).__init__(config_class)
        self.scheduler.remove_listener(self.listener.add_job_listener)
        self.listener = Listener(self.scheduler, self.config)
        self.listener.IS_DYNAMIC_UPDATE_CRON = False
        self.scheduler.add_listener(self.listener.add_job_listener, EVENT_JOB_ADDED)


if __name__ == '__main__':
    def task():
        # print(datetime.datetime.now())
        # time.sleep(10)
        print('start time: ', datetime.datetime.now(), os.getpid(), threading.current_thread().name)
        return datetime.datetime.now()

    class Config(SchedulerConfig):
        DEFAULT_DB_URL = 'postgresql+psycopg2://postgres:123456@172.16.1.54:5432/postgres?utf-8'
        SCHEDULER_SCHEMA = 'public'

    s = DynamicSchedulerProxy(config_class=Config)
    s.clear_history()
    s.add_job_with_default(func=task, cron_str='* * */5', id='task')
    s.add_result_listener()
    s.start()
