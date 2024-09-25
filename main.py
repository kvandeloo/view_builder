#TODO: make input window for main arguments
#TODO: add core arguments to first input window and build core table from template
#TODO: add counts to views
 
from view_builder import View_Builder
from mapping_window import Mapping_Window
 
def main():
    #before running this tool, build dbo.core_tbl
    source_server = 'DemoServer'
    source_db_database = 'StudentsDemoDatabase'
    dbo_database = source_db_database + '_DBO'
    source_table_schema = 'src'
    source_core_id_column = 'StudentNumber'
    ignore_columns = ['StudentNumber'] #columns you want commented out in every view where they occur
 
    #run
    view_builder = View_Builder(source_server, source_db_database, source_table_schema, source_core_id_column, dbo_database, ignore_columns)
    tbl_to_view_mapping = view_builder.get_source_tbl_list()
    #open a GUI that lets users edit the view names and choose which to run
    map_win = Mapping_Window()
    tbl_to_view_mapping = map_win.get_inputs(tbl_to_view_mapping)
    if len(tbl_to_view_mapping) > 0: #length will be 0 if the user cancels the input window
        view_builder.make_all_views(tbl_to_view_mapping)
   
 
if __name__ == '__main__':
    main()