from abc import ABC, abstractmethod
import json
from sqlalchemy import create_engine
import psycopg2


class DBMS(ABC):
    def __init__(self, **kwargs):
        self.host = kwargs['host']
        self.user = kwargs['user']
        self.pwd = kwargs['pwd']
        self.db = kwargs['db']
        self._con = None
        self._cursor = None

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def cursor(self):
        pass

    @abstractmethod
    def execute(self, sql, params):
        pass

    @abstractmethod
    def query(self, sql, params):
        pass

    @abstractmethod
    def fetchone(self):
        pass

    @abstractmethod
    def fetchall(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass


