CREATE PROCEDURE
source_table_schema.sp_ColumnBuilderNew
@table_schema VARCHAR(252),
@table_name VARCHAR(252)
AS
/*outputs data needed by view_builder.py to pull columns from each table into a view, 
change column names to underscores if needed (from camelCase or PascalCase), 
insert placeholder dates in place of null dates, and change float type to varchar where appropriate.*/
SELECT
CASE WHEN COLUMN_NAME LIKE '%date%' OR COLUMN_NAME LIKE '%time%' THEN
                                CASE DATA_TYPE
                                WHEN 'varchar' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'')
                                                                /*if not a date, use: src.[',COLUMN_NAME,']*/')
                                WHEN 'int' THEN CONCAT(', ISNULL(TRY_CONVERT(DATE,CONCAT(
                                                                LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),4)
                                                                ,''-''
                                                                ,RIGHT(LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),6),2)
                                                                ,''-''
                                                                ,RIGHT(LTRIM(STR(src.[',COLUMN_NAME,'])),2)
                                                                )
                                                                ),''1800-01-01'')
                                                                /*if not a date, use: src.[',COLUMN_NAME,']*/')
                                WHEN 'bit' THEN CONCAT(', src.[CAST(',COLUMN_NAME,' as INT)]') --these will not actually be dates
                                WHEN 'float' THEN CONCAT(', ISNULL(TRY_CONVERT(DATE,CONCAT(
                                                                LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),4)
                                                                ,''-''
                                                                ,RIGHT(LEFT(LTRIM(STR(src.[',COLUMN_NAME,'])),6),2)
                                                                ,''-''
                                                                ,RIGHT(LTRIM(STR(src.[',COLUMN_NAME,'])),2)
                                                                )
                                                                ),''1800-01-01'')')
                                WHEN 'date' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'')')
                                WHEN 'datetime' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'')')
                                ELSE CONCAT(', src.[',COLUMN_NAME,']')
                                END
                ELSE
                                CASE DATA_TYPE
                                WHEN 'varchar' THEN CONCAT(', src.[',COLUMN_NAME,']')
                                WHEN 'int' THEN CONCAT(', src.[',COLUMN_NAME,']')
                                WHEN 'bit' THEN CONCAT(', CAST(src.[',COLUMN_NAME,'] as INT)')
                                WHEN 'float' THEN CONCAT(', CAST(LTRIM(RTRIM(STR(src.[',COLUMN_NAME,']))) as VARCHAR)')
                                WHEN 'date' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'') ')
                                WHEN 'datetime' THEN CONCAT(', ISNULL(TRY_CONVERT(DATETIME,src.[',COLUMN_NAME,']),''1800-01-01'') ')
                                ELSE CONCAT(', src.[',COLUMN_NAME,']')
                                END
                END as sql_statement
                ,CASE WHEN DATA_TYPE IN ('date','datetime')
                                THEN CONCAT('SELECT COUNT (*) FROM (SELECT TOP 1 * FROM [',TABLE_SCHEMA,'].[',TABLE_NAME,'] WHERE NULLIF([',COLUMN_NAME,'],'''') IS NOT NULL) subq')
                                WHEN DATA_TYPE LIKE ('decimal%')
                                THEN CONCAT('SELECT COUNT (*) FROM (SELECT TOP 1 * FROM [',TABLE_SCHEMA,'].[',TABLE_NAME,'] WHERE [',COLUMN_NAME,'] IS NOT NULL) subq')
                                ELSE CONCAT('SELECT COUNT (*) FROM (SELECT TOP 1 * FROM [',TABLE_SCHEMA,'].[',TABLE_NAME,'] WHERE NULLIF([',COLUMN_NAME,'],'''') IS NOT NULL AND [',COLUMN_NAME,'] <> ''0'') subq')
                END as contains_data
                ,COLUMN_NAME          
FROM INFORMATION_SCHEMA.COLUMNS
 
WHERE TABLE_SCHEMA = @table_schema
AND TABLE_NAME = @table_name
ORDER BY ORDINAL_POSITION