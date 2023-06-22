-- Create a full backup of the database. Substitute the path 'C:\YourFolder' with the target location of the backup.


BACKUP DATABASE [WideWorldImportersDW] 
TO  DISK = N'C:\YourFolder\WideWorldImportersDW.bak' 
WITH FORMAT, INIT,  NAME = N'WideWorldImportersDW-Full Database Backup', SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10;
GO
