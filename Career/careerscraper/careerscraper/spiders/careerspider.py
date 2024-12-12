import scrapy
from careerscraper.items import JobItem
from careerscraper.pipelines import DatabaseConnector
from datetime import datetime

class CareerspiderSpider(scrapy.Spider):
    name = "careerspider"
    #allowed_domains = ["careerviet.vn"]
    start_urls = ["https://careerviet.vn/viec-lam/tat-ca-viec-lam-vi.html"]

    def parse(self, response):
        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="career_stg")
        list_url_in_db = connector.get_links_from_database()
        jobs = response.xpath("//div[contains(@class, 'job-item')]")

        for job in jobs:
            job_url = job.xpath(".//a[contains(@class, 'job_link')]/@href").get()
            
            if "en/search-job" in job_url:
                job_url = job_url.replace("en/search-job","vi/tim-viec-lam")

            if job_url and job_url not in list_url_in_db:
                yield response.follow(job_url, callback = self.parse_job_page)
        
        next_page_url = response.xpath("//li[@class='next-page']/a/@href").get()

        yield response.follow(next_page_url,callback=self.parse)
    
    def parse_job_page(self, response):
        job_item = JobItem()

        connector = DatabaseConnector(server="DinhNamNguyen\DinhNam", database="career_stg")
        count = connector.get_count_url()

        job_item['id'] = "career" + str(count)

        job_item['url'] = response.url
        job_item['title'] = response.xpath("//h1[contains(@class, 'title')]/text()").get()
        job_item['company_name'] = response.xpath("//a[contains(@class,'employer job-company-name')]/text()").get()
        job_item['company_url'] = response.xpath("//a[contains(@class,'employer job-company-name')]/@href").get()

        time_update = response.xpath("//li/strong[contains(text(), 'Ngày cập nhật')]/following-sibling::p/text()").get()
        time_expire= response.xpath("//li/strong[contains(text(), 'Hết hạn nộp')]/following-sibling::p/text()").get()

        if time_update:
            time_update = datetime.strptime(time_update.strip(), "%d/%m/%Y")
        else:
            time_update = datetime.now()
        
        if time_expire:
            time_expire = datetime.strptime(time_expire.strip(), "%d/%m/%Y")
        else:
            time_expire = datetime.now()
        
        job_item['time_update'] = time_update
        job_item['time_expire'] = time_expire

        salary = response.xpath("//li/strong[contains(text(), 'Lương')]/following-sibling::p/text()").get()
        try:
            if 'Cạnh tranh' in salary:
                salary = 0
            elif 'Lên đến' in salary or 'Trên' in salary:
                parts = salary.split()
                for part in parts:
                    if part.isdigit():  # Kiểm tra nếu phần tử là số
                        salary = float(part) * 1000000/25000  # Chuyển thành đơn vị VND
            elif '-' in salary:
                parts = salary.split('-')

                # Lấy phần tử đầu và cuối, loại bỏ 'Mil' và khoảng trắng, rồi chuyển thành số nguyên
                min_salary = float(parts[0].strip().replace("Tr", "").strip()) * 1000000/25000
                max_salary = float(parts[1].strip().replace("Tr", "").replace("VND", "").strip()) * 1000000/25000

                salary = (min_salary + max_salary) / 2
            else:
                salary = 0
        except:
            salary = 0
            
        job_item['salary'] = salary

        exp = response.xpath("//li/strong[contains(text(), 'Kinh nghiệm')]/following-sibling::p/text()").get()
        try:
            if exp:
                # Xóa ký tự không cần thiết và khoảng trắng thừa
                exp = exp.replace("\r", "").replace("\n", "").strip()
                exp = " ".join(exp.split())
                
                # Tách chuỗi theo khoảng trắng và lấy số đầu tiên
                parts = exp.split()
                number_part = next((int(part) for part in parts if part.isdigit()), 0)
                exp = number_part
            else:
                exp = 0  # Giá trị mặc định nếu không có kinh nghiệm
        except:
            exp = 0

        job_item['exp'] = exp

        job_item['job_level'] = response.xpath("//li/strong[contains(text(), 'Cấp bậc')]/following-sibling::p/text()").get()

        job_item['group_job'] = response.xpath("//li[strong[contains(., 'Ngành nghề')]]/p/a[1]/text()").get().replace("\n","").strip()
        job_type = response.xpath("//li[strong[normalize-space()='Ngành nghề']]/p/a/text()").getall()

        if job_type:
            job_type = ', '.join(job.strip() for job in job_type)

        job_item['job_type'] = job_type

        benefits = response.xpath("//div[@class='detail-row']//ul[@class='welfare-list']/li/text()").getall()
        benefits = [benefit.strip() for benefit in benefits if benefit.strip()]
        job_item['benefit'] = ', '.join(benefits)

        job_description = response.xpath("//div[contains(@class, 'detail-row reset-bullet') and h2[contains(text(), 'Mô tả Công việc')]]//p/text()").getall()
        job_description = [desc.strip() for desc in job_description if desc.strip()]
        job_item['job_des'] = ', '.join(job_description)

        job_req = response.xpath("//div[contains(@class, 'detail-row reset-bullet') and h2[contains(text(), 'Yêu Cầu Công Việc')]]//p/text()").getall()
        job_req = [desc.strip() for desc in job_req if desc.strip()]
        job_item['job_req'] = ', '.join(job_req)  # Chỉnh sửa ở đây để lấy job_req từ job_req thay vì job_description

        job_item['city'] = response.xpath("//div[@class='map']/p/a/text()").get()
        address = response.xpath("//div[@class='place-name']/span/text()[normalize-space()]").get()

        if address:
            job_item['address'] = address.strip()
        else:
            job_item['address'] = 'Not Show'


        job_item['web'] = 'CareerViet'

        yield job_item
