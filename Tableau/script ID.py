import pandas as pd

city_id = {
    "An Giang": 1, "Ba Ria Vung Tau": 2, "Bac Giang": 3, "Bac Kan": 4, "Bac Lieu": 5,
    "Bac Ninh": 6, "Ben Tre": 7, "Binh Duong": 8, "Binh Dinh": 9, "Binh Phuoc": 10,
    "Binh Thuan": 11, "Ca Mau": 12, "Cao Bang": 13, "Can Tho": 14, "Da Nang": 15,
    "Dak Lak": 16, "Dak Nong": 17, "Dien Bien": 18, "Dong Nai": 19, "Dong Thap": 20,
    "Gia Lai": 21, "Ha Giang": 22, "Ha Nam": 23, "Ha Noi": 24, "Ha Tinh": 25,
    "Hai Duong": 26, "Hai Phong": 27, "Hau Giang": 28, "Hoa Binh": 29, "Hung Yen": 30,
    "Khanh Hoa": 31, "Kien Giang": 32, "Kon Tum": 33, "Lai Chau": 34, "Lam Dong": 35,
    "Lang Son": 36, "Lao Cai": 37, "Long An": 38, "Nam Dinh": 39, "Nghe An": 40,
    "Ninh Binh": 41, "Ninh Thuan": 42, "Phu Tho": 43, "Phu Yen": 44, "Quang Binh": 45,
    "Quang Nam": 46, "Quang Ngai": 47, "Quang Ninh": 48, "Quang Tri": 49, "Soc Trang": 50,
    "Son La": 51, "Tay Ninh": 52, "Thai Binh": 53, "Thai Nguyen": 54, "Thanh Hoa": 55,
    "Thua Thien Hue": 56, "Tien Giang": 57, "Ho Chi Minh": 58, "Tra Vinh": 59,
    "Tuyen Quang": 60, "Vinh Long": 61, "Vinh Phuc": 62, "Yen Bai": 63, "Khac": 0
}


web_id  = {
    'CareerViet' : 1,
    'Jobsgo' : 2,
    'VietNamWork' : 3
}

group_job_id = {
    'Bán Hàng/Kinh Doanh' : 1,
    'Bán Lẻ/Tiêu Dùng' :2,
    'Bảo Hiểm':3,
    'Bất Động Sản':4,
    'Biên Phiên Dịch':5,
    'Ceo & General Management':6,
    'Chăn Nuôi/Thú Y':7,
    'Chính Phủ/Phi Lợi Nhuận':8,
    'Chứng Khoán':9,
    'Công Nghệ Thông Tin/Viễn Thông':10,
    'Dệt May/Da Giày':11,
    'Dịch Vụ Ăn Uống':12,
    'Dịch Vụ Khách Hàng':13,
    'Dược':14,
    'Giải Trí':15,
    'Giáo Dục':16,
    'Hành Chính ăn Phòng':17,
    'Hậu Cần/Xuất Nhập Khẩu/Kho Bãi':18,
    'Kế Toán/Kiểm Toán':19,
    'Khác':20,
    'Khoa Học & Kỹ Thuật':21,
    'Kiến Trúc/Xây Dựng':22,
    'Kinh Doanh':23,
    'Kỹ Thuật':24,
    'Ngân Hàng & Dịch Vụ Tài Chính':25,
    'Nghệ Thuật Truyền Thông/In Ấn/Xuất Bản':26,
    'Nhà Hàng - Khách Sạn/Du Lịch':27,
    'Nhân Sự/Tuyển Dụng':28,
    'Nông/Lâm/Ngư Nghiệp':29,
    'Pháp Lý':30,
    'Sản Xuất':31,
    'Thiết Kế':32,
    'Tiếp Thị Quảng Cáo/Truyền Thông':33,
    'Truyền Hình/Báo Chí':34,
    'Vận Tải':35,
    'Y Tế/Chăm Sóc Sức Khỏe':36,

}

job_level_id = {
    'Giám Đốc':1,
    'Mới Tốt Nghiệp' :2,
    'Nhân Viên':3,
    'Thực Tập Sinh' : 4,
    'Tổng Giám Đốc' : 5,
    'Trưởng Nhóm/Trưởng Phòng':6,
    'Phó Giám Đốc' : 7,
    'Quản Lý':8
}

salary_range_id = {
    '0-300':1,
    '300-500':2,
    '500-1000':3,
    '1000-2000':4,
    '2000-5000':5,
    '>5000':6,
    'DEAL':7
}

exp_range_id = {
    '0-1 year':1,
    '1-2 year':2,
    '2-5 year':3,
    '5-10 year' : 4,
    '>10 year': 5
}

# Hàm chuyển từ tiếng Việt có dấu sang không dấu
def create_id(df):
    df['CityID'] = df['CityID'].map(city_id).fillna(0)
    df['WebID'] = df['WebID'].map(web_id).fillna(0)
    df['GroupJobID'] = df['GroupJobID'].map(group_job_id).fillna(0)
    df['JobLevelID'] = df['JobLevelID'].map(job_level_id).fillna(0)
    df['SalaryRangeID'] = df['SalaryRangeID'].map(salary_range_id).fillna(0)
    df['ExpRangeID'] = df['ExpRangeID'].map(exp_range_id).fillna(0)

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
        'Region':prep_string(),
        'CityID':prep_int(),
        'WebID':prep_int(),
        'GroupJobID':prep_int(),
        'JobLevelID':prep_int(),
        'SalaryRangeID':prep_int(),
        'ExpRangeID':prep_int(),
    })

