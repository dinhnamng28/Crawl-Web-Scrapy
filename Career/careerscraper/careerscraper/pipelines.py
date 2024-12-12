# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pyodbc
from datetime import datetime

class CareerscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        ## Price --> convert to float
        value = adapter.get('salary')
        adapter['salary'] = float(value)

        ## Exp --> convert to int
        value = adapter.get('exp')
        adapter['exp'] = round(float(value))

        return item


class SaveToSQLServerPipeLine:

    def __init__(self):
        self.conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DinhNamNguyen\DinhNam;'  # Hoặc là tên server SQL của bạn
            'DATABASE=career_stg;'
            'Trusted_Connection=yes;'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        ## Create jobs table if none exists
        self.cur.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='jobs' AND xtype='U')
        CREATE TABLE jobs(
            id VARCHAR(500) NOT NULL PRIMARY KEY, 
            url VARCHAR(1000),
            title NVARCHAR(500),
            company_name NVARCHAR(500),
            company_url VARCHAR(1000),
            time_update DATETIME,
            time_expire DATETIME,
            salary DECIMAL(10,2),
            exp INT,
            job_level NVARCHAR(500),
            group_job NVARCHAR(500),
            job_type NVARCHAR(500),
            benefit TEXT,
            job_des TEXT,
            job_req TEXT,
            city NVARCHAR(500),
            address TEXT,
            web NVARCHAR(500)         
        );
        
        """)
        self.conn.commit()

        self.cur.execute("""
        IF NOT EXISTS (
            SELECT * 
            FROM sys.indexes 
            WHERE name='IX_jobs_url' AND object_id=OBJECT_ID('jobs')
        )
        BEGIN
            CREATE INDEX IX_jobs_url ON jobs(url);
        END
        """)
        self.conn.commit()
    
    def process_item(self, item, spider):
        # Define insert statement
        self.cur.execute("""
            INSERT INTO jobs (id, url, title, company_name, company_url, time_update, time_expire, salary, exp, job_level, group_job, job_type, benefit, job_des, job_req, city, address, web)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            item["id"],
            item["url"],
            item["title"],
            item["company_name"],
            item["company_url"],
            item["time_update"],
            item["time_expire"],
            item["salary"],
            item["exp"],
            item["job_level"],
            item["group_job"],
            item["job_type"],
            item["benefit"],
            item["job_des"],
            item["job_req"],
            item["city"],
            item["address"],
            item["web"]
        ))

        # Commit để lưu dữ liệu vào database
        self.conn.commit()
        return item


    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()

class DatabaseConnector:
    def __init__(self, server, database):
        self.server = server
        self.database = database

    def connect(self):
        return pyodbc.connect(
            'DRIVER={SQL Server};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            'Trusted_Connection=yes;'
        )

    def get_links_from_database(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """
        SELECT url 
        FROM jobs WITH (INDEX(IX_jobs_url))
        """
        cursor.execute(query)

        list_url_in_db = [row[0] for row in cursor.fetchall()]

        cursor.close()
        connection.close()

        return list_url_in_db
    
    def get_count_url(self):
        connection = self.connect()
        cursor = connection.cursor()

        query = """
        SELECT COUNT(*) 
    FROM jobs WITH (INDEX(IX_jobs_url))

        """
        cursor.execute(query)

        # Lấy số lượng bản ghi
        record_count = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return record_count


    