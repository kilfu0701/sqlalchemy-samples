from core import EngineTemplate

DB_CONFIGS = {
    'sqlite_memory': {
        'engine': 'sqlite',
        'path':   '',  # None or empty string will be memory use
        'driver': '',
    },

    'sqlite_file': {
        'engine': 'sqlite',
        'path':   'sqlite3.db',
        'driver': '',
    },

    'sqlite':   EngineTemplate('sqlite').value,
    'postgres': EngineTemplate('postgres').value,
    'mysql':    EngineTemplate('mysql').value,
    'oracle':   EngineTemplate('oracle').value,
    'mssql':    EngineTemplate('mssql').value,
}
