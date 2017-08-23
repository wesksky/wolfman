from django.db import models

# from sqlalchemy import Column, String, Integer, create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# 该类用于 sqlalchemy orm 映射
# 目前不使用orm方式实现数据库

# engine = create_engine("mysql+pymysql://root:911220@104.128.91.88/wolfman",
#                                     encoding='utf-8', echo=True)
# base = declarative_base()

# class User(base):
#     __tablename__ = 'user'  # 表名
#     id = Column(String(128), primary_key=True)
#     nickname = Column(String(128))
#     password = Column(String(64))
#     sex = Column(Integer)
#     avatar = Column(String(512))
#     liveness = Column(Integer)
#     phone = Column(String(32))
#     state = Column(Integer)

# base.metadata.create_all(engine)

# Create your models here.
# class UserInfo(models.Model):
#     nickname = models.CharField(max_length=30)
#     sex = models.IntegerField()
#     avatar = models.CharField(max_length=30)
#     liveness = models.IntegerField()
#     phone = models.CharField(max_length=30)
#     state = models.IntegerField()
