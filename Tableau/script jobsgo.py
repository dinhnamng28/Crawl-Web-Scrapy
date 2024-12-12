import unidecode

import logging

# Cấu hình logging để ghi vào file với mã hóa UTF-8
logging.basicConfig(filename='app3.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    encoding='utf-8')


mapping = {
    'Điện/Điện Tử/Điện Lạnh' : 'Kỹ Thuật',
    'Truyền Thông/PR/Quảng Cáo' :'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Bán Sỉ/Bán Lẻ/Cửa Hàng':'Bán Hàng/Kinh Doanh',
    'Nhà Hàng/Khách Sạn' : 'Nhà Hàng - Khách Sạn/Du Lịch',
    'An Toàn Lao Động': 'Khác',
    'Giáo Dục/Đào Tạo': 'Giáo Dục',
    'Sản Xuất/Lắp Ráp/Chế Biến':'Sản Xuất',
    'Dệt May/Da Giày':'Dệt May/Da Giày',
    'Hóa Sinh': 'Khoa Học & Kỹ Thuật',
    'IT Phần Mềm': 'Công Nghệ Thông Tin/Viễn Thông',
    'Kinh Doanh/Bán Hàng':'Bán Hàng/Kinh Doanh',
    'Đấu Thầu/Dự Án': 'Bất Động Sản',
    'Cơ Khí/Ô Tô/Tự Động Hóa' : 'Khoa Học & Kỹ Thuật',
    'Biên Phiên Dịch': 'Biên Phiên Dịch',
    'In Ấn/Chế Bản' : 'Nghệ Thuật, Truyền Thông/In Ấn/Xuất Bản',
    'Nông/Lâm/Ngư Nghiệp': 'Nông/Lâm/Ngư Nghiệp',
    'Chăm Sóc Khách Hàng' : 'Dịch Vụ Khách Hàng',
    'Vận Hành/Bảo Trì/Bảo Dưỡng' : 'Kỹ Thuật',
    'IT Phần Cứng': 'Công Nghệ Thông Tin/Viễn Thông',
    'Nhân Sự': 'Nhân Sự/Tuyển Dụng',
    'Xuất Nhập Khẩu':'Hậu Cần/Xuất Nhập Khẩu/Kho Bãi',
    'Spa/Làm Đẹp':'Dịch Vụ Khách Hàng',
    'Viễn Thông': 'Công Nghệ Thông Tin/Viễn Thông',
    'Kế Toán/Kiểm Toán': 'Kế Toán/Kiểm Toán',
    'Luật/Pháp Chế':'Pháp Lý',
    'Truyền Hình/Báo Chí' : 'Truyền Hình/Báo Chí',
    'Khoa Học/Kỹ Thuật' : 'Khoa Học & Kỹ Thuật',
    'Thiết Kế': 'Thiết Kế',
    'Hành Chính/Văn Phòng': 'Hành Chính Văn Phòng',
    'Bảo Hiểm': 'Bảo Hiểm',
    'Y Tế':'Y Tế/Chăm Sóc Sức Khỏe',
    'Tài Chính/Ngân Hàng':'Ngân Hàng & Dịch Vụ Tài Chính',
    'Kiến Trúc/Nội Thất': 'Kiến Trúc/Xây Dựng',
    'Kho Vận': 'Hậu Cần/Xuất Nhập Khẩu/Kho Bãi',
    'Thu Mua': 'Kinh Doanh',
    'Dược Phẩm/Mỹ Phẩm': 'Dược',
    'Marketing':'Tiếp Thị, Quảng Cáo/Truyền Thông',
    'Lao Động Phổ Thông':'Khác',
    'Bất Động Sản':'Bất Động Sản',
    'Mỏ/Địa Chất': "Khác",
    'Du Lịch': 'Nhà Hàng - Khách Sạn/Du Lịch',
    'Môi Trường': 'Khác',
    'Xây Dựng': 'Kiến Trúc/Xây Dựng',
    'Quản Lý': 'Ceo & General Management',
    'Sáng Tạo/Nghệ Thuật': 'Nghệ Thuật, Truyền Thông/In Ấn/Xuất Bản'
}

mapping_job_level = {
    'Giám Đốc Và Cấp Cao Hơn' : 'Giám Đốc',
    'Mới Tốt Nghiệp/Thực Tập Sinh' : 'Mới Tốt Nghiệp',
    'Nhân Viên' : 'Nhân Viên',
    'Nhân Viên/Chuyên Viên' : 'Nhân Viên',
    'Thực Tập Sinh' : 'Thực Tập Sinh',
    'Trường Nhóm/Trưởng Phòng' : 'Trưởng Nhóm/Trưởng Phòng'
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

