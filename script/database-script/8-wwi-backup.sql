-- Create a full backup of the database. Substitute the path 'C:\YourFolder' with the target location of the backup.

BACKUP DATABASE [WideWorldImporters] 
TO  DISK = N'C:\YourFolder\WideWorldImporters.bak' 
WITH FORMAT, INIT,  NAME = N'WideWorldImporters-Full Database Backup', SKIP, NOREWIND, NOUNLOAD, COMPRESSION,  STATS = 10;
GO
�