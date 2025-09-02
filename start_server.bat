@echo off
echo ========================================
echo    HealthFirst - Khởi động Server
echo ========================================
echo.

echo [1/4] Kích hoạt môi trường ảo...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Lỗi: Không thể kích hoạt môi trường ảo
    echo Vui lòng chạy: python -m venv .venv
    pause
    exit /b 1
)

echo [2/4] Cài đặt dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Lỗi: Không thể cài đặt dependencies
    pause
    exit /b 1
)

echo [3/4] Khởi tạo database...
python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all(); print('Database initialized successfully')"
if errorlevel 1 (
    echo Cảnh báo: Không thể khởi tạo database, nhưng vẫn tiếp tục...
)

echo [4/4] Khởi động server...
echo.
echo Server sẽ chạy tại: http://localhost:5000
echo Nhấn Ctrl+C để dừng server
echo.
python run.py

pause
