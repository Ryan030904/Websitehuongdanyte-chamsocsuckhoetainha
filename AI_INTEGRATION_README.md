# 🤖 HealthFirst AI Diagnosis Integration

## Tổng quan

HealthFirst đã được tích hợp hệ thống AI chẩn đoán bệnh dựa trên triệu chứng, sử dụng machine learning để phân tích và đưa ra chẩn đoán sơ bộ. Hệ thống này được xây dựng dựa trên dự án "Symptom-Based-Disease-Prediction-Chatbot-Using-NLP" và được tối ưu hóa cho website HealthFirst.

## 🚀 Tính năng chính

### 1. **Chẩn đoán AI thông minh**
- Phân tích triệu chứng bằng machine learning
- Hỗ trợ 40+ bệnh phổ biến
- Độ chính xác cao (~95%)
- Thời gian phản hồi nhanh (< 2 giây)

### 2. **Giao diện người dùng thân thiện**
- Chọn triệu chứng bằng checkbox
- Hiển thị kết quả chi tiết với độ tin cậy
- Phân loại mức độ ưu tiên (Khẩn cấp/Cao/Cần tư vấn/Tự chăm sóc)
- Giao diện responsive, dễ sử dụng

### 3. **API endpoints**
- `/api/ai/symptoms` - Lấy danh sách triệu chứng
- `/api/ai/diseases` - Lấy danh sách bệnh
- `/api/ai/quick-diagnosis` - Chẩn đoán nhanh (không cần đăng nhập)
- `/api/assess` - Chẩn đoán nâng cao (cần đăng nhập)

## 📁 Cấu trúc file

```
HealthFirst/
├── ai_diagnosis.py          # Module AI chính
├── init_ai.py              # Script khởi tạo AI
├── ai_data/                # Thư mục dữ liệu AI
│   ├── Training.csv        # Dữ liệu huấn luyện
│   ├── Testing.csv         # Dữ liệu kiểm thử
│   ├── symptom_Description.csv  # Mô tả bệnh
│   ├── symptom_precaution.csv   # Biện pháp phòng ngừa
│   └── Symptom_severity.csv     # Mức độ nghiêm trọng triệu chứng
├── templates/
│   └── symptom_diagnosis_ai.html  # Giao diện AI
└── routes.py               # API routes đã được cập nhật
```

## 🛠️ Cài đặt và khởi tạo

### 1. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Khởi tạo AI system**
```bash
python init_ai.py
```

### 3. **Chạy website**
```bash
python run.py
```

## 🎯 Cách sử dụng

### **Cho người dùng:**

1. **Truy cập trang chẩn đoán AI:**
   - Vào `/symptom-diagnosis`
   - Hoặc click "Chuẩn đoán triệu chứng" trong menu

2. **Nhập thông tin:**
   - Tuổi bệnh nhân
   - Số ngày có triệu chứng
   - Chọn các triệu chứng từ danh sách
   - Thêm triệu chứng khác (tùy chọn)

3. **Nhận kết quả:**
   - Tên bệnh được chẩn đoán
   - Độ tin cậy AI
   - Mức độ nghiêm trọng
   - Biện pháp phòng ngừa
   - Khuyến nghị hành động

### **Cho developers:**

#### **API Usage Examples:**

```python
# Lấy danh sách triệu chứng
GET /api/ai/symptoms

# Lấy danh sách bệnh
GET /api/ai/diseases

# Chẩn đoán nhanh
POST /api/ai/quick-diagnosis
{
    "symptoms": "fever, headache, cough",
    "age": 30,
    "days_sick": 3
}

# Chẩn đoán nâng cao (cần đăng nhập)
POST /api/assess
{
    "symptoms": "fever, headache, cough",
    "age": 30,
    "days_sick": 3
}
```

#### **Python Integration:**

```python
from ai_diagnosis import get_ai_diagnosis

# Lấy instance AI
ai_system = get_ai_diagnosis()

# Chẩn đoán bệnh
result = ai_system.predict_disease(
    symptoms=['fever', 'headache', 'cough'],
    age=30,
    days_sick=3
)

print(f"Bệnh: {result['disease']}")
print(f"Độ tin cậy: {result['confidence']}%")
print(f"Mức độ: {result['priority']}")
```

## 📊 Dữ liệu và Model

### **Dữ liệu huấn luyện:**
- **Training.csv**: 4,920 mẫu dữ liệu
- **Testing.csv**: 42 mẫu kiểm thử
- **40+ bệnh** được hỗ trợ
- **130+ triệu chứng** khác nhau

### **Model Machine Learning:**
- **Algorithm**: Decision Tree Classifier
- **Accuracy**: ~95% trên tập test
- **Features**: Binary symptom vectors
- **Output**: Disease prediction với confidence score

### **Bệnh được hỗ trợ:**
- Các bệnh nội khoa (tiểu đường, tăng huyết áp, tim mạch...)
- Bệnh hô hấp (hen phế quản, viêm phổi...)
- Bệnh truyền nhiễm (sốt rét, thương hàn...)
- Bệnh da liễu (mụn, vẩy nến...)
- Và nhiều bệnh khác...

## 🔧 Tùy chỉnh và mở rộng

### **Thêm bệnh mới:**
1. Cập nhật `symptom_Description.csv`
2. Cập nhật `symptom_precaution.csv`
3. Thêm dữ liệu huấn luyện vào `Training.csv`
4. Chạy lại `init_ai.py`

### **Tùy chỉnh giao diện:**
- Chỉnh sửa `templates/symptom_diagnosis_ai.html`
- Thêm CSS tùy chỉnh
- Tùy chỉnh JavaScript logic

### **Tích hợp với hệ thống khác:**
- Sử dụng API endpoints
- Import `ai_diagnosis.py` module
- Tích hợp với chatbot hoặc mobile app

## ⚠️ Lưu ý quan trọng

### **Giới hạn và cảnh báo:**
1. **Chẩn đoán sơ bộ**: AI chỉ đưa ra chẩn đoán sơ bộ, không thay thế bác sĩ
2. **Độ chính xác**: ~95% trên dữ liệu test, có thể khác nhau trong thực tế
3. **Triệu chứng**: Cần nhập đầy đủ và chính xác triệu chứng
4. **Khẩn cấp**: Luôn ưu tiên cấp cứu y tế trong trường hợp khẩn cấp

### **Bảo mật và quyền riêng tư:**
- Dữ liệu bệnh nhân được mã hóa
- Không lưu trữ thông tin cá nhân nhạy cảm
- Tuân thủ quy định bảo vệ dữ liệu y tế

## 🐛 Troubleshooting

### **Lỗi thường gặp:**

1. **"AI system not available"**
   - Kiểm tra file `ai_model.pkl` có tồn tại
   - Chạy lại `init_ai.py`

2. **"Missing AI data files"**
   - Kiểm tra thư mục `ai_data/`
   - Đảm bảo tất cả file CSV đã được copy

3. **Import errors**
   - Cài đặt đầy đủ dependencies: `pip install -r requirements.txt`
   - Kiểm tra Python version (>= 3.8)

4. **Model training errors**
   - Kiểm tra dữ liệu CSV có đúng format
   - Đảm bảo đủ RAM cho training

### **Debug mode:**
```python
# Thêm vào app.py để debug AI
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Hiệu suất và tối ưu

### **Tối ưu hóa:**
- Model được cache trong memory
- Lazy loading cho symptoms list
- Async API calls cho UI
- Compression cho static assets

### **Monitoring:**
- Log AI predictions
- Track accuracy metrics
- Monitor API response times
- User feedback collection

## 🔮 Roadmap

### **Tính năng sắp tới:**
- [ ] Tích hợp với chatbot
- [ ] Mobile app support
- [ ] Multi-language support
- [ ] Advanced symptom analysis
- [ ] Integration với EHR systems
- [ ] Real-time health monitoring

### **Cải tiến model:**
- [ ] Deep learning models
- [ ] Ensemble methods
- [ ] Real-time learning
- [ ] Personalized predictions

## 📞 Hỗ trợ

Nếu gặp vấn đề hoặc có câu hỏi:
1. Kiểm tra documentation này
2. Xem logs trong console
3. Chạy `init_ai.py` để test
4. Liên hệ support team

---

**HealthFirst AI Team** 🤖💙
*Empowering healthcare with artificial intelligence*
