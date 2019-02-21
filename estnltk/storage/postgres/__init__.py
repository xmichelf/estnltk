"""This package provides tools to conveniently store and search `estnltk` text objects in a postgres database.

Example usage:

    # connect to database, create a new table
    storage = PostgresStorage(dbname='estnltk', user='***', password='***')
    table = 'tmp'
    storage.create_table(table)

    # insert some data
    text = Text('ööbik laulab.').analyse('morphology')
    key = storage.insert(table, text)

    # select all data in the table
    for key, text in storage.select(table):
        print(key, text)

    # search by key
    txt = storage.select_by_key(table, key=key)

    # search using layer attributes
    q = JsonbQuery('morph_analysis', lemma='laulma')
    for key, txt in storage.select(table, query=q):
        print(key, txt)

    # search using composite query
    q = (JsonbQuery('morph_analysis', lemma='ööbik') | JsonbQuery('morph_analysis', lemma='öökull')) &
        JsonbQuery('morph_analysis', lemma='laulma')
    for key, txt in storage.select(table, query=q):
        print(key, txt)

"""
from .sql_strings import collection_table_name
from .sql_strings import structure_table_name
from .sql_strings import layer_table_name
from .sql_strings import fragment_table_name

from .pg_operations import collection_table_identifier
from .pg_operations import structure_table_identifier
from .pg_operations import layer_table_identifier
from .pg_operations import fragment_table_identifier

from .pg_operations import create_schema
from .pg_operations import create_collection_table
from .pg_operations import create_structure_table

from .pg_operations import table_exists
from .pg_operations import table_identifier
from .pg_operations import collection_table_exists
from .pg_operations import structure_table_exists
from .pg_operations import layer_table_exists
from .pg_operations import fragment_table_exists

from .pg_operations import delete_schema
from .pg_operations import drop_collection_table
from .pg_operations import drop_structure_table
from .pg_operations import drop_fragment_table
from .pg_operations import drop_layer_table

from .pg_operations import build_layer_ngram_query
from .pg_operations import build_column_ngram_query
from .pg_operations import build_sql_query
from .pg_operations import select_raw

from .pg_operations import count_rows

from .where_clause import WhereClause
from .selected_columns import SelectedColumns
from .selected_columns import SelectedColumns_2

from .jsonb_layer_query import JsonbLayerQuery
from .jsonb_text_query import JsonbTextQuery

from .collection import RowMapperRecord
from .collection import PgCollection
from .collection import PgCollectionException

from .pgpass_parsing import parse_pgpass

from .pg_subcollection import PgSubCollection

from .storage import PgStorageException
from .storage import PostgresStorage
