#!/usr/bin/env python3
"""
Demo script để test hệ thống đánh giá sức khỏe HealthFirst
Sử dụng Python thuần với Flask backend
"""

import requests
import json
import time

# Cấu hình
BASE_URL = "http://localhost:5000"
TEST_USER = {
    "email": "demo@healthfirst.com",
    "password": "demo123"
}

def test_health_assessment():
    """Test toàn bộ quy trình đánh giá sức khỏe"""
    print("🏥 HealthFirst - Demo Đánh Giá Sức Khỏe")
    print("=" * 50)
    
    # 1. Đăng nhập
    print("\n1️⃣ Đăng nhập...")
    login_data = {
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code == 200:
            print("✅ Đăng nhập thành công!")
        else:
            print(f"❌ Đăng nhập thất bại: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Không thể kết nối đến server. Hãy chạy 'python run.py' trước!")
        return
    
    # 2. Cập nhật thông tin sức khỏe
    print("\n2️⃣ Cập nhật thông tin sức khỏe...")
    health_data = {
        "gender": "male",
        "age": 30,
        "height": 175.0,
        "weight": 70.0,
        "medical_history": "Không có bệnh mãn tính, đôi khi bị đau đầu"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/profile/update",
            json=health_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Thông tin sức khỏe đã được cập nhật!")
                user_info = result.get('user', {})
                print(f"   - Tuổi: {user_info.get('age')}")
                print(f"   - Chiều cao: {user_info.get('height')} cm")
                print(f"   - Cân nặng: {user_info.get('weight')} kg")
                print(f"   - BMI: {user_info.get('bmi')} ({user_info.get('bmi_category')})")
            else:
                print(f"❌ Lỗi: {result.get('error')}")
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật thông tin: {e}")
    
    # 3. Đánh giá triệu chứng
    print("\n3️⃣ Đánh giá triệu chứng...")
    symptoms_data = {
        "symptoms": "Đau đầu, mệt mỏi, sốt nhẹ 37.5°C",
        "days_sick": 2,
        "age": 30
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/assess",
            json=symptoms_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Đánh giá triệu chứng hoàn tất!")
            print(f"   - Mức độ: {result.get('priority', 'N/A')}")
            print(f"   - Khuyến nghị: {result.get('message', 'N/A')}")
            
            if result.get('recommendations'):
                print("   - Hướng dẫn:")
                for rec in result['recommendations']:
                    print(f"     • {rec}")
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi khi đánh giá triệu chứng: {e}")
    
    # 4. Lấy chủ đề y tế
    print("\n4️⃣ Lấy chủ đề y tế...")
    try:
        response = requests.get(f"{BASE_URL}/api/health-topics")
        if response.status_code == 200:
            topics = response.json()
            print(f"✅ Tìm thấy {len(topics)} chủ đề y tế")
            for i, topic in enumerate(topics[:3], 1):
                print(f"   {i}. {topic.get('title', 'N/A')}")
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
    except Exception as e:
        print(f"❌ Lỗi khi lấy chủ đề y tế: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo hoàn tất!")
    print("💡 Mở trình duyệt và truy cập: http://localhost:5000")

if __name__ == "__main__":
    print("🚀 Khởi động demo HealthFirst...")
    print("⚠️  Đảm bảo server đang chạy (python run.py)")
    print()
    
    try:
        test_health_assessment()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo bị dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {e}")
    
    print("\n👋 Tạm biệt!")
