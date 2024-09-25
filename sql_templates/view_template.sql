CREATE VIEW [dbo].[dbo_view_name] AS
 
/*
DROP TABLE [dbo].[dbo_view_name_tbl]
SELECT * INTO [dbo].[dbo_view_name_tbl]
FROM [dbo].[dbo_view_name]
CREATE UNIQUE CLUSTERED INDEX I_id ON [dbo].[dbo_view_name_tbl](id)
 
*/
 
SELECT
 
column_string
 
--new ids
, CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as [id]
, CAST(dbo_core.id AS INT) as [core_id]
 
FROM [source_db_database].[source_table_schema].[source_table_name] src --count:
INNER JOIN dbo.core_tbl dbo_core
                ON [src].[source_core_id_column] = dbo_core.core_identifier --count: