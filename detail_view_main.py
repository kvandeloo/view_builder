from detail_view_builder import Detail_View_Builder
from detail_mapping_window import Detail_Mapping_Window
 
def main():
    #before running this tool, build dbo.core_tbl
    source_server = 'DemoServer'
    source_db_database = 'StudentsDemoDatabase'
    dbo_database = source_db_database + '_DBO'
    source_table_schema = 'src'
    source_core_id_column = '' #leave blank for detail view builder
    ignore_columns = ['ClassNumber','ID'] #columns you want commented out in every view where they occur
 
    #run
    detail_view_builder = Detail_View_Builder(source_server, source_db_database, source_table_schema, source_core_id_column, dbo_database=dbo_database, ignore_columns=ignore_columns)
    tbl_to_view_mapping = detail_view_builder.get_source_tbl_list()
    #open a GUI that lets users edit the view names and choose which to run
    map_win = Detail_Mapping_Window()
    tbl_to_view_mapping = map_win.get_inputs(tbl_to_view_mapping)
    if len(tbl_to_view_mapping) > 0: #length will be 0 if the user cancels the input window
        detail_view_builder.make_detail_views(tbl_to_view_mapping)
   
 
if __name__ == '__main__':
    main()