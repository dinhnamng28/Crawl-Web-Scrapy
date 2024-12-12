import unidecode
import pandas as pd

import logging

# Cấu hình logging để ghi vào file với mã hóa UTF-8
logging.basicConfig(filename='app1.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    encoding='utf-8')




mapping = {
    'An Ninh / Bảo Vệ' : 'Nhân Sự/Tuyển Dụng',
    'An Toàn Lao Động' : 'Bảo Hiểm',
    'Bán Hàng / Kinh Doanh' : 'Bán Hàng/Kinh Doanh',
    'Bán Lẻ / Bán Sỉ' : 'Bán Lẻ/Tiêu Dùng',
    'Bảo Hiểm': 'Bảo Hiểm',
    'Bảo Trì / Sửa Chữa': 'Kỹ Thuật',
    'Bất Động Sản' : 'Bất Động Sản',
    'Biên Phiên Dịch' : 'Biên Phiên Dịch',
    'Bưu Chính Viễn Thông' : 'Công Nghệ Thông Tin/Viễn Thông',
    'Chăn Nuôi / Thú Y' : 'Chăn Nuôi/Thú Y',
    'Chứng Khoán' : 'Chứng Khoán',
    'Cntt - Phần Cứng / Mạng' : 'Công Nghệ Thông Tin/Viễn Thông',
   ' Cntt - Phần Mềm' : 'Công Nghệ Thông Tin/Viễn Thông',
    'Cơ Khí / Ô Tô / Tự Động Hóa' : 'Kỹ Thuật',
    'Công Nghệ Sinh Học' : 'Khoa Học & Kỹ Thuật',
    'Công Nghệ Thực Phẩm / Dinh Dưỡng' : 'Y Tế/Chăm Sóc Sức Khỏe',
    'Dầu Khí' : 'Khác',
    'Dệt May / Da Giày / Thời Trang' : 'Dệt May/Da Giày',
    'Dịch Vụ Khách Hàng' : 'Dịch Vụ Khách Hàng',
    'Điện / Điện Tử / Điện Lạnh' : 'Kỹ Thuật',
    'Đồ Gỗ' : 'Khác',
    'Du Lịch' : 'Nhà Hàng - Khách Sạn/Du Lịch',
    'Dược Phẩm' : 'Dược',
    'Giải Trí' : 'Giải Trí',
    'Giáo Dục / Đào Tạo' : 'Giáo Dục',
    'Hàng Gia Dụng / Chăm Sóc Cá Nhân' : 'Bán Lẻ/Tiêu Dùng',
    'Hàng Hải' : 'Vận Tải',
    'Hàng Không' : 'Vận Tải',
    'Hành Chính / Thư Ký' : 'Hành Chính Văn Phòng',
    'Hóa Học' : 'Khoa Học & Kỹ Thuật',
    'In Ấn / Xuất Bản' : 'Nghệ Thuật, Truyền Thông/In Ấn/Xuất Bản',
    'Kế Toán / Kiểm Toán' : 'Kế Toán/Kiểm Toán',
    'Khoáng Sản' : 'Khác',
    'Kiến Trúc' : 'Kiến Trúc/Xây Dựng',
    'Lâm Nghiệp' : 'Nông/Lâm/Ngư Nghiệp',
    'Lao Động Phổ Thông' : 'Khác',
    'Luật / Pháp Lý' : 'Pháp Lý',
    'Mới Tốt Nghiệp / Thực Tập' : 'Khác',
    'Môi Trường' : 'Khác',
    'Mỹ Thuật / Nghệ Thuật / Thiết Kế' : 'Nghệ Thuật, Truyền Thông/In Ấn/Xuất Bản',
    'Ngân Hàng' : 'Ngân Hàng & Dịch Vụ Tài Chính',
    'Ngành Khác' : 'Khác',
    'Nhà Hàng/ Khách Sạn' : 'Nhà Hàng - Khách Sạn/Du Lịch',
    'Nhân Sự' : 'Nhân Sự/Tuyển Dụng',
    'Nội Ngoại Thất' : 'Kiến Trúc/Xây Dựng',
    'Nông Nghiệp' : 'Nông/Lâm/Ngư Nghiệp',
    'Phi Chính Phủ / Phi Lợi Nhuận' : 'Chính Phủ/Phi Lợi Nhuận',
    'Quản Lý Chất Lượng (Qa/Qc)' : 'Khác',
    'Quản Lý Điều Hành' :'Ceo & General Management',
    'Quảng Cáo / Đối Ngoại / Truyền Thông' : 'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Sản Xuất / Vận Hành Sản Xuất' : 'Sản Xuất',
    'Tài Chính / Đầu Tư' : 'Ngân Hàng & Dịch Vụ Tài Chính',
    'Thống Kê' : 'Hành Chính Văn Phòng',
    'Thu Mua / Vật Tư' : 'Kinh Doanh',
    'Thư Viện' : 'Khác',
    'Thực Phẩm & Đồ Uống' : 'Dịch Vụ Ăn Uống',
    'Thủy Lợi' : 'Sản Xuất',
    'Thủy Sản / Hải Sản' : 'Nông/Lâm/Ngư Nghiệp',
    'Tiếp Thị / Marketing' : 'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Tiếp Thị Trực Tuyến' : 'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Tổ Chức Sự Kiện' : 'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Trắc Địa / Địa Chất' : 'Khác',
    'Truyền Hình / Báo Chí / Biên Tập' : 'Truyền Hình/Báo Chí',
    'Tư Vấn' : 'Dịch Vụ Khách Hàng',
    'Vận Chuyển / Giao Nhận /  Kho Vận' : 'Hậu Cần/Xuất Nhập Khẩu/Kho Bãi',
    'Xây Dựng' : 'Kiến Trúc/Xây Dựng',
    'Xuất Nhập Khẩu' : 'Hậu Cần/Xuất Nhập Khẩu/Kho Bãi' ,
    'Y Tế / Chăm Sóc Sức Khỏe' : 'Y Tế/Chăm Sóc Sức Khỏe',
    'Bảo Trì / Sửa Chữa' : 'Kỹ Thuật'
}

mapping_job_level = {
    'Giám Đốc' : 'Giám Đốc',
    'Mới Tốt Nghiệp' : 'Mới Tốt Nghiệp',
    'Nhân Viên' : 'Nhân Viên',
    'Phó Giám Đốc' : 'Phó Giám Đốc',
    'Quản Lý': 'Quản Lý',
    'Sinh Viên/ Thực Tập Sinh' : 'Thực Tập Sinh',
    'Tổng Giám Đốc' : 'Tổng Giám Đốc',
    'Trưởng Nhóm / Giám Sát' : 'Trưởng Nhóm/Trưởng Phòng'
}

provinces_regions = {
    "Vung Trung Du Mien Nui Bac Bo": [
        "Ha Giang", "Cao Bang", "Lang Son", "Bac Giang", "Phu Tho", "Thai Nguyen", "Bac Kan",
        "Tuyen Quang", "Lao Cai", "Yen Bai", "Lai Chau", "Son La", "Dien Bien", "Hoa Binh"
    ],
    "Vung Dong Bang Song Hong": [
        "Ha Noi", "Hai Phong", "Hai Duong", "Hung Yen", "Vinh Phuc", "Bac Ninh", "Thai Binh",
        "Nam Dinh", "Ha Nam", "Ninh Binh", "Quang Ninh"
    ],
    "Vung Bac Trung Bo va Duyen Hai Mien Trung": [
        "Thanh Hoa", "Nghe An", "Ha Tinh", "Quang Binh", "Quang Tri", "Thua Thien Hue", "Da Nang",
        "Quang Nam", "Quang Ngai", "Binh Dinh", "Phu Yen", "Khanh Hoa", "Ninh Thuan", "Binh Thuan"
    ],
    "Vung Tay Nguyen": [
        "Kon Tum", "Gia Lai", "Dak Lak", "Dak Nong", "Lam Dong"
    ],
    "Vung Dong Nam Bo": [
        "Ho Chi Minh", "Dong Nai", "Ba Ria Vung Tau", "Binh Duong", "Binh Phuoc", "Tay Ninh"
    ],
    "Vung Dong Bang Song Cuu Long": [
        "Can Tho", "Long An", "Tien Giang", "Ben Tre", "Tra Vinh", "Vinh Long", "An Giang", "Vinh Phuc",
        "Dong Thap", "Bac Lieu", "Kien Giang", "Soc Trang", "Hau Giang", "Ca Mau", "Bac Lieu"
    ]
}


regions_mien = {
    "Mien Bac": [
        "Ha Giang", "Cao Bang", "Lang Son", "Bac Giang", "Phu Tho", "Thai Nguyen", "Bac Kan",
        "Tuyen Quang", "Lao Cai", "Yen Bai", "Lai Chau", "Son La", "Dien Bien", "Hoa Binh", 
        "Ha Noi", "Hai Phong", "Hai Duong", "Hung Yen", "Vinh Phuc", "Bac Ninh", "Thai Binh",
        "Nam Dinh", "Ha Nam", "Ninh Binh", "Quang Ninh"
    ],
    "Mien Trung": [
        "Thanh Hoa", "Nghe An", "Ha Tinh", "Quang Binh", "Quang Tri", "Thua Thien Hue", "Da Nang",
        "Quang Nam", "Quang Ngai", "Binh Dinh", "Phu Yen", "Khanh Hoa", "Ninh Thuan", "Binh Thuan",
        "Kon Tum", "Gia Lai", "Dak Lak", "Dak Nong", "Lam Dong"
    ],
    "Mien Nam": [
        "Ho Chi Minh", "Dong Nai", "Ba Ria Vung Tau", "Binh Duong", "Binh Phuoc", "Tay Ninh",
        "Can Tho", "Long An", "Tien Giang", "Ben Tre", "Tra Vinh", "Vinh Long", "Vinh Phuc",
        "Bac Lieu", "Kien Giang", "Soc Trang", "Hau Giang", "Ca Mau", "Dong Thap", "An Giang"
    ]
}


city_list = {
    "An Giang", "Ba Ria Vung Tau", "Bac Giang", "Bac Kan", "Bac Lieu", "Bac Ninh",
    "Ben Tre", "Binh Duong", "Binh Dinh", "Binh Phuoc", "Binh Thuan", "Ca Mau",
    "Cao Bang", "Can Tho", "Da Nang", "Dak Lak", "Dak Nong", "Dien Bien", "Dong Nai",
    "Dong Thap", "Gia Lai", "Ha Giang", "Ha Nam", "Ha Noi", "Ha Tinh", "Hai Duong",
    "Hai Phong", "Hau Giang", "Hoa Binh", "Hung Yen", "Khanh Hoa", "Kien Giang",
    "Kon Tum", "Lai Chau", "Lam Dong", "Lang Son", "Lao Cai", "Long An", "Nam Dinh",
    "Nghe An", "Ninh Binh", "Ninh Thuan", "Phu Tho", "Phu Yen", "Quang Binh",
    "Quang Nam", "Quang Ngai", "Quang Ninh", "Quang Tri", "Soc Trang", "Son La",
    "Tay Ninh", "Thai Binh", "Thai Nguyen", "Thanh Hoa", "Thua Thien Hue", "Tien Giang",
    "Ho Chi Minh", "Tra Vinh", "Tuyen Quang", "Vinh Long", "Vinh Phuc", "Yen Bai"
}


def transform(df):
    # Chuyển cột company_name và city thành không dấu
    df['CompanyName'] = df['CompanyName'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)
    df['CityName'] = df['CityName'].apply(lambda x: unidecode.unidecode(x) if isinstance(x, str) else x)

    df['CityName'] = df['CityName'].apply(lambda x: x if x in city_list else 'Khac')

    df['GroupJobName'] = df['GroupJobName'].map(mapping).fillna('Khác')

    df['JobLevelName'] = df['JobLevelName'].map(mapping_job_level).fillna('Khác')

    df['EcoRegion'] = df['CityName'].map(lambda city: next((region for region, provinces in provinces_regions.items() if city in provinces), 'Khac'))

    df['Region'] = df['CityName'].map(lambda city: next((mien for mien, provinces in regions_mien.items() if city in provinces), 'Khac'))

    return df


def get_output_schema():
    return pd.DataFrame({
        'ExpRange':prep_string(),
        'SalaryRange':prep_string(),
        'Address':prep_string(),
        'Benefit':prep_string(),
        'CityName':prep_string(),
        'CompanyName':prep_string(),
        'CompanyURL':prep_string(),
        'Exp':prep_int(),
        'GroupJobName':prep_string(),
        'JobID':prep_string(),
        'JobDes':prep_string(),
        'JobLevelName':prep_string(),
        'JobReq':prep_string(),
        'JobType':prep_string(),
        'Salary':prep_decimal(),
        'TimeExpire':prep_date(),
        'DateID':prep_date(),
        'JobTitle':prep_string(),
        'JobURL':prep_string(),
        'Web':prep_string(),
        'EcoRegion':prep_string(),
        'Region':prep_string()
    })