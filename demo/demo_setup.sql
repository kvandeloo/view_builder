USE StudentDemoDatabase
CREATE SCHEMA src;
CREATE TABLE src.Students (StudentNumber varchar(250),LastName varchar(250),FirstName varchar(250));
INSERT INTO src.Students VALUES ('12345','Mouse','Mickey');
INSERT INTO src.Students VALUES ('23456','Mouse','Minnie');
INSERT INTO src.Students VALUES ('34567','Mallard','Daffy');
 
CREATE TABLE src.ContactInformation (StudentNumber varchar(250),ContactType varchar(250), ContactDescription varchar(250));
INSERT INTO src.ContactInformation VALUES ('12345','Home Phone','111-222-3333');
INSERT INTO src.ContactInformation VALUES ('12345','Email','mmouse1@disney.com');
INSERT INTO src.ContactInformation VALUES ('23456','Email','mouse2@disney.com');
INSERT INTO src.ContactInformation VALUES ('23456','Home Address','123 Happy Lane, Disney, FL 34543');
 
CREATE TABLE src.Classes (StudentNumber varchar(250),ClassNumber int,ClassDescription varchar(250), StartDate date);
INSERT INTO src.Classes VALUES ('12345',1,'History of Cheese','2024-01-01');
INSERT INTO src.Classes VALUES ('23456',2,'Cheesemaking 101','2024-01-01');
INSERT INTO src.Classes VALUES ('34567',3,'Swimming Lessons','2024-01-01');
 
CREATE TABLE src.Assignments (ClassNumber int, AssignmentNumber int, AssignmentName varchar(250), DueDate date);
INSERT INTO src.Assignments VALUES (1,1,'3-Page Paper','2024-01-15');
INSERT INTO src.Assignments VALUES (1,2,'Code Sample','2024-02-02');
INSERT INTO src.Assignments VALUES (2,3,'Powerpoint Presentation','2024-01-15');
INSERT INTO src.Assignments VALUES (2,4,'Lab Report','2024-02-02');
INSERT INTO src.Assignments VALUES (3,5,'In-Class Practice','2024-01-15');
INSERT INTO src.Assignments VALUES (3,6,'Final Assessment','2024-02-02');
 
CREATE TABLE src.Dictionary (FieldName varchar(250),Code int, Description varchar(250));
INSERT INTO src.Dictionary VALUES ('PayFeeTo',1,'Student Government');
 
CREATE TABLE src.Hobbies(StudentNumber varchar(250),ClubNumber int, HobbyNumber int, HobbyName varchar(250));
 
 
-------
USE StudentDemoDatabase_DBO
CREATE TABLE dbo.core_tbl (id INT,student_number varchar(250),last_name varchar(250),first_name varchar(250));
--INSERT INTO dbo.core_tbl VALUES (1,'12345','Mouse','Mickey');
--INSERT INTO dbo.core_tbl VALUES (2,'23456','Mouse','Minnie');
--INSERT INTO dbo.core_tbl VALUES (3,'34567','Mallard','Daffy');
 
CREATE VIEW dbo.core AS
 
/*
DROP TABLE dbo.core_tbl
SELECT * INTO dbo.core_tbl
FROM dbo.core
CREATE UNIQUE CLUSTERED INDEX I_id ON dbo.core_tbl(id)
*/
 
SELECT
CAST(ROW_NUMBER()OVER(ORDER BY (SELECT NULL)) AS INT) AS id
,StudentNumber as student_number
,LastName as last_name
,FirstName as first_name
FROM StudentDemoDatabase.src.Students

;

SELECT * INTO dbo.core_tbl
FROM dbo.core;
CREATE UNIQUE CLUSTERED INDEX I_id ON dbo.core_tbl(id);