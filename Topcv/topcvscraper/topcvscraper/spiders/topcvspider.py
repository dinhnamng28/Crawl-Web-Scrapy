import scrapy
from unidecode import unidecode
from topcvscraper.items import JobItem
from topcvscraper.pipelines import DatabaseConnector
from datetime import datetime, timedelta


class TopcvspiderSpider(scrapy.Spider):
    name = "topcvspider"
    #allowed_domains = ["www.topcv.vn"]
    start_urls = ["https://www.topcv.vn/tim-viec-lam-moi-nhat?sba=1"]


    def parse(self, response):
        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="topcv_stg")
        list_url_in_db = connector.get_links_from_database()

        jobs = response.xpath("//div[contains(@class, 'job-item-search-result')]")

        for job in jobs:
            job_url = job.xpath(".//div[@class='title-block']//h3[contains(@class,'title')]/a/@href").get()

            if job_url and job_url not in list_url_in_db:
                yield response.follow(job_url, callback=self.parse_job_page)
            
        next_page_url = response.xpath("//li/a[@rel='next']/@data-href").get()
        if next_page_url:
            yield response.follow(next_page_url,callback=self.parse)
        
    def parse_job_page(self, response):
        job_item = JobItem()

        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="topcv_stg")
        count = connector.get_count_url()

        job_item['id'] = "tcv" + str(count)

        url = response.url
        title = response.xpath("//h1[contains(@class,'job-detail__info--title')]/a/text()").get()
        if title:
            title = title.strip()

        company_name = response.xpath("//h2[@class='company-name-label']/a[@class='name']/text()").get()
        
        company_url = response.xpath("//h2[@class='company-name-label']/a[@class='name']/@href").get()
        
        time_update = datetime.now()
        time_update = time_update.strftime("%d/%m/%Y")

        time_expire = response.xpath("//div[@class='job-detail__info--deadline']/text()[contains(., 'Hạn nộp hồ sơ')]").get()

        # Kiểm tra và xử lý giá trị của time_expire
        if time_expire:
            try:
                time_expire = time_expire.replace("Hạn nộp hồ sơ:","").replace(" ","")
                time_expire = datetime.strptime(time_expire, "%Y-%m-%d")
            except ValueError:
                time_expire = datetime.now() + timedelta(days=30)

        
        salary = response.xpath("//div[contains(text(),'Mức lương')]/following-sibling::div/text()").get()
        try:
            if salary:
                salary = salary.strip()  # Loại bỏ khoảng trắng dư thừa

                # Trường hợp "Thỏa thuận"
                if "Thỏa thuận" in salary:
                    salary = 0
                
                # Trường hợp lương tính bằng "triệu"
                elif "triệu" in salary:
                    salary = salary.replace("triệu", "").replace(",", "").strip()
                    if "Tới" in salary or "Trên" in salary:
                        salary_value = float(salary.split(" ")[1])
                        salary = salary_value * 1000000 / 25000
                    elif "-" in salary:
                        min_salary, max_salary = salary.split('-')
                        min_salary = float(min_salary.strip()) * 1000000 / 25000
                        max_salary = float(max_salary.strip()) * 1000000 / 25000
                        salary = (min_salary + max_salary) / 2

                # Trường hợp lương tính bằng "USD"
                elif "USD" in salary:
                    salary = salary.replace("USD", "").replace(",", "").strip()
                    if "Tới" in salary or "Trên" in salary:
                        salary_value = float(salary.split(" ")[1])
                        salary = salary_value
                    elif "-" in salary:
                        min_salary, max_salary = salary.split('-')
                        min_salary = float(min_salary.strip())
                        max_salary = float(max_salary.strip())
                        salary = (min_salary + max_salary) / 2

                else:
                    salary = 0
            else:
                salary = 0

        except:
            salary = 0

        exp = response.xpath("//div[contains(text(),'Kinh nghiệm')]/following-sibling::div/text()").get()
        try:
            if exp is not None:  # Kiểm tra nếu exp không phải là None
                if "Không yêu cầu kinh nghiệm" in exp:
                    exp = 0
                else:
                    exp = exp.split()
    
                    exp = next((x for x in exp if x.isdigit()), 0)
        except Exception as e:  
            exp = 0
        
        job_level = response.xpath("//div[contains(text(),'Cấp bậc')]/following-sibling::div/text()").get()
        if job_level:
            job_level = job_level.strip()
        else:
            job_level = 'Nhân viên'

        group_job = response.xpath("//div[contains(text(), 'Danh mục Nghề liên quan')]/following-sibling::div//a[@class='box-category-tag'][1]/text()").get()

        if group_job:
            group_job = group_job.strip()
        else:
            group_job = "Not Show"

        job_type = response.xpath("//div[contains(text(), 'Danh mục Nghề liên quan')]/following-sibling::div//a[@class='box-category-tag']/text()").getall()
        if job_type:
            job_type = ', '.join(job.strip() for job in job_type)  # Nối các giá trị lại với nhau bằng dấu phẩy và loại bỏ khoảng trắng
        else:
            job_type = "Not Show"  # Nếu không có giá trị nào, gán là "Not Show"

        benefits = response.xpath("//div[@class='job-description__item']//h3[text()='Quyền lợi']/following-sibling::div[@class='job-description__item--content']//p/text()").getall()
        benefits_cleaned = [benefit.strip() for benefit in benefits]
        benefit = '. '.join(benefits_cleaned)

        job_description = response.xpath("//div[@class='job-description__item']//h3[text()='Mô tả công việc']/following-sibling::div[@class='job-description__item--content']//p/text()").getall()
        job_description = [desc.strip() for desc in job_description if desc.strip()]
        job_des = ', '.join(job_description)

        job_requirements = response.xpath("//div[@class='job-description__item']//h3[text()='Yêu cầu ứng viên']/following-sibling::div[@class='job-description__item--content']//p/text()").getall()
        job_requirement = [desc.strip() for desc in job_requirements if desc.strip()]
        job_req = ', '.join(job_requirement)

        city = response.xpath("//div[contains(text(),'Địa điểm')]/following-sibling::div/text()").get()
        if city:
            city = city.strip()
            city = unidecode(city)  # loại bỏ dấu

        address = response.xpath("//div[@class='job-description__item']//h3[text()='Địa điểm làm việc']/following-sibling::div[@class='job-description__item--content']//div/text()").get()
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
        job_item['web'] = 'TopCV'

        yield job_item


