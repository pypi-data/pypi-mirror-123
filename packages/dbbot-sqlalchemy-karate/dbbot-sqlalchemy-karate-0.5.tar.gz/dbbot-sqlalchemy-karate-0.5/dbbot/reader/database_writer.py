#  Copyright 2013-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from sqlalchemy import create_engine, Column, DateTime, ForeignKey, Integer, MetaData, Sequence, String, Table, Text, \
    UniqueConstraint
from sqlalchemy.sql import and_, select
from sqlalchemy.exc import IntegrityError
from dbbot import Logger


class DatabaseWriter(object):

    def __init__(self, db_url, verbose_stream):
        self._verbose = Logger('DatabaseWriter', verbose_stream)
        self._engine = create_engine(db_url)
        self._connection = self._engine.connect()
        self._metadata = MetaData()
        self._init_schema()

    def _init_schema(self):
        self._verbose('- Initializing database schema')
        self.test_runs = self._create_table_test_runs()
        self.tests = self._create_table_tests()
        self.test_status = self._create_table_test_status()
        self._metadata.create_all(bind=self._engine)

    def _create_table_test_runs(self):
        return self._create_table('test_runs', (
            Column('hash', String(64), nullable=False),
            Column('imported_at', DateTime, nullable=False),
            Column('started_at', DateTime, nullable=False),
            Column('elapsed', Integer, nullable=False),
            Column('passed', Integer, nullable=False),
            Column('failed', Integer, nullable=False),
            Column('build_number', Integer, nullable=False),
            Column('attempt', String(256)),
        ), ('hash','started_at'))

    def _create_table_tests(self):
        return self._create_table('tests', (
            Column('name', String(256), nullable=False),
            Column('package_name', String(256)),
            Column('suite', String(256)),
        ), ('name','suite'))

    def _create_table_test_status(self):
        return self._create_table('test_status', (
            Column('test_run_id', Integer, ForeignKey('test_runs.id'), nullable=False),
            Column('test_id', Integer, ForeignKey('tests.id'), nullable=False),
            Column('status', String(4), nullable=False),
            Column('elapsed', Integer, nullable=False)
        ), ('test_run_id', 'test_id'))

    def _create_table(self, table_name, columns, unique_columns=()):
        args = [Column('id', Integer, Sequence('{table}_id_seq'.format(table=table_name)), primary_key=True)]
        args.extend(columns)
        if unique_columns:
            args.append(UniqueConstraint(*unique_columns, name='unique_{table}'.format(table=table_name)))
        return Table(table_name, self._metadata, *args)

    def fetch_id(self, table_name, criteria):
        table = getattr(self, table_name)
        sql_statement = select([table.c.id]).where(
            and_(*(getattr(table.c, key) == value for key, value in criteria.items()))
        )
        result = self._connection.execute(sql_statement).first()
        if not result:
            raise Exception('Query did not yield id, even though it should have.'
                            '\nSQL statement was:\n%s\nArguments were:\n%s' % (sql_statement, list(criteria.values())))
        return result['id']

    def insert(self, table_name, criteria):
        sql_statement = getattr(self, table_name).insert()
        result = self._connection.execute(sql_statement, **criteria)
        return result.inserted_primary_key[0]

    def insert_or_ignore(self, table_name, criteria):
        try:
            self.insert(table_name, criteria)
        except IntegrityError:
            self._verbose('Failed insert to {table} with values {values}'.format(table=table_name,
                                                                                 values=list(criteria.values())))

    def close(self):
        self._verbose('- Closing database connection')
        self._connection.close()
