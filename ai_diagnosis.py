import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from typing import Dict, List

class HealthFirstAI:
    def __init__(self, data_dir: str = "ai_data"):
        self.data_dir = data_dir
        self.model = None
        self.label_encoder = LabelEncoder()
        self.symptom_severity = {}
        self.disease_descriptions = {}
        self.disease_precautions = {}
        self.symptoms_list = []
        self.diseases_list = []
        
        # Vietnamese translations
        self.symptom_translations = {
            'abdominal_pain': 'Đau bụng',
            'back_pain': 'Đau lưng',
            'chest_pain': 'Đau ngực',
            'cough': 'Ho',
            'depression': 'Trầm cảm',
            'dizziness': 'Chóng mặt',
            'fatigue': 'Mệt mỏi',
            'fever': 'Sốt',
            'headache': 'Đau đầu',
            'nausea': 'Buồn nôn',
            'vomiting': 'Nôn',
            'diarrhoea': 'Tiêu chảy',
            'burning_micturition': 'Tiểu buốt',
            'itching': 'Ngứa',
            'skin_rash': 'Phát ban',
            'joint_pain': 'Đau khớp',
            'muscle_pain': 'Đau cơ',
            'swelling': 'Sưng',
            'shortness_of_breath': 'Khó thở',
            'anxiety': 'Lo lắng',
            'constipation': 'Táo bón',
            'blister': 'Phồng rộp',
            'bruising': 'Bầm tím',
            'chills': 'Ớn lạnh',
            'congestion': 'Nghẹt mũi',
            'runny_nose': 'Sổ mũi',
            'sweating': 'Đổ mồ hôi',
            'weight_loss': 'Giảm cân',
            'weight_gain': 'Tăng cân'
        }
        
        self.disease_translations = {
            '(vertigo) Paroymsal  Positional Vertigo': 'Chóng mặt tư thế kịch phát',
            'AIDS': 'AIDS',
            'Acne': 'Mụn trứng cá',
            'Alcoholic hepatitis': 'Viêm gan do rượu',
            'Allergy': 'Dị ứng',
            'Arthritis': 'Viêm khớp',
            'Bronchial Asthma': 'Hen phế quản',
            'Cervical spondylosis': 'Thoái hóa đốt sống cổ',
            'Chicken pox': 'Thủy đậu',
            'Chronic cholestasis': 'Ứ mật mạn tính',
            'Common Cold': 'Cảm lạnh thông thường',
            'Dengue': 'Sốt xuất huyết',
            'Diabetes ': 'Tiểu đường',
            'Dimorphic hemmorhoids(piles)': 'Trĩ hỗn hợp',
            'Drug Reaction': 'Phản ứng thuốc',
            'Fungal infection': 'Nhiễm nấm',
            'GERD': 'Trào ngược dạ dày thực quản',
            'Gastroenteritis': 'Viêm dạ dày ruột',
            'Heart attack': 'Đau tim',
            'Hepatitis B': 'Viêm gan B',
            'Hepatitis C': 'Viêm gan C',
            'Hepatitis D': 'Viêm gan D',
            'Hepatitis E': 'Viêm gan E',
            'Hypertension ': 'Tăng huyết áp',
            'Hyperthyroidism': 'Cường giáp',
            'Hypoglycemia': 'Hạ đường huyết',
            'Hypothyroidism': 'Suy giáp',
            'Impetigo': 'Chốc lở',
            'Jaundice': 'Vàng da',
            'Malaria': 'Sốt rét',
            'Migraine': 'Đau nửa đầu',
            'Osteoarthristis': 'Viêm xương khớp',
            'Paralysis (brain hemorrhage)': 'Liệt (xuất huyết não)',
            'Peptic ulcer diseae': 'Loét dạ dày tá tràng',
            'Pneumonia': 'Viêm phổi',
            'Psoriasis': 'Vẩy nến',
            'Tuberculosis': 'Lao',
            'Typhoid': 'Thương hàn',
            'Urinary tract infection': 'Nhiễm trùng đường tiết niệu',
            'Varicose veins': 'Giãn tĩnh mạch',
            'hepatitis A': 'Viêm gan A'
        }
        
        self._load_data()
        self._train_model()
    
    def _load_data(self):
        try:
            severity_df = pd.read_csv(os.path.join(self.data_dir, "Symptom_severity.csv"))
            self.symptom_severity = dict(zip(severity_df.iloc[:, 0], severity_df.iloc[:, 1]))
            
            desc_df = pd.read_csv(os.path.join(self.data_dir, "symptom_Description.csv"))
            self.disease_descriptions = dict(zip(desc_df.iloc[:, 0], desc_df.iloc[:, 1]))
            
            prec_df = pd.read_csv(os.path.join(self.data_dir, "symptom_precaution.csv"))
            self.disease_precautions = dict(zip(prec_df.iloc[:, 0], prec_df.iloc[:, 1:].values.tolist()))
            
            self.training_data = pd.read_csv(os.path.join(self.data_dir, "Training.csv"))
            self.symptoms_list = [col for col in self.training_data.columns if col != 'prognosis']
            self.diseases_list = self.training_data['prognosis'].unique().tolist()
            
            print(f"✅ Loaded {len(self.symptoms_list)} symptoms and {len(self.diseases_list)} diseases")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self._create_fallback_data()
    
    def _create_fallback_data(self):
        print("📝 Creating fallback data...")
        self.symptom_severity = {
            'fever': 5, 'headache': 3, 'cough': 4, 'fatigue': 4, 'nausea': 5,
            'vomiting': 5, 'diarrhea': 6, 'abdominal_pain': 4, 'chest_pain': 7,
            'shortness_of_breath': 6, 'dizziness': 4, 'joint_pain': 3,
            'muscle_pain': 2, 'skin_rash': 3, 'itching': 1, 'swelling': 5
        }
        
        self.disease_descriptions = {
            'Common Cold': 'Nhiễm virus đường hô hấp trên gây ra các triệu chứng nhẹ.',
            'Influenza': 'Nhiễm virus tấn công hệ hô hấp của bạn.',
            'Gastroenteritis': 'Viêm dạ dày và ruột gây tiêu chảy và nôn.',
            'Hypertension': 'Huyết áp cao có thể dẫn đến các vấn đề sức khỏe nghiêm trọng.',
            'Diabetes': 'Bệnh ảnh hưởng đến cách cơ thể sử dụng glucose.',
            'Migraine': 'Đau đầu dữ dội có thể gây đau dữ dội và các triệu chứng khác.'
        }
        
        self.disease_precautions = {
            'Common Cold': ['Nghỉ ngơi', 'Uống nhiều nước', 'Dùng thuốc không kê đơn', 'Tránh tiếp xúc với người khác'],
            'Influenza': ['Nghỉ ngơi', 'Uống nhiều nước', 'Dùng thuốc hạ sốt', 'Tìm kiếm sự chăm sóc y tế nếu nghiêm trọng'],
            'Gastroenteritis': ['Uống nhiều nước', 'Nghỉ ngơi', 'Tránh thức ăn rắn ban đầu', 'Tìm kiếm sự chăm sóc y tế nếu nghiêm trọng'],
            'Hypertension': ['Giảm lượng muối', 'Tập thể dục thường xuyên', 'Duy trì cân nặng khỏe mạnh', 'Theo dõi huyết áp'],
            'Diabetes': ['Theo dõi đường huyết', 'Tuân theo chế độ ăn', 'Tập thể dục thường xuyên', 'Dùng thuốc theo chỉ định'],
            'Migraine': ['Nghỉ ngơi trong phòng tối', 'Tránh các yếu tố kích thích', 'Dùng thuốc giảm đau', 'Xem xét điều trị dự phòng']
        }
        
        self.symptoms_list = list(self.symptom_severity.keys())
        self.diseases_list = list(self.disease_descriptions.keys())
        
        np.random.seed(42)
        n_samples = 100
        n_symptoms = len(self.symptoms_list)
        
        data = []
        for _ in range(n_samples):
            symptoms = np.random.choice([0, 1], size=n_symptoms, p=[0.7, 0.3])
            disease = np.random.choice(self.diseases_list)
            row = list(symptoms) + [disease]
            data.append(row)
        
        columns = self.symptoms_list + ['prognosis']
        self.training_data = pd.DataFrame(data, columns=columns)
    
    def _train_model(self):
        try:
            X = self.training_data.drop('prognosis', axis=1)
            y = self.training_data['prognosis']
            y_encoded = self.label_encoder.fit_transform(y)
            
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42
            )
            
            self.model = DecisionTreeClassifier(random_state=42, max_depth=10)
            self.model.fit(X_train, y_train)
            
            train_accuracy = self.model.score(X_train, y_train)
            test_accuracy = self.model.score(X_test, y_test)
            
            print(f"✅ Model trained successfully!")
            print(f"   Training accuracy: {train_accuracy:.2f}")
            print(f"   Test accuracy: {test_accuracy:.2f}")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            self.model = None
    
    def predict_disease(self, symptoms: List[str], age: int = 30, days_sick: int = 3) -> Dict:
        try:
            if not self.model:
                return self._fallback_prediction(symptoms, age, days_sick)
            
            feature_vector = np.zeros(len(self.symptoms_list))
            
            for symptom in symptoms:
                symptom_normalized = symptom.lower().replace(' ', '_')
                for i, known_symptom in enumerate(self.symptoms_list):
                    if symptom_normalized in known_symptom or known_symptom in symptom_normalized:
                        feature_vector[i] = 1
                        break
            
            prediction_encoded = self.model.predict([feature_vector])[0]
            predicted_disease = self.label_encoder.inverse_transform([prediction_encoded])[0]
            
            probabilities = self.model.predict_proba([feature_vector])[0]
            confidence = max(probabilities)
            
            severity_score = self._calculate_severity_score(symptoms, age, days_sick)
            priority = self._determine_priority(severity_score, confidence, age, days_sick)
            
            description = self.disease_descriptions.get(predicted_disease, "Không có mô tả.")
            precautions = self.disease_precautions.get(predicted_disease, ["Tham khảo ý kiến bác sĩ", "Nghỉ ngơi", "Uống nhiều nước"])
            
            disease_vn = self.disease_translations.get(predicted_disease, predicted_disease)
            
            return {
                'disease': disease_vn,
                'disease_en': predicted_disease,
                'confidence': round(confidence * 100, 1),
                'severity_score': severity_score,
                'priority': priority,
                'description': description,
                'precautions': precautions,
                'recommendations': self._generate_recommendations(priority, disease_vn, age),
                'symptoms_analyzed': symptoms,
                'age_factor': age,
                'duration_factor': days_sick
            }
            
        except Exception as e:
            print(f"❌ Error in prediction: {e}")
            return self._fallback_prediction(symptoms, age, days_sick)
    
    def _calculate_severity_score(self, symptoms: List[str], age: int, days_sick: int) -> int:
        base_score = 0
        
        for symptom in symptoms:
            symptom_normalized = symptom.lower().replace(' ', '_')
            for known_symptom, severity in self.symptom_severity.items():
                if symptom_normalized in known_symptom or known_symptom in symptom_normalized:
                    base_score += severity
                    break
        
        age_factor = max(0, (age - 30) / 10)
        duration_factor = min(days_sick / 7, 2)
        
        total_score = base_score + age_factor + duration_factor
        return min(int(total_score), 10)
    
    def _determine_priority(self, severity_score: int, confidence: float, age: int, days_sick: int) -> str:
        if severity_score >= 8 or (severity_score >= 6 and age > 60):
            return 'emergency'
        elif severity_score >= 6 or (severity_score >= 4 and days_sick > 7):
            return 'high'
        elif severity_score >= 4 or confidence < 0.5:
            return 'consult_doctor'
        else:
            return 'self_care'
    
    def _generate_recommendations(self, priority: str, disease: str, age: int) -> List[str]:
        recommendations = []
        
        if priority == 'emergency':
            recommendations.extend([
                "🚨 Tìm kiếm sự chăm sóc y tế ngay lập tức",
                "Gọi cấp cứu nếu triệu chứng trở nên tồi tệ hơn",
                "Không trì hoãn điều trị"
            ])
        elif priority == 'high':
            recommendations.extend([
                "🏥 Đặt lịch hẹn với bác sĩ trong vòng 24-48 giờ",
                "Theo dõi triệu chứng chặt chẽ",
                "Nghỉ ngơi và tránh các hoạt động gắng sức"
            ])
        elif priority == 'consult_doctor':
            recommendations.extend([
                "👨‍⚕️ Xem xét tham khảo ý kiến bác sĩ nếu triệu chứng kéo dài",
                "Theo dõi triệu chứng để phát hiện bất kỳ thay đổi nào",
                "Tuân theo các hướng dẫn sức khỏe chung"
            ])
        else:
            recommendations.extend([
                "🏠 Tự chăm sóc thường là đủ",
                "Nghỉ ngơi và uống nhiều nước",
                "Theo dõi bất kỳ triệu chứng trở nên tồi tệ hơn"
            ])
        
        if age > 60:
            recommendations.append("⚠️ Bệnh nhân cao tuổi nên thận trọng hơn và tìm kiếm lời khuyên y tế sớm hơn")
        
        return recommendations
    
    def _fallback_prediction(self, symptoms: List[str], age: int, days_sick: int) -> Dict:
        if any(symptom in ['fever', 'cough', 'sore throat'] for symptom in symptoms):
            disease = 'Cảm lạnh thông thường'
        elif any(symptom in ['chest pain', 'shortness of breath'] for symptom in symptoms):
            disease = 'Khẩn cấp - Vấn đề tim/phổi'
        elif any(symptom in ['vomiting', 'diarrhea', 'abdominal pain'] for symptom in symptoms):
            disease = 'Viêm dạ dày ruột'
        else:
            disease = 'Bệnh chung'
        
        severity_score = self._calculate_severity_score(symptoms, age, days_sick)
        priority = self._determine_priority(severity_score, 0.5, age, days_sick)
        
        return {
            'disease': disease,
            'disease_en': disease,
            'confidence': 50.0,
            'severity_score': severity_score,
            'priority': priority,
            'description': 'Mô hình AI không khả dụng. Đây là đánh giá cơ bản.',
            'precautions': ['Tham khảo ý kiến bác sĩ', 'Nghỉ ngơi', 'Uống nhiều nước', 'Theo dõi triệu chứng'],
            'recommendations': self._generate_recommendations(priority, disease, age),
            'symptoms_analyzed': symptoms,
            'age_factor': age,
            'duration_factor': days_sick
        }
    
    def get_available_symptoms(self) -> List[str]:
        return sorted(self.symptoms_list)
    
    def get_available_symptoms_vn(self) -> List[Dict]:
        symptoms_vn = []
        for symptom in sorted(self.symptoms_list):
            symptoms_vn.append({
                'en': symptom,
                'vn': self.symptom_translations.get(symptom, symptom.replace('_', ' ').title())
            })
        return symptoms_vn
    
    def get_available_diseases(self) -> List[str]:
        return sorted(self.diseases_list)
    
    def get_available_diseases_vn(self) -> List[Dict]:
        diseases_vn = []
        for disease in sorted(self.diseases_list):
            diseases_vn.append({
                'en': disease,
                'vn': self.disease_translations.get(disease, disease)
            })
        return diseases_vn
    
    def get_symptom_info(self, symptom: str) -> Dict:
        symptom_normalized = symptom.lower().replace(' ', '_')
        
        for known_symptom, severity in self.symptom_severity.items():
            if symptom_normalized in known_symptom or known_symptom in symptom_normalized:
                return {
                    'name': known_symptom,
                    'name_vn': self.symptom_translations.get(known_symptom, known_symptom.replace('_', ' ').title()),
                    'severity': severity,
                    'description': f'Mức độ nghiêm trọng: {severity}/10'
                }
        
        return {
            'name': symptom,
            'name_vn': symptom,
            'severity': 3,
            'description': 'Triệu chứng không có trong cơ sở dữ liệu'
        }
    
    def save_model(self, filepath: str = "ai_model.pkl"):
        try:
            with open(filepath, 'wb') as f:
                pickle.dump({
                    'model': self.model,
                    'label_encoder': self.label_encoder,
                    'symptoms_list': self.symptoms_list,
                    'diseases_list': self.diseases_list,
                    'symptom_severity': self.symptom_severity,
                    'disease_descriptions': self.disease_descriptions,
                    'disease_precautions': self.disease_precautions
                }, f)
            print(f"✅ Model saved to {filepath}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")
    
    def load_model(self, filepath: str = "ai_model.pkl"):
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['label_encoder']
                self.symptoms_list = data['symptoms_list']
                self.diseases_list = data['diseases_list']
                self.symptom_severity = data['symptom_severity']
                self.disease_descriptions = data['disease_descriptions']
                self.disease_precautions = data['disease_precautions']
            print(f"✅ Model loaded from {filepath}")
        except Exception as e:
            print(f"❌ Error loading model: {e}")

# Global AI instance
ai_diagnosis = None

def initialize_ai():
    global ai_diagnosis
    try:
        if os.path.exists("ai_model.pkl"):
            ai_diagnosis = HealthFirstAI()
            ai_diagnosis.load_model("ai_model.pkl")
        else:
            ai_diagnosis = HealthFirstAI()
            ai_diagnosis.save_model("ai_model.pkl")
        
        return ai_diagnosis
    except Exception as e:
        print(f"❌ Error initializing AI: {e}")
        return None

def get_ai_diagnosis():
    global ai_diagnosis
    if ai_diagnosis is None:
        ai_diagnosis = initialize_ai()
    return ai_diagnosis
