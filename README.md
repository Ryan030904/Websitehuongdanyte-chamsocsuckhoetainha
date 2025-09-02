# HealthFirst - Hệ Thống Hướng Dẫn Y Tế Tại Nhà

## Mô tả
HealthFirst là nền tảng tư vấn và hướng dẫn chăm sóc sức khỏe tại nhà, hỗ trợ người dùng tự đánh giá sơ bộ triệu chứng và đưa ra quyết định an toàn, đúng lúc.

## Tính năng chính

### 🔐 Hệ thống xác thực
- **Đăng ký/Đăng nhập**: Hỗ trợ email/password
- **Quản lý phiên đăng nhập**: Sử dụng Flask-Login
- **Bảo mật**: Mật khẩu được mã hóa bằng Argon2

### 👤 Hồ sơ cá nhân
- **Thông tin cơ bản**: Tên hiển thị, giới tính, tuổi
- **Chỉ số sức khỏe**: Chiều cao, cân nặng, BMI
- **Tiền sử bệnh**: Lưu trữ thông tin bệnh án, thuốc đang dùng

### 🏥 Đánh giá triệu chứng
- **Phân tích thông minh**: Dựa trên quy tắc y tế chuẩn
- **Khuyến nghị cá nhân hóa**: Tùy theo thông tin sức khỏe người dùng
- **Phân loại ưu tiên**: Từ tự chăm sóc tại nhà đến cấp cứu

### 📚 Tài liệu y tế
- **Chủ đề đa dạng**: Hô hấp, tiêu hóa, da liễu, sốt trẻ em...
- **Nguồn tin cậy**: WHO, Bộ Y tế Việt Nam

## Cài đặt và chạy

### 1. Yêu cầu hệ thống
- Python 3.8+
- pip (Python package manager)

### 2. Cài đặt dependencies
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
# Chạy server
python run.py
```

Ứng dụng sẽ chạy tại: http://localhost:5000

## Cấu trúc dự án

```
healthfirst_web/
├── app.py                 # Flask application factory
├── config.py             # Cấu hình ứng dụng
├── models.py             # Các model database
├── routes.py             # Định tuyến
├── utils.py              # Tiện ích và logic nghiệp vụ
├── run.py               # Khởi chạy ứng dụng
├── requirements.txt      # Dependencies
├── data/                # Dữ liệu y tế
├── static/              # Tài nguyên tĩnh
├── templates/           # HTML templates
└── instance/            # Database và cấu hình
```

## Sử dụng

### Người dùng mới
1. Truy cập trang chủ
2. Click "Đăng nhập" → "Đăng ký"
3. Nhập email và mật khẩu
4. Sau khi đăng ký thành công, cập nhật thông tin cá nhân

### Đánh giá triệu chứng
1. Đăng nhập vào hệ thống
2. Cập nhật thông tin sức khỏe cá nhân
3. Mô tả triệu chứng và số ngày bị bệnh
4. Nhận kết quả phân tích và khuyến nghị

### Admin Dashboard
- **Truy cập**: Sau khi đăng nhập admin, truy cập `/admin`
- **Email**: admin@healthfirst.com
- **Mật khẩu**: admin123
- **Tính năng**:
  - Quản lý người dùng và tài khoản
  - Theo dõi đánh giá sức khỏe
  - Xử lý tin nhắn liên hệ từ người dùng
  - Thống kê hệ thống và xuất báo cáo
- **Xem chi tiết**: [ADMIN_README.md](ADMIN_README.md)

## Bảo mật

- **Mã hóa mật khẩu**: Sử dụng Argon2
- **Phiên đăng nhập**: Quản lý bằng Flask-Login
- **CSRF Protection**: Bảo vệ khỏi tấn công CSRF
- **Validation**: Kiểm tra dữ liệu đầu vào

## Lưu ý quan trọng

⚠️ **HealthFirst chỉ là công cụ hỗ trợ tham khảo, không thay thế chẩn đoán hay điều trị của bác sĩ.**

**Khi có dấu hiệu nguy hiểm:**
- Khó thở, đau ngực dữ dội
- Lơ mơ, co giật, tím tái
- Chảy máu không cầm, yếu liệt đột ngột

**Hãy gọi cấp cứu 115 hoặc đến cơ sở y tế gần nhất ngay lập tức!**

## License

© 2024 HealthFirst. Tất cả quyền được bảo lưu.

---

**HealthFirst - Đồng hành cùng sức khỏe của bạn! 💙**

