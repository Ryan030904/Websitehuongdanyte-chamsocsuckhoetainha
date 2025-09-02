# HƯỚNG DẪN CHẠY ỨNG DỤNG WEB Y TẾ

## Yêu cầu hệ thống
- Python 3.8 trở lên
- Windows 10/11 (hoặc Linux/macOS)
- Kết nối internet để tải thư viện

## Cách 1: Chạy nhanh trên Windows (Khuyến nghị)

### Bước 1: Mở Command Prompt
- Nhấn `Win + R`, gõ `cmd` và nhấn Enter
- Hoặc mở PowerShell

### Bước 2: Di chuyển đến thư mục dự án
```cmd
cd "D:\website hướng dẫn y tế & chăm sóc sức khỏe tại nhà"
```

### Bước 3: Chạy script tự động (Khuyến nghị)
```cmd
start_admin_fixed.bat
```

Hoặc script cũ:
```cmd
start_admin.bat
```

Script `start_admin_fixed.bat` sẽ tự động:
- Tạo môi trường ảo Python
- Cài đặt các thư viện cần thiết
- **Sửa lỗi tài khoản admin** (quan trọng!)
- Kiểm tra kết nối Firebase (tùy chọn)
- Khởi động web server

Script `start_admin.bat` (cũ):
- Tạo môi trường ảo Python
- Cài đặt các thư viện cần thiết
- Tạo tài khoản admin mặc định
- Khởi động web server

### Bước 4: Truy cập ứng dụng
- Mở trình duyệt web
- Truy cập: `http://localhost:5000`
- Đăng nhập admin: `admin@healthfirst.com` / `admin123`
- Đăng nhập user test: `user@healthfirst.com` / `user123`

## Cách 2: Chạy thủ công

### Bước 1: Tạo môi trường ảo
```cmd
python -m venv venv
```

### Bước 2: Kích hoạt môi trường ảo
```cmd
venv\Scripts\activate
```

### Bước 3: Cài đặt thư viện
```cmd
pip install -r requirements.txt
```

### Bước 4: Tạo tài khoản admin
```cmd
python create_admin.py
```

### Bước 5: Khởi động ứng dụng
```cmd
python run.py
```

## Cách 3: Sử dụng Docker (Nâng cao)

### Bước 1: Cài đặt Docker Desktop
- Tải và cài đặt Docker Desktop từ docker.com

### Bước 2: Chạy với Docker Compose
```cmd
docker-compose up -d
```

### Bước 3: Truy cập ứng dụng
- Web app: `http://localhost:5000`
- Database: `localhost:5432`

## Cấu trúc tài khoản

### Tài khoản Admin
- **Email**: `admin@healthfirst.com`
- **Mật khẩu**: `admin123`
- **Quyền**: Quản lý toàn bộ hệ thống

### Tài khoản User Test
- **Email**: `user@healthfirst.com`
- **Mật khẩu**: `user123`
- **Quyền**: Người dùng thông thường

## Tính năng chính

### Giao diện người dùng
- Đăng ký/Đăng nhập
- Hồ sơ sức khỏe cá nhân
- Đánh giá triệu chứng
- Tài nguyên y tế
- Liên hệ hỗ trợ

### Giao diện Admin
- Quản lý tài khoản người dùng
- Xem lịch sử đánh giá sức khỏe
- Quản lý phản hồi từ người dùng
- Thống kê và báo cáo
- Xuất dữ liệu

## Xử lý lỗi thường gặp

### Lỗi "Module not found"
```cmd
pip install -r requirements.txt
```

### Lỗi "Database not found"
```cmd
python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

### Lỗi "Admin login không hoạt động"
```cmd
python fix_admin.py
```

### Lỗi "Port already in use"
- Thay đổi port trong `run.py` hoặc
- Tắt ứng dụng đang chạy trên port 5000

### Lỗi "Template not found"
- Kiểm tra thư mục `templates/` có tồn tại
- Đảm bảo file HTML được tạo đúng

## Dừng ứng dụng

### Cách 1: Nhấn Ctrl+C trong terminal

### Cách 2: Đóng terminal

### Cách 3: Với Docker
```cmd
docker-compose down
```

## Lưu ý quan trọng

1. **Bảo mật**: Đổi mật khẩu admin sau khi chạy lần đầu
2. **Dữ liệu**: Database được lưu trong file `health_app.db`
3. **Logs**: Kiểm tra terminal để xem log lỗi
4. **Backup**: Sao lưu file database thường xuyên
5. **Cập nhật**: Chạy `pip install -r requirements.txt` để cập nhật thư viện

## Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra Python version: `python --version`
2. Kiểm tra thư viện: `pip list`
3. Xem log lỗi trong terminal
4. Đảm bảo tất cả file được tạo đúng vị trí

## Cấu trúc thư mục quan trọng

```
website hướng dẫn y tế & chăm sóc sức khỏe tại nhà/
├── app.py                    # File chính của ứng dụng
├── run.py                    # Script khởi động
├── requirements.txt          # Danh sách thư viện
├── config.py                # Cấu hình
├── models.py                # Mô hình dữ liệu
├── routes.py                # Định tuyến
├── utils.py                 # Tiện ích
├── firebase_config.py       # Cấu hình Firebase
├── templates/               # Giao diện HTML
├── static/                  # CSS, JS, hình ảnh
├── data/                    # Dữ liệu y tế JSON
├── start_admin_fixed.bat    # Script tự động Windows (mới)
├── start_admin.bat          # Script tự động Windows (cũ)
├── fix_admin.py             # Sửa lỗi tài khoản admin
├── create_admin.py          # Tạo tài khoản admin
├── firebase-credentials.json # File cấu hình Firebase (tùy chọn)
└── venv/                    # Môi trường ảo Python
```

Chúc bạn chạy ứng dụng thành công! 🏥





























