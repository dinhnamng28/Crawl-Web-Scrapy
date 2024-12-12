import scrapy
from unidecode import unidecode
from viecoiscraper.items import JobItem
from viecoiscraper.pipelines import DatabaseConnector
from datetime import datetime, timedelta

class ViecoispiderSpider(scrapy.Spider):
    name = "viecoispider"
    #allowed_domains = ["viecoi.vn"]
    start_urls = ["https://viecoi.vn/tim-viec/all.html"]

    custom_settings = {
    'FEEDS': {
        'viecoi.json': {'format': 'json', 'overwrite': True, 'encoding': 'utf-8'},
    }
    }

    def parse(self, response):
        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="viecoi_stg")
        list_url_in_db = connector.get_links_from_database()

        jobs = response.xpath("//div[contains(@class, 'jobs-info grid-job')]")

        for job in jobs:
            job_url = job.xpath(".//h2[contains(@class, 'title-jobs')]/a/@href").get()

            if job_url and job_url not in list_url_in_db:
                yield response.follow(job_url, callback=self.parse_job_page)
            
        next_page_url = response.xpath("//a[@title='nextPage']/@href").get()
        if next_page_url:
            yield response.follow(next_page_url,callback=self.parse)

    def parse_job_page(self, response):
        job_item = JobItem()

        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="viecoi_stg")
        count = connector.get_count_url()

        job_item['id'] = "vo" + str(count)

        url = response.url
        title = response.xpath("//h1[contains(@class,'title-jobs-home')]/text()").get()
        company_name = response.xpath("//ul[@class='ul-sub-detail']//li[1]//div[@class='d-table-cell d-table-padding']/a/text()").get()
        
        company_url = response.xpath("//ul[@class='ul-sub-detail']//li[1]//div[@class='d-table-cell d-table-padding']/a/@href").get()
        
        time_update = datetime.now()
        time_update = time_update.strftime("%d/%m/%Y")
        time_expire = response.xpath("//li[.//b[contains(text(), 'Hạn nộp')]]//div[@class='d-table-cell d-table-padding']/text()").get()

        # Kiểm tra và xử lý giá trị của time_expire
        if time_expire:
            try:
                time_expire = time_expire.strip()
                time_expire = datetime.strptime(time_expire, "%Y-%m-%d")
            except ValueError:
                time_expire = datetime.now() + timedelta(days=30)

        
        salary = response.xpath("//div[@class='col-xs-12 position_title_job']//div[@class='div-salary']//div[@class='col-xs-12 color-orange px-0'][i[@class='fa fa-usd']]/text()[2]").get().strip()
        try:
            if salary:
                salary = salary.replace("VNĐ","").replace(",","").replace(" ","")
                min_salary, max_salary = salary.split('-')
                min_salary = float(min_salary) / 25000  
                max_salary = float(max_salary) / 25000  
                salary = (min_salary+ max_salary)/2  
            else:
                salary = 0
        except ValueError:
            salary = 0

        exp_str = response.xpath("//li[.//b[contains(text(), 'Kinh nghiệm')]]//div[@class='d-table-cell d-table-padding']/a/text()").get()
        try:
            if exp_str is not None:  # Kiểm tra nếu exp không phải là None
                if 'Từ' in exp:
                    exp_split = exp_str.split()
    
                    exp = next((x for x in exp_split if x.isdigit()), None)
                elif "Không yêu cầu kinh nghiệm" in exp:
                    exp = 0
                else:
                    exp = 0 
        except Exception as e:  
            exp = 0
        
        job_level = response.xpath("//li[.//b[contains(text(), 'Vị trí')]]//div[@class='d-table-cell d-table-padding']/a/text()").get()
        if job_level:
            job_level = job_level.strip()
        else:
            job_level = 'Nhân viên'

        group_job = response.xpath("//b[contains(text(),'Lĩnh vực')]/ancestor::li//a[1]/text()").get()

        if group_job:
            group_job = group_job.strip()
        else:
            group_job = "Not Show"

        job_type = response.xpath("//b[contains(text(),'Lĩnh vực')]/ancestor::li//a/text()").getall()
        if job_type:
            job_type = ', '.join(job.strip() for job in job_type)  # Nối các giá trị lại với nhau bằng dấu phẩy và loại bỏ khoảng trắng
        else:
            job_type = "Not Show"  # Nếu không có giá trị nào, gán là "Not Show"

        benefits = response.xpath("//div[@id='prf']//a[contains(@class, 'cp-tag')]/text()").getall()
        benefits_cleaned = [benefit.strip() for benefit in benefits]
        benefit = '. '.join(benefits_cleaned)

        job_description = response.xpath("//strong[contains(text(), 'Quyền lợi')]/following-sibling::text()").getall()
        job_description = [desc.strip() for desc in job_description if desc.strip()]
        job_des = ', '.join(job_description)

        job_requirements = response.xpath(".//div[contains(@class, 'widget-header')]//h3/a[contains(text(), 'Kỹ năng')]/following::div[contains(@class, 'spacing_tag')]//a[contains(@class, 'cp-tag')]/text()").getall()
        job_requirement = [desc.strip() for desc in job_requirements if desc.strip()]
        job_req = ', '.join(job_requirement)

        city = response.xpath("//li[contains(., 'Nơi làm việc')]/div[@class='d-table-cell d-table-padding']/a/text()").get()
        if city:
            city = city.replace('Việc làm ', '').strip()
            city = unidecode(city)  # loại bỏ dấu

        address = response.xpath("//strong[contains(text(), 'Địa điểm')]/following-sibling::text()[normalize-space()]").get()
        if address:
            job_item['address'] = address.replace("\n", "").replace("  ","")
        else:
            job_item['address'] = 'Not Show'
        
        job_item['url'] = url
        job_item['title'] = title
        job_item['company_name'] = company_name
        job_item['company_url'] = company_url
        job_item['time_update'] = time_update
        job_item['time_expire'] = time_expire
        job_item['salary'] = salary
        job_item['exp'] = exp
        job_item['job_level'] = job_level
        job_item['group_job'] = group_job
        job_item['job_type'] = job_type
        job_item['benefit'] = benefit
        job_item['job_des'] = job_des
        job_item['job_req'] = job_req
        job_item['city'] = city
        job_item['address'] = address
        job_item['web'] = 'Jobsgo'

        yield job_item

