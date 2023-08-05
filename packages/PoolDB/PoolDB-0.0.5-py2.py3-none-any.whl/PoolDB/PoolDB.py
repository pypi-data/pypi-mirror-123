# @Time    : 2021/4/30 11:07
# @Author  : wz
# File     : PoolDB.py
# Software : EngiPower.com
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.pool import QueuePool
import gevent
from loguru import logger

MANAGER_ENGINE = {}


class PoolDB:

    def __init__(self, db_url, pool_size=10, **kwargs):
        """
        @Param db_url:传入数据库连接url
        """
        self.db_url = db_url
        self.pool_size = pool_size
        self.engine = self.get_engine(pool_size, **kwargs)

    def get_engine(self, pool_size, **kwargs):
        if self.db_url not in MANAGER_ENGINE:
            engine = create_engine(self.db_url, poolclass=QueuePool, encoding="utf-8",
                                   pool_size=pool_size, pool_recycle=300, max_overflow=5,
                                   **kwargs)
            MANAGER_ENGINE[self.db_url] = engine
        return MANAGER_ENGINE[self.db_url]

    def connect(self) -> Connection:
        conn = self.engine.connect()
        return conn

    def multi_data(self, sql, **kwargs):
        """多条数据并发获取"""
        gevent_num = len(sql) if isinstance(sql, list) else 1
        if gevent_num > self.pool_size:
            w_msg = f"当前数据库连接池数最大并发：{self.pool_size}, 不建议同时操作长度为{len(sql)}的sql列表"
            logger.warning(w_msg)
        # gevent_num = gevent_num if gevent_num < self.pool_size else self.pool_size
        conn_dict = {}
        g_list = []
        for i in range(gevent_num):
            conn_dict[i] = self.connect()
        for i in range(gevent_num):
            g = gevent.spawn(self.get_data_from_sql, sql=sql[i], conn=conn_dict[i], **kwargs)
            g_list.append(g)
        gevent.joinall(g_list)
        for k, v in conn_dict.items():
            v.close()
        return [g.value for g in g_list]

    def close(self, conn):
        try:
            conn.close()  # 使其返回池
        except:
            pass

    def dispose(self):
        try:
            self.engine.dispose()
        except Exception as e:
            print(e)
            pass

    def __enter__(self):
        self.conn = self.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close(self.conn)

    def get_data_from_sql(self, sql, conn, **kwargs):
        """若是多次操作获取，可以晚点关闭连接"""
        data = []
        try:
            if isinstance(sql, list):
                for s in sql:
                    data.append(pd.read_sql(text(s), conn, **kwargs))
            else:
                data.append(pd.read_sql(text(sql), conn, **kwargs))
        finally:
            return pd.concat(data, ignore_index=True) if data else pd.DataFrame()

    def __getitem__(self, item):
        """单次获取，自动开关"""
        with self as conn:
            res = self.get_data_from_sql(item, conn)
        return res

    def execute(self, sql):
        self.insert(sql)

    def insert(self, sql):
        engine = create_engine(self.db_url, encoding="utf-8")
        conn = engine.connect()
        try:
            conn.execute(sql)
        except Exception as e:
            logger.error("sql 执行失败， sql: {}, error: {}", sql, e)
        finally:
            conn.close()
            engine.dispose()
