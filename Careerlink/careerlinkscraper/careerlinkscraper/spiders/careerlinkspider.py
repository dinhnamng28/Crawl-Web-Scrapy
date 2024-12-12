import scrapy
from careerlinkscraper.items import JobItem
from careerlinkscraper.pipelines import DatabaseConnector

class CareerlinkspiderSpider(scrapy.Spider):
    name = "careerlinkspider"
    #allowed_domains = ["www.careerlink.vn"]
    start_urls = ["https://www.careerlink.vn/vieclam/list"]


    def parse(self, response):
        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="careerlink_stg")
        list_url_in_db = connector.get_links_from_database()
        jobs = response.xpath("//li[contains(@class, 'list-group-item job-item')]")

        for job in jobs:
            job_url = job.xpath(".//a[contains(@class, 'job-link clickable-outside')]/@href").get()

            if "https://www.careerlink.vn/" not in job_url :
                job_url = "https://www.careerlink.vn/"+job_url

            if job_url and job_url not in list_url_in_db:
                yield response.follow(job_url, callback = self.parse_job_page)
        
        next_page_url = response.xpath("//a[@rel='next'][@class='page-link d-none d-md-block']/@href").get()
        if next_page_url and "https://www.careerlink.vn/" not in next_page_url:
            next_page_url = "https://www.careerlink.vn/"+next_page_url

        yield response.follow(next_page_url,callback=self.parse)
        
    def parse_job_page(self, response):
        job_item = JobItem()

        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="careerlink_stg")
        count = connector.get_count_url()

        job_item['id'] = "careerlink" + str(count)

        url = response.url
        title = response.xpath("//h1[contains(@class, 'job-title')]/text()").get().strip()
        company_name = response.xpath("//p[contains(@class, 'org-name mb-2')]/a/span/text()").get().strip()
        
        company_url = response.xpath("//p[contains(@class, 'org-name mb-2')]/a/@href").get()
        if company_url and "https://www.careerlink.vn/" not in company_url :
            company_url = "https://www.careerlink.vn/"+ company_url
        
        time_update = response.xpath("//span[contains(text(), 'Ngày đăng tuyển')]/following-sibling::text()").get()
        time_expire_str = response.xpath("//span[contains(text(), 'Hết hạn trong')]/b/text()").get()

        if time_update:
            time_update = time_update.strip()
        if time_expire_str:
            time_expire = int(next(part for part in time_expire_str.split() if part.isdigit()))

        salary = response.xpath("//span[contains(@class, 'text-primary')]/text()").get()
        try:
            if salary:
                if 'Thương lượng' in salary or 'Cạnh tranh' in salary:
                    salary = 0
                elif 'Trên' in salary:
                    salary = salary.replace(",","").replace("triệu","").replace("Trên","").strip()
                    salary = float(salary)*1000000/25000
                else:
                    min_salary, max_salary = salary.split('-')
                    min_salary = min_salary.replace(",", "").replace("triệu", "").strip()
                    max_salary = max_salary.replace(",", "").replace("triệu", "").strip()
                    min_salary = float(min_salary) * 1000000 / 25000  
                    max_salary = float(max_salary) *1000000/ 25000  
                    salary = (min_salary+ max_salary)/2  
            else:
                salary = 0
        except:
            salary = 0

        exp = response.xpath("//div[@class='d-flex align-items-center mb-2' and not(@id)]/span/text()").get()
        try:
            if exp:
                exp = exp.replace(" ","").split('-')[0]
            else:
                exp = 0
        except:
            exp = 0
        
        job_level = response.xpath("//div[contains(text(), 'Cấp bậc')]/following-sibling::div[@class='font-weight-bolder']/text()").get()
        if job_level:
            job_level = job_level.replace("\n","")

        group_job = response.xpath("//div[contains(text(), 'Ngành nghề')]/following-sibling::div[@class='font-weight-bolder']/a[1]/span/text()").get()

        if group_job:
            group_job = group_job.replace("\n","")

        job_type_list = response.xpath("//div[contains(text(), 'Ngành nghề')]/following-sibling::div[@class='font-weight-bolder']/a/span/text()").getall()
        job_type = ', '.join(job_type_list).replace("\n","")


        benefits = response.xpath("//div[@id='section-job-benefits']//span[not(ancestor::h5)][not(ancestor::div[@class='image-icon'])]/text()").getall()
        benefits_cleaned = [benefit.strip() for benefit in benefits]
        benefit = '. '.join(benefits_cleaned)

        job_description = response.xpath("//div[@id='section-job-description']//div[@class='rich-text-content']/p/text()").getall()
        job_description = [desc.strip() for desc in job_description if desc.strip()]
        job_des = ', '.join(job_description)

        job_requirements = response.xpath("//div[@id='section-job-skills']//div[@class='raw-content rich-text-content']/p/text()").getall()
        job_requirement = [desc.strip() for desc in job_requirements if desc.strip()]
        job_req = ', '.join(job_requirement)

        city = response.xpath("//a[@class='text-reset font-weight-bold']/text()").get()
        if city:
            city = city.strip()

        address = response.xpath("//span[@class='mr-1']/text()").get()
        if address:
            address = address.replace("\n","")
        else:
            address = 'Not Show'
        
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
        job_item['web'] = 'CareerLink'

        yield job_item
