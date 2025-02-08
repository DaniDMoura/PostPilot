CREATE DATABASE PostManager
GO
USE PostManager;
GO
CREATE TABLE credencials (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
)
GO

