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
, CAST(dbo_modal.id AS INT) as [custom_dbo_modal_view_id]
 
FROM [source_db_database].[source_table_schema].[source_table_name] src --count:
INNER JOIN dbo.dbo_modal_view_tbl dbo_modal
                ON [src].[source_modal_id_column_in_src_dtl1] = [dbo_modal].[source_modal_id_column_in_dbo_modal1] --count:
                AND [src].[source_modal_id_column_in_src_dtl2] = [dbo_modal].[source_modal_id_column_in_dbo_modal2]