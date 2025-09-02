# HealthFirst Makefile
# Sử dụng: make <target>

.PHONY: help install setup run test clean venv db-init db-migrate db-upgrade

# Default target
help:
	@echo "🏥 HealthFirst - Hệ Thống Hướng Dẫn Y Tế Tại Nhà"
	@echo "=================================================="
	@echo ""
	@echo "Các lệnh có sẵn:"
	@echo "  install     - Cài đặt dependencies"
	@echo "  setup       - Thiết lập dự án (tạo venv, cài đặt, khởi tạo DB)"
	@echo "  run         - Chạy ứng dụng"
	@echo "  test        - Chạy tests"
	@echo "  clean       - Dọn dẹp cache và temporary files"
	@echo "  venv        - Tạo môi trường ảo"
	@echo "  db-init     - Khởi tạo database"
	@echo "  db-migrate  - Tạo migration mới"
	@echo "  db-upgrade  - Áp dụng migrations"
	@echo ""

# Tạo môi trường ảo
venv:
	@echo "🐍 Tạo môi trường ảo..."
	python -m venv .venv
	@echo "✅ Môi trường ảo đã được tạo!"

# Cài đặt dependencies
install:
	@echo "📦 Cài đặt dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies đã được cài đặt!"

# Thiết lập dự án
setup: venv
	@echo "🔧 Thiết lập dự án..."
	.venv/bin/activate && pip install -r requirements.txt
	.venv/bin/activate && python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all(); print('Database initialized successfully')"
	@echo "✅ Dự án đã được thiết lập!"

# Chạy ứng dụng
run:
	@echo "🚀 Khởi động HealthFirst..."
	python run.py

# Chạy tests
test:
	@echo "🧪 Chạy tests..."
	python -m pytest tests/ -v

# Dọn dẹp
clean:
	@echo "🧹 Dọn dẹp..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	@echo "✅ Đã dọn dẹp xong!"

# Khởi tạo database
db-init:
	@echo "🗄️  Khởi tạo database..."
	python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all(); print('Database initialized successfully')"

# Tạo migration mới
db-migrate:
	@echo "📝 Tạo migration mới..."
	flask db migrate -m "Auto migration"

# Áp dụng migrations
db-upgrade:
	@echo "⬆️  Áp dụng migrations..."
	flask db upgrade

# Windows commands
windows-setup:
	@echo "🔧 Thiết lập dự án trên Windows..."
	python -m venv .venv
	.venv\Scripts\activate.bat && pip install -r requirements.txt
	.venv\Scripts\activate.bat && python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all(); print('Database initialized successfully')"
	@echo "✅ Dự án đã được thiết lập trên Windows!"

windows-run:
	@echo "🚀 Khởi động HealthFirst trên Windows..."
	.venv\Scripts\activate.bat && python run.py

# Development commands
dev-install:
	@echo "🔧 Cài đặt development dependencies..."
	pip install -r requirements.txt
	pip install -e .[dev]

dev-run:
	@echo "🚀 Khởi động HealthFirst trong chế độ development..."
	FLASK_ENV=development python run.py

# Production commands
prod-install:
	@echo "🔧 Cài đặt production dependencies..."
	pip install -r requirements.txt
	pip install -e .[production]

prod-run:
	@echo "🚀 Khởi động HealthFirst trong chế độ production..."
	FLASK_ENV=production gunicorn -w 4 -b 0.0.0.0:5000 run:app
