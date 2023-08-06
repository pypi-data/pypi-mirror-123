# -*- coding: utf-8 -*-
import string
from datetime import datetime, time

from numpy import long
from pymssql import InternalError
from sqlalchemy import Time, create_engine, exc, Table, MetaData, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, mapper

from cap.cap_config import CAPStorageConfig

metadata = MetaData()
message_published_table = Table("Published", metadata,
                                Column("Id", Integer, primary_key=True, autoincrement=False),
                                Column("Version", String, default="V1"),
                                Column("Name", String),
                                Column("Content", String),
                                Column("Retries", Integer, default=0),
                                Column("Added", DateTime),
                                Column("ExpiresAt", DateTime),
                                Column("StatusName", String),
                                schema="[cap]")


class MessagePublished:
    """
    消息发布表实体
    """

    def __init__(self, id, name, content, added, expires_at, status_name):
        self.Id = id
        self.Name = name
        self.Content = content
        self.Added = added
        self.ExpiresAt = expires_at
        self.StatusName = status_name


class CAPStorageBase(object):
    """
    CAP消息存储基类
    """

    def store_message(self, routing_key, message, status):
        pass


class CAPStorage(CAPStorageBase):
    """
    CAP消息存储
    """

    def __init__(self, config:CAPStorageConfig):
        self.config = config

        # 编码特殊字符
        pwd = config.password.replace("@", "%40")
        self.engine = create_engine(
            'mssql+pymssql://%s:%s@%s/%s' % (config.user, pwd, config.server, config.database))

        # 通过mapper函数进行映射关联
        mapper(MessagePublished, message_published_table)

    def store_message(self, message_id: long, routing_key: string, message: string, status: string):
        """
        存储消息
        """

        try:
            session_cls = sessionmaker(bind=self.engine,autoflush=True)

            with session_cls() as session:

                message_published = MessagePublished(message_id, routing_key, message,
                                                     str(datetime.utcnow()), str(datetime.utcnow()),
                                                     status)
                session.add(message_published)

                # 提交即保存到数据库:
                session.commit()

        except (exc.InternalError, InternalError):  # 如果创建连接失败，一般意味着数据库本身不可达。此例中是因为目标数据库不存在
            print('连接数据库连接失败')
            raise
