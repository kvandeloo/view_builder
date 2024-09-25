import pypyodbc
import os,re
 
class View_Builder(object):
    def __init__(self, server, source_database, source_table_schema, source_core_id_column, dbo_database = '',ignore_columns = [],exclude_null_empty = 1):
        #source connection info
        self.server = server
        self.source_database = source_database
        #self.username = username
        #self.password = password
        self.source_table_schema = source_table_schema
 
        #used in queries
        if dbo_database  == '':
            self.dbo_database = source_database + '_DBO'
        else:
            self.dbo_database = dbo_database
        self.source_core_id_column = source_core_id_column
        #columns to exclude from the views
        self.ignore_columns = ignore_columns
        self.exclude_null_empty = exclude_null_empty
 
        #for input/output files
        dirname, filename = os.path.split(os.path.abspath(__file__))
        self.dirname = dirname
 
        #get view template
        with open(dirname + '\\sql_templates\\view_template.sql', encoding = 'utf-8-sig') as f:
            view_template = f.read()
        self.view_template = view_template
 
    def insert_into(self, database, query):
        connection_info = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ self.server + ';DATABASE=' + database + ';Trusted_Connection=yes'
        connection = pypyodbc.connect(connection_info)
        #create a cursor to query the databse you've connected to
        cur = connection.cursor()
        try:
            cur.execute(query)
        except pypyodbc.ProgrammingError as err:
            pretty_err = err.args[1].replace('[Microsoft][ODBC Driver 17 for SQL Server][SQL Server]','')
            print(pretty_err)
            return False
        connection.commit()
        #close connections
        cur.close()
        connection.close()
        #return a list of tuples where each tuple is a row of data
        return True
   
    def query_db(self, database, query):
        '''return all results from query as a list of tuples'''
        connection_info = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+ self.server + ';DATABASE=' + database + ';Trusted_Connection=yes'
        connection = pypyodbc.connect(connection_info)
        #create a cursor to query the databse you've connected to
        cur = connection.cursor()
        try:
            cur.execute(query)
        except pypyodbc.ProgrammingError as err:
            print(err)
            return None
        #grab ALL results
        results = cur.fetchall()
        #close connections
        cur.close()
        connection.close()
        #return a list of tuples where each tuple is a row of data
        return results
 
    def source_tbl_is_populated(self,source_tbl):
        src_tbl_query = 'SELECT COUNT(*) FROM(SELECT TOP 1 * FROM  [' + self.source_table_schema + '].[' + source_tbl + ']) top_row'
        is_populated = self.query_db(self.source_database,src_tbl_query)
        try:
            is_populated = is_populated[0][0]
            return is_populated
        except:
            print('Cannot check count for table: ' + src_tbl_query)
            return 1
 
    def get_source_tbl_list(self, tables_to_exclude = []):
        query = 'SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = \'BASE TABLE\' ORDER BY TABLE_NAME'
        tables = self.query_db(self.source_database,query)
        source_tbl_list = []
        for table in tables:
            table_name = table[0]
            if table_name not in tables_to_exclude: #these are now chosen by the user in the input window
                is_populated = self.source_tbl_is_populated(table_name)
                table_map_row = (table_name,is_populated)
                source_tbl_list.append(table_map_row)
        return source_tbl_list
   
    def sql_insert_from_file(self,in_file,database):
        with open(in_file, encoding = 'utf-8-sig') as f:
            query = f.read()
            query = query.replace('source_table_schema',self.source_table_schema)     
        try:
            result = self.insert_into(database, query)
            if result == True:
                print('Ran query from ' + in_file + '\n')
            else:
                print('Failed to run query from ' + in_file + '\n')
        except:
            #run sp_ColumnBuilder manually in source db, if it doesn't exist there yet
            print('Failed to run query from ' + in_file + '\n')
            pass
   
    def build_dbo_tbl_from_view(self,table_schema,dbo_view_name):
        dbo_tbl = dbo_view_name + '_tbl'
        query = 'SELECT * INTO [' + table_schema + '].[' + dbo_tbl + '] FROM [' + table_schema + '].[' + dbo_view_name + ']'
        try:
            result = self.insert_into(self.dbo_database,query)
            if result == True:
                print('dbo table built: ' + dbo_tbl + '\n')
            else:
                print('***dbo table build FAILURE***: ' + dbo_tbl + '\n')
        except:
            print('***dbo table build FAILURE***: ' + dbo_tbl + '\n')
            pass
 
    def camel_to_underscores(self,camel_string):
        split = re.findall('[A-Z][^A-Z]*', camel_string)
        new_name = ''
        if not split or len(split) <= 1:
            new_name = camel_string.lower()
            if new_name == 'id':
                new_name = 'oldid'
        else:
            for item in split:
                new_name = new_name + "_" + item.lower()
            new_name = new_name[1:]
            if new_name.endswith('_id'):
                new_name = 'uuid_' + new_name.replace('_id','')
        if new_name == '' or not new_name:
            print("column rename failed: " + camel_string)
        return new_name
 
    def build_columns(self, source_table_name):
        column_query = 'EXEC ' + self.source_table_schema + '.sp_ColumnBuilderNew N\'' + self.source_table_schema + '\', N\'' + source_table_name + '\';'
        results = self.query_db(self.source_database, column_query)
        column_string = ''
        additional_column_string = ''
 
        for (column_sql,contains_data_query,column_name) in results:
            new_column_name = self.camel_to_underscores(column_name)
            #skip over columns the user said to ignore
            if column_name in self.ignore_columns:
                additional_column_string += '--' + column_sql + ' as [' + new_column_name + ']\n\t'
                continue
            #exclude columns that are always null or empty, maybe add a flag to turn this on or off?
            if self.exclude_null_empty == 1:
                contains_data = self.query_db(self.source_database,contains_data_query)
                if contains_data == 0:
                    additional_column_string += '--' + column_sql + ' as [' + new_column_name + ']\n\t'
                    continue
            #add column to string
            if column_sql not in [', src.[file_id] as [file_id]',', src.[patID] as [patid]']:
                if column_string == '':
                    column_string += '\t' + column_sql[1:] + ' as [' + new_column_name + ']\n\t' #remove leading comma from first column
                else:    
                    column_string += column_sql + ' as [' + new_column_name + ']\n\t'
        #add columns that are not needed/commented out
        if additional_column_string != '':
            column_string += '\n\t' + additional_column_string
        return column_string
   
    def create_view(self, source_table_name, dbo_view_name = ''):
        #create view name if no manual mapping was provided
        if dbo_view_name == '':
            dbo_view_name = source_table_name.replace('_tbl','').lower()
 
        #build columns
        column_string = self.build_columns(source_table_name)
   
        #build view def
        view_def = self.view_template.replace('source_db_database',self.source_database)
        view_def = view_def.replace('source_table_schema',self.source_table_schema)
        view_def = view_def.replace('source_core_id_column',self.source_core_id_column)
        view_def = view_def.replace('dbo_view_name',dbo_view_name)
        view_def = view_def.replace('source_table_name',source_table_name)
        view_def = view_def.replace('column_string',column_string)
   
        #execute view def
        try:
            result = self.insert_into(self.dbo_database, view_def)
            if result == True:
                print('Created view ' + dbo_view_name + '\n')
            else:
                print('SQL Insert Failed for ' + dbo_view_name + '\n')
        except:
            print('SQL Insert Failed for ' + dbo_view_name + '\n')
 
        #write view def to out_file
        out_file = self.dirname + '\\out_file.sql'
        #TODO: create a fresh out_file for each run?
        with open(out_file,'a',encoding = 'utf-8-sig') as f:
            f.write('\n\n')
            f.write(view_def)
 
    def make_all_views(self,tbl_to_view_mapping):
        self.sql_insert_from_file(self.dirname + '\\sql_templates\\sp_ColumnBuilderNew.sql',self.source_database)
 
        #TODO: create dbo.core view and dbo.core_tbl
 
        #create and execute modal views
        for (source_table_name,dbo_view_name,run) in tbl_to_view_mapping:
            if run == True:
                self.create_view(source_table_name, dbo_view_name)
       
        #start building tables after all views have been executed
        for (source_table_name,dbo_view_name,run) in tbl_to_view_mapping:
            #create view name if no manual mapping was provided
            if dbo_view_name == '':
                dbo_view_name = source_table_name.replace('_tbl','').lower()
            if run == True:
                self.build_dbo_tbl_from_view('dbo',dbo_view_name)
 
def main():
    #before running this tool, build dbo.core_tbl
    source_server = 'server_name'
    source_user = ''
    source_pw = ''
    source_db_database = 'source_database_name'
    dbo_database = source_db_database + '_DBO'
    source_table_schema = 'dbo'
    source_core_id_column = 'core_id'
    ignore_columns = ['core_id','person_num'] #columns you want commented out in every view where they occur
 
    #format: [(source_tbl_1,dbo_view_1,True),(source_tbl_2,dbo_view_2,True)]
    # tbl_to_view_mapping = [
    # ('appointments','',True),
    # ('charges','',True),
    # ('patients','patient_detail',True)
    # ]
 
    #run
    view_builder = View_Builder(source_server, source_db_database, source_user, source_pw, source_table_schema, source_core_id_column, dbo_database, ignore_columns)
    tbl_to_view_mapping = view_builder.get_source_tbl_list()
    #open a GUI that lets users edit the view names and map them to the source tables and checkbox to include/exclude the table
    view_builder.make_all_views(tbl_to_view_mapping)
   
 
if __name__ == '__main__':
    main()