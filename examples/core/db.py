import copy
from collections import defaultdict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

__all__ = ['Database', 'EngineTemplate']

# https://docs.sqlalchemy.org/en/latest/core/engines.html
GENERAL_TPL = '{engine}{driver}://{user}:{password}@{host}:{port}/{database}'
SQLITE_TPL = 'sql://{path}'
ENGINE_TPL = {
    'postgresql': GENERAL_TPL,
    'mysql':      GENERAL_TPL,
    'oracle':     GENERAL_TPL,
    'mssql':      GENERAL_TPL,
    'sqlite':     SQLITE_TPL,
}

ENGINE_DEFAULT_SETTING = {
    'postgres': {
        'engine':   'postgresql',
        'user':     'postgres',
        'password': '',
        'host':     'localhost',
        'port':     5432,
        'database': '',
        'driver':   '', # psycopg2 / pg8000
    },

    'mysql': {
        'engine':   'mysql',
        'user':     'root',
        'password': '',
        'host':     'localhost',
        'port':     3306,
        'database': '',
        'driver':   '',
    },

    'oracle': {
        'engine':   'oracle',
        'user':     'root',
        'password': '',
        'host':     'localhost',
        'port':     1521,
        'database': '',
        'driver':   '',
    },

    'mssql': {
        'engine':   'oracle',
        'user':     'root',
        'password': '',
        'host':     'localhost',
        'port':     1433,
        'database': '',
        'driver':   '',
    },

    'sqlite': {
        'engine': 'sqlite',
        'path':   'sqlite3.db',  # None or empty string will be memory use
        'driver': '',
    },
}

class EngineTemplate(object):
    def __init__(self, engine, *args, **kwargs):
        if engine not in ENGINE_DEFAULT_SETTING:
            err_msg = "Unsupported engine.\n  Supported: {}".format(' | '.join(ENGINE_DEFAULT_SETTING.keys()))
            raise Exception(err_msg)

        self.value = {**ENGINE_DEFAULT_SETTING[engine], **kwargs)


class Database(object):
    def __init__(self, *args, **kwargs):
        kw_copy = copy.deepcopy(kwargs)
        if kw_copy['driver'] != '':
            kw_copy['driver'] += '+'

        self._session = None
        _engine = kw_copy['engine']
        if _engine == 'sqlite':
            self._engine_context = ENGINE_TPL[_engine].format(**kw_copy)
            if kw_copy['path'] != '':
                import platform
                if platform.system() == 'Windows':
                    self._engine_context = r'sqlite:///' + kw_copy['path']
        else:
            self._engine_context = ENGINE_TPL[_engine].format(**kw_copy)

    def __del__(self):
        if self._session:
            self._session.close()

    def connect(self):
        engine = create_engine(self._engine_context)
        self._session = sessionmaker(bind=engine)()
        return self

    def get_engine_context(self):
        return self._engine_context

    def get_session(self):
        return self._session
