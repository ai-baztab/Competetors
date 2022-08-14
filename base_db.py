import psycopg2

class DBHandler:
    def __init__(self, db_name, connection, user_name='postgres', password='1372', host='127.0.0.1', port='5432'):
        """

        param db_name: it could be None if the connection has been initialized and is going to be passed
                    otherwise it must be a string
        :param connection: instance of psycopg2

        """
        condition_a = db_name is None
        condition_b = connection is None
        assert condition_b != condition_a, 'either database name or the connection must be passed Also only one of ' \
                                           'them must be specified '

        if db_name is not None:
            self.conn = psycopg2.connect(user=user_name, password=password, host=host, port=port
                                         )
            self.conn.autocommit = True
            res = self.create_db(db_name)
            assert res is True
        else:
            self.conn = connection
        self.tables = []

    def create_db(self, name):
        """
            creates database
        :param name: name of the database
        :return:  if the process was successful return True, else False
        """
        sql = f'CREATE database {name}'
        return self.execute_command(sql)

    def create_table(self, name, columns):
        """

        param name is the name of the table that is going to be created,
        param columns must be a string in full sql mode
        return: if the process was successful return True, else False

        """
        assert isinstance(columns, str)
        if self.check_table_exists(name):
            return True
        command = f'CREATE TABLE {name}({columns});'
        return self.execute_command(command)

    def insert_row(self, table, row):
        assert self.check_table_exists(table), 'table does not exist!! please create the able from create_table()'
        command = f'''INSERT INTO {table} 
        VALUES ({row})'''
        return self.execute_command(command)

    def check_table_exists(self, table_name):
        if table_name in self.tables:
            return True
        command = f'''
        SELECT EXISTS (
    SELECT FROM 
        pg_tables
    WHERE 
        tablename  = '{table_name}'
    )
        '''
        try:
            cursor = self.conn.cursor()
            cursor.execute(command)
            result = cursor.fetchone()
            if result[0]:
                self.tables.append(table_name)
                return True
            else:
                return False
        except NameError:
            print("could not check existence of the table")

    # there are no tables named "tableName"

    def execute_command(self, command):
        """
        execute the input sql command
        :param command: string in sql mode
        :return:  if the process was successful return True, else False
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(command)
            cursor.close()
            return True
        except:
            return False

    def del_row(self, row, ids, condition):
        pass
