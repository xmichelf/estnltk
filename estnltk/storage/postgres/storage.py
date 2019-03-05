import pandas

import psycopg2
from psycopg2.sql import SQL, Identifier, Literal

from estnltk import logger
from estnltk.storage.postgres import PgCollection
from estnltk.storage.postgres import parse_pgpass
from estnltk.storage.postgres import drop_layer_table
from estnltk.storage.postgres import drop_structure_table
from estnltk.storage.postgres import drop_collection_table


class PgStorageException(Exception):
    pass


class PostgresStorage:
    """`PostgresStorage` instance wraps a database connection and
    exposes interface to conveniently search/save json data.
    """

    def __init__(self, dbname=None, user=None, password=None, host=None, port=None,
                 pgpass_file=None, schema="public", role=None, temporary=False, **kwargs):
        """
        Connects to database either using connection parameters if specified, or ~/.pgpass file.

            ~/.pgpass file format: hostname:port:database:username:password

        """
        self.schema = schema
        self.temporary = temporary

        conn_param = parse_pgpass(pgpass_file, host, port, dbname, user, password)

        if role is None:
            role = conn_param['user']

        logger.info('connecting to host: '
                    '{host!r}, port: {port!r}, dbname: {dbname!r}, user: {user!r}'.format(**conn_param))

        try:
            self.conn = psycopg2.connect(**conn_param, **kwargs)
        except Exception:
            logger.error('Failed to connect '
                         'host: {host!r}, port: {port!r}, dbname: {dbname!r}, user: {user!r}.'.format(**conn_param))
            raise

        with self.conn.cursor() as c:
            c.execute(SQL("SET ROLE {};").format(Identifier(role)))
        self.conn.commit()

        tables = self._get_all_tables()
        self._collections = {table: None for table in tables if table + '__structure' in tables}

        logger.info('schema: {!r}, temporary: {!r}, role: {!r}'.format(self.schema, self.temporary, role))

    def close(self):
        """Closes database connection"""
        self.conn.close()

    def closed(self):
        return self.conn.closed

    def get_all_table_names(self):
        if self.closed():
            return None
        with self.conn.cursor() as c:
            c.execute(SQL(
                "SELECT table_name FROM information_schema.tables WHERE table_schema=%s AND table_type='BASE TABLE'"),
                [self.schema])
            table_names = [row[0] for row in c.fetchall()]
            return table_names

    def _get_all_tables(self):
        if self.closed():
            return None
        with self.conn.cursor() as c:
            c.execute(SQL(
                "SELECT table_name, "
                       "pg_size_pretty(pg_total_relation_size({schema}||'.'||table_name)), "
                       "obj_description(({schema}||'.'||table_name)::regclass) "
                "FROM information_schema.tables "
                "WHERE table_schema={schema} AND table_type='BASE TABLE';").format(schema=Literal(self.schema))
                )
            tables = {row[0]: {'total_size': row[1], 'comment':row[2]} for row in c}
            return tables

    def get_collection(self, table_name: str, meta_fields: dict = None):
        """Returns a new instance of `PgCollection` without physically creating it."""
        collection = self[table_name]
        if meta_fields is not None:
            collection.meta = meta_fields
        return collection

    @property
    def collections(self):
        return sorted(self._collections)

    def __getitem__(self, item):
        collection = self._collections.get(item)
        if collection is not None:
            return collection
        collection = PgCollection(item, self)
        self._collections[item] = collection
        return collection

    def __delitem__(self, key):
        collection = self._collections.get(key)
        if collection is None:
            raise KeyError('collection not found: {!r}'.format(key))

        assert collection.name == key, (collection.name, key)

        if collection.exists():
            for layer, v in collection.structure.structure.items():
                if v['layer_type'] == 'detached':
                    drop_layer_table(self, key, layer)
            drop_structure_table(self, key)
            drop_collection_table(self, key)
        del self._collections[key]

    def __str__(self):
        return '{self.__class__.__name__}({self.conn.dsn} schema={self.schema} temporary={self.temporary})'.format(
                self=self)

    def _repr_html_(self):
        tables = self._get_all_tables()

        structure = {}

        collection_tables = ''
        if tables is not None:
            for t, v in tables.items():
                t_split = t.split('__')
                if len(t_split) == 1 and t_split[0] + '__structure' in tables:
                    structure[(t_split[0], '')] = v
                elif len(t_split) == 3 and t_split[2] == 'layer' and t_split[0] in tables:
                    structure[(t_split[0], t_split[1])] = v

            if structure:
                df = pandas.DataFrame.from_dict(structure, orient='index', columns=['total_size', 'comment'])
                df.index.names = ('collection', 'layers')
                collection_tables = df.to_html()
            else:
                collection_tables = '<br/>This storage has no collections.'
        return ('<b>{self.__class__.__name__}</b><br/>\n{self.conn.dsn} schema={self.schema}<br/>'
                'temporary={self.temporary}\n'
                '{collections}').format(
                self=self, collections=collection_tables)
