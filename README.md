# view_builder
Automate the creation of SQL views to clean and simplify the data you would like to copy to your database

_Sample reasons to use:_
1. Make a clean copy of relevant populated tables from a large, convoluted source database,
so it is easier to determine which tables might contain data relevant to the project at hand. 
Since the tool creates views for each table, it's easy for the user to go into SSMS after it runs 
and further manipulate the data to show exactly what is needed for a project, then rebuild the table. 
Since the tool works with views and copies of existing data, the user does not have to worry about 
accidentally deleting raw data that will be needed in the future. 
2. Generate fresh id's according to a standardized naming convention that can be used easily by other scripts. 
3. Help with data cleaning (cast date columns as date type, insert placeholder date if needed so migrations do not fail when using Pentaho) and meta-data cleaning (output column names will always be in underscores, making them easier to work with in other python scripts).

_Expected Results:_ 
1. New views selected by the user in the mapping window are created in the new database. 
2. Tables are built from the views in the new database. 
3. Messages print to the terminal to let the user know which views and tables are built successfully
and what SQL errors prevent views from executing. 
4. out_file.sql is generated with all of the views that the tool attempted to run to allow for easy troubleshooting. 
5. sp_ColumnBuilderNew is created in the source database to generate column logic for the new views (byproduct). 

_To run:_ 
1. Build "dbo.core_tbl" in the database where you want new views and tables to be written. See "core_template.sql" for specifications. 
2. Enter arguments in main.py. Argument list: 
* source_server = SSMS server where your databases are
* source_db_database = Database where source tables are
* dbo_database = Database where you want to write new views and tables (Default to source_db_database + '_DBO')
* source_table_schema = schema where source tables are (used for querying existing tables and to make sure we write sp_ColumnBuilderNew to an existing schema)
* source_core_id_column = identifier column in source database that you will use to link tables back to the new "core" table to ensure relationships are maintained
* optional: ignore_columns = Comma-separated list of columns you want commented out in every view where they occur, for example: ['StudentNumber','StudentGUID'] 
5. Run main.py from VSCode
   
_Drawbacks:_ 
1. Makes copies of existing data, which takes up extra space. 
2. Does not capture complex relationships among tables (for example, when the source data tables contain ids that would allow them to be grouped in multiple ways (Hobbies table has a StudentNumber and a ClubNumber, so the tool would include the Hobbies table whether the "core" table comes from "Students" or "Clubs", but the tool cannot work with two "core" tables in a single run), the tool only allows for a single "core" table.)

_Extensions:_ 
1. detail_view_main.py (along with the other detail_ files) can be used to build views that depend on the views just created by the tool. The user must specify (in the mapping window) what view/table in the new database this view depends on, 
and the user must specify which column(s) are used to link the source data to new view/table (example: ClassNumber = class_number).

_Future enhancements:_ 
1. Create a GUI that accepts the arguments for main (and has tooltips!), 
as well as the arguments that would be needed to build the "core" table (instead of having the user build it manually before running the tool). 
2. Have the tool comment out columns that are always NULL,'' or 0 so they are excluded from the tables built. 
3. Have the tool get the row count of each source table and the row count after the inner join to core_tbl,
and include those counts as comments in the source views so users can more easily detect problems when reviewing the code generated. 
4. Switch from using pypyodbc to sqlalchemy for easier connection and additional query/data insertion options. 
5. Restructure inheritance of View_Builder in subclass Detail_View_Builder and avoid duplicate functions 
for changing column/table names to underscores to make the code easier to adapt for future needs. 
