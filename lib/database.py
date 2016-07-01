# !/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.types import BIGINT
# from sqlalchemy.types import TIMESTAMP
from sqlalchemy.types import Date
from sqlalchemy.types import DateTime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from lib.config import Config

Base = declarative_base()


class Malicious_dn_records(Base):
    """Record malicious domain"""
    __tablename__ = 'Malicious_DN'

    idx = Column(Integer, primary_key=True)
    dn = Column(String(255), unique=True)
    port = Column(Integer, nullable=True)
    date = Column(Date)
    source = Column(String(15))
    note = Column(String(255), nullable=True)

    def __init__(self, data):
        self.idx = data.get('idx')
        self.dn = data.get('dn')
        self.port = data.get('port')
        self.date = data.get('date')
        self.source = data.get('source')
        self.note = data.get('note')


class Malicious_ip_records(Base):
    """Record malicious ip"""
    __tablename__ = 'Malicious_IP'

    idx = Column(Integer, primary_key=True)
    ip = Column(String(50), unique=True)
    port = Column(Integer, nullable=True)
    date = Column(Date)
    source = Column(String(50))
    note = Column(String(255), nullable=True)

    def __init__(self, data):
        self.idx = data.get('idx')
        self.ip = data.get('ip')
        self.port = data.get('port')
        self.date = data.get('date')
        self.source = data.get('source')
        self.note = data.get('note')


class Pdns_records(Base):
    __tablename__ = 'pdns'

    id = Column(BIGINT, primary_key=True)
    query = Column(String(255))
    maptype = Column(String(10))
    rr = Column(String(10))
    answer = Column(String(255))
    ttl = Column(Integer)
    count = Column(BIGINT)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

    def __init__(self, data):
        self.id = data.get('id')
        self.query = data.get('query')
        self.maptype = data.get('type')
        self.rr = data.get('rr')
        self.answer = data.get('answer')
        self.ttl = data.get('ttl')
        self.count = data.get('count')
        self.first_seen = data.get('first_seen')
        self.last_seen = data.get('last_seen')


class Country_amount(Base):
    __tablename__ = 'Country_Amount'

    code = Column(String(2), primary_key=True, unique=True)
    country = Column(String(50), unique=True)
    amount = Column(Integer)

    def __init__(self, data):
        self.code = data.get('code')
        self.country = data.get('country')
        self.amount = data.get('amount')


class Database(object):
    db_conn = ''

    def __init__(self, dsn=None):
        cfg = Config()
        if dsn:
            self.db_conn = dsn
        elif cfg.database.connection:
            self.db_conn = cfg.database.connection
        else:
            raise
        self.engine = create_engine(self.db_conn)
        self.Session = sessionmaker(bind=self.engine)

    def __del__(self):
        self.engine.dispose()

    def insert_malicious_dn_record(self, **data):
        session = self.Session()
        try:
            malicious_dn_record = Malicious_dn_records(data)
            session.add(malicious_dn_record)
            session.commit()
        except SQLAlchemyError as e:
            logging.info(str(e))
            return e
        session.close()

    def insert_malicious_ip_record(self, **data):
        session = self.Session()
        try:
            malicious_ip_record = Malicious_ip_records(data)
            session.add(malicious_ip_record)
            session.commit()
        except SQLAlchemyError as e:
            logging.info(str(e))
            return e
        finally:
            session.close()

    def delete_malicious_dn_record(self, dn):
        session = self.Session()
        try:
            result_list = session.query(Malicious_dn_records).filter(
                Malicious_dn_records.dn == dn).all()
            for query in result_list:
                session.delete(query)
                session.commit()
        except SQLAlchemyError as e:
            logging.info(str(e))
        finally:
            session.close()

    def delete_malicious_ip_record(self, ip):
        session = self.Session()
        try:
            # malicious_ip_record = Malicious_ip_records(data)
            result_list = session.query(Malicious_ip_records).filter(
                Malicious_ip_records.ip == ip).all()
            for query in result_list:
                session.delete(query)
                session.commit()
        except SQLAlchemyError as e:
            logging.info((str(e)))
        finally:
            session.close()

    def get_malicious_ip_record(self, ip):
        session = self.Session()
        try:
            ip_record = session.query(Malicious_ip_records).filter(
                Malicious_ip_records.ip.like('%{}%'.format(ip))).all()
            return ip_record
        except SQLAlchemyError as e:
            logging.info(str(e))
        finally:
            session.close()

    def get_malicious_dn_record(self, dn):
        session = self.Session()
        try:
            dn_record = session.query(Malicious_dn_records).filter(
                Malicious_dn_records.dn.like('%{}%'.format(dn))).all()
            return dn_record
        except SQLAlchemyError as e:
            logging.info((str(e)))
        finally:
            session.close()

    def get_all_malicious_dn_record(self):
        session = self.Session()
        try:
            dn_list = session.query(Malicious_dn_records.dn)
            return dn_list
        except SQLAlchemyError as e:
            logging.info((str(e)))
        finally:
            session.close()

    def get_pdns_record(self, dn=None, ip=None,
                        start='2016-01-01', end=datetime.date.today()):
        session = self.Session()
        try:
            if dn:
                result = session.query(Pdns_records).filter(
                    Pdns_records.query.like('%{}%'.format(dn)),
                    Pdns_records.first_seen >= start,
                    Pdns_records.last_seen <= '{} 23:59:59'.format(end))
            elif ip:
                result = session.query(Pdns_records).filter(
                    Pdns_records.answer.like('%P{%'.format(ip)),
                    Pdns_records.first_seen >= start,
                    Pdns_records.last_seen <= '{} 23:59:59'.format(end))
            return result
        except SQLAlchemyError as e:
            logging.info((str(e)))
        finally:
            session.close()

    def count_dn(self):
        session = self.Session()
        try:
            dn_count = session.query(Malicious_dn_records).count()
            return dn_count
        except SQLAlchemyError as e:
            logging.info("Database error counting dn:{}".format(e))
        finally:
            session.close()

    def count_ip(self):
        session = self.Session()
        try:
            ip_count = session.query(Malicious_ip_records).count()
            return ip_count
        except SQLAlchemyError as e:
            logging.info("Database error counting ip:{}".format(e))
        finally:
            session.close()

    def last_added_dn(self):
        session = self.Session()
        try:
            dn_list = session.query(Malicious_dn_records).order_by(
                Malicious_dn_records.idx.desc()).limit(10).all()
            return dn_list
        except SQLAlchemyError as e:
            logging.info("Database error getting last dn:{}".format(e))
        finally:
            session.close()

    def count_alive_dn(self, today=datetime.date.today()):
        session = self.Session()
        try:
            alive_dn_count = session.query(
                Pdns_records.query).filter(
                    Pdns_records.last_seen >= '{} 00:00:00'.format(today)
                ).filter(Pdns_records.query == Malicious_dn_records.dn
                         ).distinct(Pdns_records.query).count()
            return alive_dn_count
        except SQLAlchemyError as e:
            logging.info("Database error counting alive dn:{}".format(e))
        finally:
            session.close()

    def top_mapping_ip(self, today=datetime.date.today()):
        session = self.Session()
        try:
            top_mapping_ip = session.query(
                Pdns_records.answer,
                func.count(Pdns_records.answer).label("count")).filter(
                    Pdns_records.last_seen >= '{} 00:00:00'.format(today)
                ).group_by(Pdns_records.answer).order_by(
                    func.count(Pdns_records.answer).desc()).limit(10).all()
            return top_mapping_ip
        except SQLAlchemyError as e:
            logging.info("Database error getting top mapping ip:{}".format(e))
        finally:
            session.close()

    def count_dn_record(self, dn):
        session = self.Session()
        try:
            count = session.query(Pdns_records).filter(
                Pdns_records.query == dn).count()
            return count
        except SQLAlchemyError as e:
            logging.info("Database error counting dn records:{}".format(e))
        finally:
            session.close()

    def top10_country_amount(self):
        session = self.Session()
        try:
            top10_country_amount = session.query(Country_amount).order_by(
                Country_amount.amount.desc()).limit(10)
            return top10_country_amount
        except SQLAlchemyError as e:
            logging.info("Database error getting top10 country amount:{}"
                         .format(str(e)))
        finally:
            session.close()
