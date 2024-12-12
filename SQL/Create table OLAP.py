import pandas as pd
import pyodbc
from pyodbc import Error

connection = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=DinhNamNguyen\DinhNam;'
    'DATABASE=da2;'
    'Trusted_Connection=yes;'
)

cursor = connection.cursor()

try:
    cursor.execute("SELECT 1")  # Truy vấn đơn giản để kiểm tra kết nối
    print("Kết nối thành công!")
except Exception as e:
    print("Kết nối thất bại!")
    print("Lỗi:", e)

create_tables_queries = [
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_Date' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_Date (
            DateID DATE PRIMARY KEY NOT NULL,
            DateMonth INT,
            DateQuarter INT,
            DateYear INT
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_Web' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_Web (
            WebID INT PRIMARY KEY NOT NULL,
            Web VARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_JobLevel' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_JobLevel(
        JobLevelID int PRIMARY KEY NOT NULL,
        JobLevelName NVARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_GroupJob' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_GroupJob(
        GroupJobID int PRIMARY KEY NOT NULL,
        GroupJobName NVARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_Address' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_Address(
        CityID INT PRIMARY KEY,
        CityName NVARCHAR(500),
        EcoRegion NVARCHAR(255),
        Region NVARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_ExpRange' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_ExpRange(
        ExpRangeID INT  PRIMARY KEY,
        ExpRange NVARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Dim_SalaryRange' AND xtype='U')
    BEGIN
        CREATE TABLE Dim_SalaryRange(
        SalaryRangeID INT PRIMARY KEY,
        SalaryRange VARCHAR(255)
        );
    END
    """,
    """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Fact_Job' AND xtype='U')
    BEGIN
        CREATE TABLE Fact_Job(
        JobID VARCHAR(255) PRIMARY KEY,
        JobTitle NVARCHAR(500),
        JobURL VARCHAR(3000),
        JobType NVARCHAR(500),
        GroupJobID INT,
        JobLevelID  INT,
        DateID DATE,
        CompanyName NVARCHAR(255),
        CompanyURL VARCHAR(3000),
        TimeExpire DATE,
        Salary DECIMAL(10,2),
        SalaryRangeID INT,
        CityID INT,
        Address NVARCHAR(3000),
        Benefit NVARCHAR(3000),
        JobDes NVARCHAR(3000),
        JobReq NVARCHAR(3000),
        ExpRangeID INT,
        Exp INT,
        WebID INT,

        FOREIGN KEY (GroupJobID) REFERENCES Dim_GroupJob(GroupJobID),
        FOREIGN KEY (JobLevelID) REFERENCES Dim_JobLevel(JobLevelID),
        FOREIGN KEY (DateID) REFERENCES Dim_Date(DateID),
        FOREIGN KEY (CityID) REFERENCES Dim_Address(CityID),
        FOREIGN KEY (SalaryRangeID) REFERENCES Dim_SalaryRange(SalaryRangeID),
        FOREIGN KEY (ExpRangeID) REFERENCES Dim_ExpRange(ExpRangeID),
        FOREIGN KEY (WebID) REFERENCES Dim_Web(WebID)
        );
    END
    """
]
try:
    cursor = connection.cursor()
    for query in create_tables_queries:
        cursor.execute(query)
        print("Tạo bảng thành công!")
except Error as e:
    print(f"Lỗi: {e}")


# Commit và đóng kết nối
connection.commit()
connection.close()