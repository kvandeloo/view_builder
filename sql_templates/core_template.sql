/*
arguments needed:
${modeling_db_database}
${src_table_name} --source core table
 
--mapped column names from source core table:
${person_number}
${last_name}
${first_name}
${middle_name}
${date_of_birth}
${core_identifier}
*/
 
CREATE OR ALTER VIEW dbo.core AS
 
/*
DROP TABLE dbo.core_tbl
SELECT * INTO dbo.core_tbl
FROM dbo.core
CREATE UNIQUE CLUSTERED INDEX I_id ON dbo.core_tbl(id)
*/
 
SELECT
 
  src_tbl.${person_number} as person_number
, src_tbl.${last_name} as last_name
, src_tbl.${first_name} as first_name
, src_tbl.${middle_name} as middle_name
, ISNULL(TRY_CONVERT(DATE,src_tbl.${date_of_birth}),'1800-01-01') as date_of_birth
, src_tbl.${core_type} as core_identifier --backend unique core identifier is (used for joining other views back to core table)
 
--new id
,CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as id
 
FROM [${modeling_db_database}].[dbo].[${src_table_name}] src_tbl