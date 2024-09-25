CREATE PROCEDURE
source_table_schema.sp_ColumnBuilder
@table_schema VARCHAR(252),
@table_name VARCHAR(252)
AS
/*Replaced by sp_ColumnBuilderNew, but still useful for building views manually if needed.*/
SELECT
CASE WHEN COLUMN_NAME LIKE '%date%' OR COLUMN_NAME LIKE '%time%' THEN
                                CASE DATA_TYPE
                                WHEN 'varchar' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']
                                                                --if not a date, use: src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'int' THEN CONCAT(', ISNULL(TRY_CONVERT(DATE,CONCAT(
                                                                LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),4)
                                                                ,''-''
                                                                ,RIGHT(LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),6),2)
                                                                ,''-''
                                                                ,RIGHT(LTRIM(STR(src.[',COLUMN_NAME,'])),2)
                                                                )
                                                                ),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']
                                                                --if not a date, use: src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'bit' THEN CONCAT(', src.[CAST(',COLUMN_NAME,' as INT)] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']') --these will not actually be dates
                                WHEN 'float' THEN CONCAT(', ISNULL(TRY_CONVERT(DATE,CONCAT(
                                                                LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),4)
                                                                ,''-''
                                                                ,RIGHT(LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),6),2)
                                                                ,''-''
                                                                ,RIGHT(LTRIM(STR(src.[',COLUMN_NAME,'])),2)
                                                                )
                                                                ),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'date' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),'] ')
                                WHEN 'datetime' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'') [',LOWER(COLUMN_NAME),'] ')
                                ELSE CONCAT(', src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                END
                ELSE
                                CASE DATA_TYPE
                                WHEN 'varchar' THEN CONCAT(', src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'int' THEN CONCAT(', src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'bit' THEN CONCAT(', CAST(src.[',COLUMN_NAME,'] as INT) as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'float' THEN CONCAT(', CAST(src.[',COLUMN_NAME,'] as VARCHAR) as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                WHEN 'date' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,'])),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),'] ')
                                WHEN 'datetime' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,'])),''1800-01-01'') as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),'] ')
                                ELSE CONCAT(', src.[',COLUMN_NAME,'] as [',LOWER(REPLACE(COLUMN_NAME,' ','_')),']')
                                END
                END as sql_statement
                ,CASE WHEN DATA_TYPE IN ('date','datetime')
                                THEN CONCAT('SELECT COUNT (*) FROM (SELECT TOP 1 * FROM [',TABLE_SCHEMA,'].[',TABLE_NAME,'] WHERE NULLIF([',COLUMN_NAME,'],'''') IS NOT NULL) subq')
                                ELSE CONCAT('SELECT COUNT (*) FROM (SELECT TOP 1 * FROM [',TABLE_SCHEMA,'].[',TABLE_NAME,'] WHERE NULLIF([',COLUMN_NAME,'],'''') IS NOT NULL AND [',COLUMN_NAME,'] <> ''0'') subq')
                END as contains_data
                ,COLUMN_NAME          
FROM INFORMATION_SCHEMA.COLUMNS
 
WHERE TABLE_SCHEMA = @table_schema
AND TABLE_NAME = @table_name
ORDER BY ORDINAL_POSITION