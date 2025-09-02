#!/usr/bin/env python3
"""
HealthFirst Web Application
Hệ thống hướng dẫn y tế tại nhà
"""

import os
import sys
from app import create_app

def main():
    """Main entry point"""
    print("🏥 HealthFirst - Hệ Thống Hướng Dẫn Y Tế Tại Nhà")
    print("=" * 60)
    
    # Set environment
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌍 Môi trường: {env}")
    
    # Create app
    app = create_app(env)
    
    # Get configuration
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = app.config.get('DEBUG', False)
    
    print(f"🚀 Khởi động server tại: http://{host}:{port}")
    print(f"🐛 Debug mode: {'Bật' if debug else 'Tắt'}")
    print("=" * 60)
    print("💡 Nhấn Ctrl+C để dừng server")
    print()
    
    try:
        app.run(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\n⏹️  Server đã dừng")
    except Exception as e:
        print(f"\n❌ Lỗi khởi động server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
