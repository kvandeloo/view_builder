CREATE VIEW [dbo].[assignments] AS
 
/*
DROP TABLE [dbo].[assignments_tbl]
SELECT * INTO [dbo].[assignments_tbl]
FROM [dbo].[assignments]
CREATE UNIQUE CLUSTERED INDEX I_id ON [dbo].[assignments_tbl](id)
 
*/
 
SELECT
 
                src.[ClassNumber] as [class_number]
                , src.[AssignmentNumber] as [assignment_number]
                , src.[AssignmentName] as [assignment_name]
                , ISNULL(TRY_CONVERT(DATETIME,src.[DueDate]),'1800-01-01') as [due_date]
               
 
--new ids
, CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as [id]
, CAST(dbo_core.id AS INT) as [core_id]
 
FROM [StudentDemoDatabase].[src].[Assignments] src --count:
INNER JOIN dbo.core_tbl dbo_core
                ON [src].[StudentNumber] = dbo_core.core_identifier --count:
 
 
 
 
CREATE VIEW [dbo].[classes] AS
 
/*
DROP TABLE [dbo].[classes_tbl]
SELECT * INTO [dbo].[classes_tbl]
FROM [dbo].[classes]
CREATE UNIQUE CLUSTERED INDEX I_id ON [dbo].[classes_tbl](id)
 
*/
 
SELECT
 
                src.[ClassNumber] as [class_number]
                , src.[ClassDescription] as [class_description]
                , ISNULL(TRY_CONVERT(DATETIME,src.[StartDate]),'1800-01-01') as [start_date]
               
                --, src.[StudentNumber] as [student_number]
               
 
--new ids
, CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as [id]
, CAST(dbo_core.id AS INT) as [core_id]
 
FROM [StudentDemoDatabase].[src].[Classes] src --count:
INNER JOIN dbo.core_tbl dbo_core
                ON [src].[StudentNumber] = dbo_core.core_identifier --count:
 
 
 
 
CREATE VIEW [dbo].[contact_information] AS
 
/*
DROP TABLE [dbo].[contact_information_tbl]
SELECT * INTO [dbo].[contact_information_tbl]
FROM [dbo].[contact_information]
CREATE UNIQUE CLUSTERED INDEX I_id ON [dbo].[contact_information_tbl](id)
 
*/
 
SELECT
 
                src.[ContactType] as [contact_type]
                , src.[ContactDescription] as [contact_description]
               
                --, src.[StudentNumber] as [student_number]
               
 
--new ids
, CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as [id]
, CAST(dbo_core.id AS INT) as [core_id]
 
FROM [StudentDemoDatabase].[src].[ContactInformation] src --count:
INNER JOIN dbo.core_tbl dbo_core
                ON [src].[StudentNumber] = dbo_core.core_identifier --count:
 
 
 
 
CREATE VIEW [dbo].[dictionary] AS
 
/*
DROP TABLE [dbo].[dictionary_tbl]
SELECT * INTO [dbo].[dictionary_tbl]
FROM [dbo].[dictionary]
CREATE UNIQUE CLUSTERED INDEX I_id ON [dbo].[dictionary_tbl](id)
 
*/
 
SELECT
 
                src.[FieldName] as [field_name]
                , src.[Code] as [code]
                , src.[Description] as [description]
               
 
--new ids
, CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) as [id]
, CAST(dbo_core.id AS INT) as [core_id]
 
FROM [StudentDemoDatabase].[src].[Dictionary] src --count:
INNER JOIN dbo.core_tbl dbo_core
                ON [src].[StudentNumber] = dbo_core.core_identifier --count: