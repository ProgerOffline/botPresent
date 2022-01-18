#-*- coding: utf-8 -*-

from gino import Gino
from sqlalchemy import sql
from sqlalchemy import (Column, Integer, BigInteger, String,
                       Sequence, Boolean, Float, DateTime)


db = Gino()


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    username = Column(String(length=50))
    phone = Column(BigInteger)
    ballance = Column(Float)
    buyed = Column(Boolean)
    invest_amount = Column(Float)
    wallet = Column(String)
    referer = Column(Integer)
    ref_level = Column(Integer)
    reg_date = Column(DateTime)
    query: sql.Select


class Support(db.Model):
    __tablename__ = "supports"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    support_id = Column(BigInteger)
    quest_type = Column(String(length=50))
    quest_full = Column(String(length=500))
    msg_id = Column(BigInteger)
    query: sql.Select


class Referers(db.Model):
    __tablename__ = "referers"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    referer_id = Column(BigInteger)
    query: sql.Select


class ReferalProgramLevels(db.Model):
    __tablename__ = "referalprogramlevels"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    level = Column(Integer)
    precent = Column(Integer)
    query: sql.Select


class InvestProduct(db.Model):
    __tablename__ = "investproduct"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    precent = Column(Integer)


class UsersPayments(db.Model):
    __tablename__ = "userspayments"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_db_id = Column(BigInteger)
    phone = Column(BigInteger)
    date = Column(DateTime)
    wallet = Column(String)
    bank = Column(String)
    amount = Column(BigInteger)
    status = Column(String)
    client_status = Column(String)


class Settings(db.Model):
    __tablename__ = "settings"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    precent = Column(Float)
    cber_bank = Column(BigInteger)
    tinkoff_bank = Column(BigInteger)
    fio = Column(String)
    wallet_pm = Column(String)
    pm_account = Column(BigInteger)
    pm_passwd = Column(String)


class OutsRecords(db.Model):
    __tablename__ = "outsrecords"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_db_id = Column(BigInteger)
    phone = Column(BigInteger)
    date = Column(DateTime)
    wallet = Column(String)
    amount = Column(Float)
    error = Column(String)
