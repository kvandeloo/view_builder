import os
from view_builder import View_Builder
 
class Detail_View_Builder(View_Builder):
    def __init__(self, server, source_database, source_table_schema, source_core_id_column, dbo_database = '',ignore_columns = [],exclude_null_empty = 1):
        super().__init__(server, source_database, source_table_schema, source_core_id_column, dbo_database,ignore_columns,exclude_null_empty)
        #add join column(s)
        # self.source_core_id_column = source_core_id_column
 
        #get detail view template
        dirname, filename = os.path.split(os.path.abspath(__file__))
        with open(dirname + '\\sql_templates\\detail_view_template.sql', encoding = 'utf-8-sig') as f:
            detail_view_template = f.read()
        self.detail_view_template = detail_view_template
 
    def create_detail_view(self, source_table_name, dbo_modal_view, source_modal_id_column_in_dbo_modal1, source_modal_id_column_in_src_dtl1, source_modal_id_column_in_dbo_modal2 = '', source_modal_id_column_in_src_dtl2 = '', dbo_view_name = ''):
        #create view name if no manual mapping was provided
        if dbo_view_name == '':
            dbo_view_name = source_table_name.replace('_tbl','').lower()
 
        #build columns
        column_string = self.build_columns(source_table_name)
   
        #build view def
        view_def = self.detail_view_template.replace('source_db_database',self.source_database)
        view_def = view_def.replace('source_table_schema',self.source_table_schema)
        view_def = view_def.replace('source_modal_id_column_in_dbo_modal1',source_modal_id_column_in_dbo_modal1)
        view_def = view_def.replace('source_modal_id_column_in_src_dtl1',source_modal_id_column_in_src_dtl1)
        if source_modal_id_column_in_dbo_modal2 == '' and source_modal_id_column_in_src_dtl2 == '':
            view_def = view_def.replace('AND [src].[source_modal_id_column_in_src_dtl2] = [dbo_modal].[source_modal_id_column_in_dbo_modal2]','')
        else:
            view_def = view_def.replace('source_modal_id_column_in_dbo_modal2',source_modal_id_column_in_dbo_modal2)
            view_def = view_def.replace('source_modal_id_column_in_src_dtl2',source_modal_id_column_in_src_dtl2)
        view_def = view_def.replace('dbo_view_name',dbo_view_name)
        view_def = view_def.replace('source_table_name',source_table_name)
        view_def = view_def.replace('column_string',column_string)
        view_def = view_def.replace('dbo_modal_view',dbo_modal_view)
   
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
 
    def make_detail_views(self,tbl_to_view_mapping):
 
        self.sql_insert_from_file(self.dirname + '\\sql_templates\\sp_ColumnBuilder.sql',self.source_database)
 
        #create and execute submodal views
        #TODO: add to tbl_to_view_mapping: , dbo_modal_view, source_modal_id_column, source_modal_id_column_in_src_dtl
        for (source_table_name,dbo_view_name,run, dbo_modal_view, source_modal_id_column_in_dbo_modal1, source_modal_id_column_in_src_dtl1, source_modal_id_column_in_dbo_modal2, source_modal_id_column_in_src_dtl2) in tbl_to_view_mapping:
            if run == True:
                self.create_detail_view(source_table_name, dbo_modal_view, source_modal_id_column_in_dbo_modal1, source_modal_id_column_in_src_dtl1, source_modal_id_column_in_dbo_modal2, source_modal_id_column_in_src_dtl2, dbo_view_name)
       
        #start building tables after all views have been executed
        for (source_table_name,dbo_view_name,run, dbo_modal_view, source_modal_id_column_in_dbo_modal1, source_modal_id_column_in_src_dtl1, source_modal_id_column_in_dbo_modal2, source_modal_id_column_in_src_dtl2) in tbl_to_view_mapping:
            #create view name if no manual mapping was provided
            if dbo_view_name == '':
                dbo_view_name = source_table_name.replace('_tbl','').lower()
            if run == True:
                self.build_dbo_tbl_from_view('dbo',dbo_view_name)
 
def main():
    #before running this tool, build dbo.core_tbl and work.documents_tbl
    source_server = 'server_name'
    source_db_database = 'source_database_name'
    dbo_database = source_db_database + '_DBO'
    source_table_schema = 'dbo'
    source_core_id_column = 'core_id'
    ignore_columns = ['core_id','person_number'] #columns you want commented out in every view where they occur
 
    #run
    detail_view_builder = Detail_View_Builder(source_server, source_db_database, source_table_schema, source_core_id_column, dbo_database, ignore_columns)
    tbl_to_view_mapping = detail_view_builder.get_source_tbl_list()
    #open a GUI that lets users edit the view names and map them to the source tables and checkbox to include/exclude the table
    detail_view_builder.make_detail_views(tbl_to_view_mapping)
 
if __name__ == '__main__':
    main()