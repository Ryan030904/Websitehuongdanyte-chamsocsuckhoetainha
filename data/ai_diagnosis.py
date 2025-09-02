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
        
        # Vietnamese translations - Complete list with all symptoms
        self.symptom_translations = {
            'abdominal_pain': 'Đau bụng',
            'abnormal_menstruation': 'Rối loạn kinh nguyệt',
            'acidity': 'Ợ chua',
            'acute_liver_failure': 'Suy gan cấp',
            'altered_sensorium': 'Rối loạn ý thức',
            'anxiety': 'Lo lắng',
            'back_pain': 'Đau lưng',
            'belly_pain': 'Đau bụng',
            'blackheads': 'Mụn đầu đen',
            'bladder_discomfort': 'Khó chịu bàng quang',
            'blister': 'Phồng rộp',
            'blood_in_sputum': 'Ho ra máu',
            'bloody_stool': 'Phân có máu',
            'blurred_and_distorted_vision': 'Mờ mắt',
            'breathlessness': 'Khó thở',
            'brittle_nails': 'Móng tay giòn',
            'bruising': 'Bầm tím',
            'burning_micturition': 'Tiểu buốt',
            'chest_pain': 'Đau ngực',
            'chills': 'Ớn lạnh',
            'cold_hands_and_feets': 'Tay chân lạnh',
            'coma': 'Hôn mê',
            'congestion': 'Nghẹt mũi',
            'constipation': 'Táo bón',
            'continuous_feel_of_urine': 'Tiểu liên tục',
            'continuous_sneezing': 'Hắt hơi liên tục',
            'cough': 'Ho',
            'cramps': 'Chuột rút',
            'dark_urine': 'Nước tiểu sẫm màu',
            'dehydration': 'Mất nước',
            'depression': 'Trầm cảm',
            'diarrhoea': 'Tiêu chảy',
            'dischromic_patches': 'Đốm da bất thường',
            'distention_of_abdomen': 'Chướng bụng',
            'dizziness': 'Chóng mặt',
            'drying_and_tingling_lips': 'Khô và ngứa môi',
            'enlarged_thyroid': 'Tuyến giáp to',
            'excessive_hunger': 'Đói quá mức',
            'extra_marital_contacts': 'Quan hệ ngoài hôn nhân',
            'family_history': 'Tiền sử gia đình',
            'fast_heart_rate': 'Nhịp tim nhanh',
            'fatigue': 'Mệt mỏi',
            'fever': 'Sốt',
            'fluid_overload': 'Quá tải dịch',
            'fluid_retention': 'Giữ nước',
            'foul_smell_of_urine': 'Nước tiểu có mùi hôi',
            'headache': 'Đau đầu',
            'high_fever': 'Sốt cao',
            'hip_joint_pain': 'Đau khớp háng',
            'history_of_alcohol_consumption': 'Tiền sử uống rượu',
            'increased_appetite': 'Tăng cảm giác thèm ăn',
            'indigestion': 'Khó tiêu',
            'inflammatory_nails': 'Viêm móng',
            'internal_itching': 'Ngứa trong',
            'irregular_sugar_level': 'Đường huyết không ổn định',
            'irritability': 'Cáu gắt',
            'irritation_in_anus': 'Kích ứng hậu môn',
            'itching': 'Ngứa',
            'joint_pain': 'Đau khớp',
            'knee_pain': 'Đau đầu gối',
            'lack_of_concentration': 'Thiếu tập trung',
            'lethargy': 'Lờ đờ',
            'loss_of_appetite': 'Chán ăn',
            'loss_of_balance': 'Mất thăng bằng',
            'loss_of_smell': 'Mất khứu giác',
            'malaise': 'Khó chịu',
            'mild_fever': 'Sốt nhẹ',
            'mood_swings': 'Thay đổi tâm trạng',
            'movement_stiffness': 'Cứng khớp',
            'mucoid_sputum': 'Đờm nhầy',
            'muscle_pain': 'Đau cơ',
            'muscle_wasting': 'Teo cơ',
            'muscle_weakness': 'Yếu cơ',
            'nausea': 'Buồn nôn',
            'neck_pain': 'Đau cổ',
            'nodal_skin_eruptions': 'Nổi mẩn da',
            'obesity': 'Béo phì',
            'pain_behind_the_eyes': 'Đau sau mắt',
            'pain_during_bowel_movements': 'Đau khi đi vệ sinh',
            'pain_in_anal_region': 'Đau vùng hậu môn',
            'painful_walking': 'Đau khi đi lại',
            'palpitations': 'Đánh trống ngực',
            'passage_of_gases': 'Xì hơi',
            'patches_in_throat': 'Đốm trong họng',
            'phlegm': 'Đờm',
            'polyuria': 'Tiểu nhiều',
            'prominent_veins_on_calf': 'Tĩnh mạch nổi ở bắp chân',
            'puffy_face_and_eyes': 'Mặt và mắt sưng',
            'pus_filled_pimples': 'Mụn mủ',
            'receiving_blood_transfusion': 'Truyền máu',
            'receiving_unsterile_injections': 'Tiêm không vô trùng',
            'red_sore_around_nose': 'Vết loét đỏ quanh mũi',
            'red_spots_over_body': 'Đốm đỏ trên cơ thể',
            'redness_of_eyes': 'Đỏ mắt',
            'runny_nose': 'Sổ mũi',
            'rusty_sputum': 'Đờm rỉ sắt',
            'scurring': 'Sẹo',
            'shivering': 'Run rẩy',
            'silver_like_dusting': 'Bụi bạc',
            'sinus_pressure': 'Áp lực xoang',
            'skin_peeling': 'Bong da',
            'skin_rash': 'Phát ban',
            'slurred_speech': 'Nói lắp',
            'small_dents_in_nails': 'Vết lõm nhỏ trên móng',
            'spinning_movements': 'Chuyển động xoay',
            'spotting_urination': 'Tiểu nhỏ giọt',
            'stiff_neck': 'Cứng cổ',
            'stomach_bleeding': 'Chảy máu dạ dày',
            'stomach_pain': 'Đau dạ dày',
            'sunken_eyes': 'Mắt lõm',
            'sweating': 'Đổ mồ hôi',
            'swelled_lymph_nodes': 'Hạch bạch huyết sưng',
            'swelling_joints': 'Sưng khớp',
            'swelling_of_stomach': 'Sưng bụng',
            'swollen_blood_vessels': 'Mạch máu sưng',
            'swollen_extremeties': 'Chi sưng',
            'swollen_legs': 'Chân sưng',
            'throat_irritation': 'Kích ứng họng',
            'toxic_look_typhos': 'Vẻ mặt nhiễm độc',
            'ulcers_on_tongue': 'Loét lưỡi',
            'unsteadiness': 'Không vững',
            'visual_disturbances': 'Rối loạn thị giác',
            'vomiting': 'Nôn',
            'watering_from_eyes': 'Chảy nước mắt',
            'weakness_in_limbs': 'Yếu chi',
            'weakness_of_one_body_side': 'Yếu một bên cơ thể',
            'weight_gain': 'Tăng cân',
            'weight_loss': 'Giảm cân',
            'yellow_crust_ooze': 'Vảy vàng chảy dịch',
            'yellow_urine': 'Nước tiểu vàng',
            'yellowing_of_eyes': 'Vàng mắt',
            'yellowish_skin': 'Da vàng'
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
            'Common Cold': 'Nhiễm virus đường hô hấp trên gây ra các triệu chứng nhẹ như ho, sổ mũi, đau họng.',
            'Influenza': 'Nhiễm virus tấn công hệ hô hấp với triệu chứng sốt cao, đau cơ, mệt mỏi.',
            'Gastroenteritis': 'Viêm dạ dày và ruột gây tiêu chảy, nôn mửa, đau bụng.',
            'Hypertension': 'Huyết áp cao có thể dẫn đến các vấn đề tim mạch nghiêm trọng.',
            'Diabetes': 'Bệnh rối loạn chuyển hóa glucose, ảnh hưởng đến lượng đường trong máu.',
            'Migraine': 'Đau đầu dữ dội một bên, thường kèm theo buồn nôn và nhạy cảm với ánh sáng.',
            '(vertigo) Paroymsal  Positional Vertigo': 'Chóng mặt khi thay đổi tư thế đầu, thường do vấn đề tai trong.',
            'AIDS': 'Hội chứng suy giảm miễn dịch mắc phải, ảnh hưởng nghiêm trọng đến hệ miễn dịch.',
            'Acne': 'Tình trạng viêm da do tắc nghẽn lỗ chân lông, thường xuất hiện ở mặt và lưng.',
            'Alcoholic hepatitis': 'Viêm gan do uống rượu quá nhiều, có thể dẫn đến xơ gan.',
            'Allergy': 'Phản ứng quá mẫn của hệ miễn dịch với các chất gây dị ứng.',
            'Arthritis': 'Viêm khớp gây đau, sưng và cứng khớp, ảnh hưởng đến khả năng vận động.',
            'Bronchial Asthma': 'Bệnh viêm đường hô hấp mạn tính, gây khó thở và thở khò khè.',
            'Cervical spondylosis': 'Thoái hóa đốt sống cổ, gây đau cổ và có thể lan xuống cánh tay.',
            'Chicken pox': 'Bệnh truyền nhiễm do virus, gây phát ban và mụn nước trên da.',
            'Chronic cholestasis': 'Tình trạng ứ mật mạn tính, ảnh hưởng đến chức năng gan. Bệnh này xảy ra khi có sự cản trở trong việc vận chuyển mật từ gan đến ruột.',
            'Dengue': 'Bệnh truyền nhiễm do muỗi, gây sốt cao, đau cơ và có thể nghiêm trọng.',
            'Diabetes ': 'Bệnh rối loạn chuyển hóa glucose, cần theo dõi đường huyết thường xuyên.',
            'Dimorphic hemmorhoids(piles)': 'Bệnh trĩ hỗn hợp, gây đau và chảy máu khi đi vệ sinh.',
            'Drug Reaction': 'Phản ứng bất lợi với thuốc, có thể gây phát ban hoặc các triệu chứng khác.',
            'Fungal infection': 'Nhiễm nấm trên da hoặc niêm mạc, thường gây ngứa và đỏ da.',
            'GERD': 'Trào ngược axit dạ dày lên thực quản, gây ợ chua và đau ngực.',
            'Heart attack': 'Cơn đau tim cấp tính, cần cấp cứu ngay lập tức.',
            'Hepatitis B': 'Viêm gan B do virus, có thể dẫn đến xơ gan và ung thư gan.',
            'Hepatitis C': 'Viêm gan C do virus, thường không có triệu chứng rõ ràng.',
            'Hepatitis D': 'Viêm gan D, chỉ xảy ra ở người đã nhiễm viêm gan B.',
            'Hepatitis E': 'Viêm gan E do virus, thường lây qua đường ăn uống.',
            'Hypertension ': 'Tăng huyết áp, yếu tố nguy cơ chính của bệnh tim mạch.',
            'Hyperthyroidism': 'Cường giáp, tuyến giáp hoạt động quá mức.',
            'Hypoglycemia': 'Hạ đường huyết, có thể gây chóng mặt và ngất xỉu.',
            'Hypothyroidism': 'Suy giáp, tuyến giáp hoạt động kém.',
            'Impetigo': 'Nhiễm trùng da do vi khuẩn, gây mụn nước và vết loét.',
            'Jaundice': 'Vàng da và mắt do tăng bilirubin trong máu.',
            'Malaria': 'Bệnh truyền nhiễm do ký sinh trùng, gây sốt cao và ớn lạnh.',
            'Osteoarthristis': 'Viêm xương khớp, thoái hóa sụn khớp.',
            'Paralysis (brain hemorrhage)': 'Liệt do xuất huyết não, cần cấp cứu ngay.',
            'Peptic ulcer diseae': 'Loét dạ dày tá tràng, gây đau bụng và khó tiêu.',
            'Pneumonia': 'Viêm phổi, nhiễm trùng phổi nghiêm trọng.',
            'Psoriasis': 'Bệnh vẩy nến, rối loạn da mạn tính.',
            'Tuberculosis': 'Bệnh lao, nhiễm trùng phổi do vi khuẩn.',
            'Typhoid': 'Bệnh thương hàn, nhiễm trùng đường ruột nghiêm trọng.',
            'Urinary tract infection': 'Nhiễm trùng đường tiết niệu, gây tiểu buốt và đau.',
            'Varicose veins': 'Giãn tĩnh mạch, thường ở chân.',
            'hepatitis A': 'Viêm gan A do virus, lây qua đường ăn uống.'
        }
        
        self.disease_precautions = {
            'Common Cold': ['Nghỉ ngơi đầy đủ', 'Uống nhiều nước', 'Dùng thuốc không kê đơn', 'Tránh tiếp xúc với người khác'],
            'Influenza': ['Nghỉ ngơi hoàn toàn', 'Uống nhiều nước', 'Dùng thuốc hạ sốt', 'Tìm kiếm sự chăm sóc y tế nếu nghiêm trọng'],
            'Gastroenteritis': ['Uống nhiều nước', 'Nghỉ ngơi', 'Tránh thức ăn rắn ban đầu', 'Tìm kiếm sự chăm sóc y tế nếu nghiêm trọng'],
            'Hypertension': ['Giảm lượng muối', 'Tập thể dục thường xuyên', 'Duy trì cân nặng khỏe mạnh', 'Theo dõi huyết áp'],
            'Diabetes': ['Theo dõi đường huyết', 'Tuân theo chế độ ăn', 'Tập thể dục thường xuyên', 'Dùng thuốc theo chỉ định'],
            'Migraine': ['Nghỉ ngơi trong phòng tối', 'Tránh các yếu tố kích thích', 'Dùng thuốc giảm đau', 'Xem xét điều trị dự phòng'],
            '(vertigo) Paroymsal  Positional Vertigo': ['Tránh thay đổi tư thế đột ngột', 'Thực hiện bài tập phục hồi', 'Tham khảo ý kiến bác sĩ', 'Nghỉ ngơi khi chóng mặt'],
            'AIDS': ['Tuân thủ điều trị ARV', 'Tăng cường miễn dịch', 'Khám định kỳ', 'Tránh nhiễm trùng'],
            'Acne': ['Giữ da sạch sẽ', 'Tránh nặn mụn', 'Dùng kem chống nắng', 'Tham khảo ý kiến bác sĩ da liễu'],
            'Alcoholic hepatitis': ['Ngừng uống rượu hoàn toàn', 'Chế độ ăn lành mạnh', 'Khám gan định kỳ', 'Tập thể dục vừa phải'],
            'Allergy': ['Tránh chất gây dị ứng', 'Dùng thuốc kháng histamine', 'Giữ môi trường sạch sẽ', 'Tham khảo ý kiến bác sĩ'],
            'Arthritis': ['Tập thể dục nhẹ nhàng', 'Giữ ấm khớp', 'Dùng thuốc giảm đau', 'Vật lý trị liệu'],
            'Bronchial Asthma': ['Tránh chất kích thích', 'Dùng thuốc hít theo chỉ định', 'Tập thở', 'Khám định kỳ'],
            'Cervical spondylosis': ['Tập thể dục cổ', 'Giữ tư thế đúng', 'Dùng gối phù hợp', 'Vật lý trị liệu'],
            'Chicken pox': ['Cách ly bệnh nhân', 'Giữ vệ sinh', 'Không gãi mụn', 'Dùng thuốc theo chỉ định'],
            'Chronic cholestasis': ['Chế độ ăn ít mỡ', 'Uống nhiều nước', 'Khám gan định kỳ', 'Tránh rượu bia'],
            'Dengue': ['Diệt muỗi', 'Ngủ màn', 'Uống nhiều nước', 'Tìm kiếm sự chăm sóc y tế ngay'],
            'Diabetes ': ['Theo dõi đường huyết', 'Chế độ ăn kiêng', 'Tập thể dục', 'Dùng thuốc đúng giờ'],
            'Dimorphic hemmorhoids(piles)': ['Chế độ ăn nhiều chất xơ', 'Uống nhiều nước', 'Tránh ngồi lâu', 'Vệ sinh sạch sẽ'],
            'Drug Reaction': ['Ngừng thuốc gây dị ứng', 'Tham khảo ý kiến bác sĩ', 'Ghi nhớ thuốc dị ứng', 'Mang thông tin y tế'],
            'Fungal infection': ['Giữ vùng bệnh khô ráo', 'Dùng thuốc chống nấm', 'Vệ sinh sạch sẽ', 'Tránh dùng chung đồ'],
            'GERD': ['Tránh thức ăn cay nóng', 'Không ăn trước khi ngủ', 'Nâng cao đầu giường', 'Giảm cân nếu thừa cân'],
            'Heart attack': ['Gọi cấp cứu ngay', 'Nghỉ ngơi hoàn toàn', 'Dùng thuốc theo chỉ định', 'Khám tim định kỳ'],
            'Hepatitis B': ['Tiêm vaccine', 'Tránh lây nhiễm', 'Khám gan định kỳ', 'Chế độ ăn lành mạnh'],
            'Hepatitis C': ['Tránh lây nhiễm', 'Không dùng chung kim tiêm', 'Khám gan định kỳ', 'Điều trị theo chỉ định'],
            'Hepatitis D': ['Điều trị viêm gan B', 'Tránh lây nhiễm', 'Khám gan định kỳ', 'Chế độ ăn lành mạnh'],
            'Hepatitis E': ['Vệ sinh ăn uống', 'Uống nước sạch', 'Khám gan định kỳ', 'Nghỉ ngơi đầy đủ'],
            'Hypertension ': ['Giảm muối', 'Tập thể dục', 'Giảm cân', 'Dùng thuốc đều đặn'],
            'Hyperthyroidism': ['Dùng thuốc theo chỉ định', 'Khám định kỳ', 'Tránh stress', 'Chế độ ăn phù hợp'],
            'Hypoglycemia': ['Mang kẹo ngọt', 'Ăn đều bữa', 'Theo dõi đường huyết', 'Tham khảo ý kiến bác sĩ'],
            'Hypothyroidism': ['Dùng thuốc hormone', 'Khám định kỳ', 'Chế độ ăn giàu i-ốt', 'Tập thể dục vừa phải'],
            'Impetigo': ['Giữ vệ sinh', 'Không gãi', 'Dùng thuốc kháng sinh', 'Tránh lây nhiễm'],
            'Jaundice': ['Khám gan ngay', 'Nghỉ ngơi', 'Chế độ ăn nhẹ', 'Uống nhiều nước'],
            'Malaria': ['Ngủ màn', 'Dùng thuốc phòng', 'Diệt muỗi', 'Tìm kiếm sự chăm sóc y tế'],
            'Osteoarthristis': ['Tập thể dục nhẹ', 'Giảm cân', 'Vật lý trị liệu', 'Dùng thuốc giảm đau'],
            'Paralysis (brain hemorrhage)': ['Gọi cấp cứu ngay', 'Nghỉ ngơi hoàn toàn', 'Vật lý trị liệu', 'Khám định kỳ'],
            'Peptic ulcer diseae': ['Tránh thức ăn cay', 'Ăn đều bữa', 'Dùng thuốc theo chỉ định', 'Giảm stress'],
            'Pneumonia': ['Nghỉ ngơi hoàn toàn', 'Uống nhiều nước', 'Dùng thuốc kháng sinh', 'Tìm kiếm sự chăm sóc y tế'],
            'Psoriasis': ['Giữ ẩm da', 'Tránh stress', 'Dùng thuốc theo chỉ định', 'Tắm nắng vừa phải'],
            'Tuberculosis': ['Dùng thuốc đều đặn', 'Cách ly', 'Khám định kỳ', 'Chế độ ăn giàu dinh dưỡng'],
            'Typhoid': ['Vệ sinh ăn uống', 'Uống nước sạch', 'Dùng thuốc kháng sinh', 'Nghỉ ngơi đầy đủ'],
            'Urinary tract infection': ['Uống nhiều nước', 'Vệ sinh sạch sẽ', 'Dùng thuốc kháng sinh', 'Tránh nhịn tiểu'],
            'Varicose veins': ['Nâng chân cao', 'Mang vớ ép', 'Tập thể dục', 'Tránh đứng lâu'],
            'hepatitis A': ['Vệ sinh ăn uống', 'Tiêm vaccine', 'Nghỉ ngơi', 'Chế độ ăn nhẹ']
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
            
            description = self.disease_descriptions.get(predicted_disease, self.auto_translate_description(predicted_disease))
            precautions = self.disease_precautions.get(predicted_disease, self.auto_translate_precautions(predicted_disease))
            
            disease_vn = self.disease_translations.get(predicted_disease, self.auto_translate_disease(predicted_disease))
            
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
            # Check if we have a Vietnamese translation
            if symptom in self.symptom_translations:
                vn_name = self.symptom_translations[symptom]
            else:
                # Auto-translate if not in our dictionary
                vn_name = self.auto_translate_symptom(symptom)
            symptoms_vn.append({
                'en': symptom,
                'vn': vn_name
            })
        return symptoms_vn
    
    def auto_translate_symptom(self, symptom):
        """Auto-translate symptom names to Vietnamese"""
        # Common medical terms translation
        translations = {
            'pain': 'Đau',
            'ache': 'Đau',
            'discomfort': 'Khó chịu',
            'swelling': 'Sưng',
            'inflammation': 'Viêm',
            'infection': 'Nhiễm trùng',
            'fever': 'Sốt',
            'cough': 'Ho',
            'sneezing': 'Hắt hơi',
            'runny': 'Chảy',
            'congestion': 'Nghẹt',
            'breathlessness': 'Khó thở',
            'shortness': 'Khó',
            'nausea': 'Buồn nôn',
            'vomiting': 'Nôn',
            'diarrhea': 'Tiêu chảy',
            'constipation': 'Táo bón',
            'urination': 'Tiểu',
            'burning': 'Buốt',
            'itching': 'Ngứa',
            'rash': 'Phát ban',
            'blister': 'Phồng rộp',
            'bruise': 'Bầm tím',
            'chills': 'Ớn lạnh',
            'fatigue': 'Mệt mỏi',
            'weakness': 'Yếu',
            'dizziness': 'Chóng mặt',
            'headache': 'Đau đầu',
            'migraine': 'Đau nửa đầu',
            'anxiety': 'Lo lắng',
            'depression': 'Trầm cảm',
            'irritability': 'Cáu gắt',
            'lethargy': 'Lờ đờ',
            'malaise': 'Khó chịu',
            'loss': 'Mất',
            'gain': 'Tăng',
            'decrease': 'Giảm',
            'increase': 'Tăng',
            'abnormal': 'Bất thường',
            'irregular': 'Không đều',
            'continuous': 'Liên tục',
            'intermittent': 'Từng cơn',
            'severe': 'Nghiêm trọng',
            'mild': 'Nhẹ',
            'acute': 'Cấp',
            'chronic': 'Mạn tính',
            'failure': 'Suy',
            'liver': 'Gan',
            'bladder': 'Bàng quang',
            'bloody': 'Có máu',
            'stool': 'Phân',
            'brittle': 'Giòn',
            'nails': 'Móng tay',
            'coma': 'Hôn mê',
            'feel': 'Cảm giác',
            'urine': 'Nước tiểu',
            'cramps': 'Chuột rút',
            'distention': 'Chướng',
            'abdomen': 'Bụng',
            'enlarged': 'To',
            'thyroid': 'Tuyến giáp',
            'family': 'Gia đình',
            'history': 'Tiền sử',
            'fluid': 'Dịch',
            'overload': 'Quá tải',
            'alcohol': 'Rượu',
            'consumption': 'Tiêu thụ',
            'inflammatory': 'Viêm',
            'internal': 'Trong',
            'sugar': 'Đường',
            'level': 'Mức',
            'irritation': 'Kích ứng',
            'anus': 'Hậu môn',
            'knee': 'Đầu gối',
            'concentration': 'Tập trung',
            'appetite': 'Cảm giác thèm ăn',
            'balance': 'Thăng bằng',
            'smell': 'Khứu giác',
            'mood': 'Tâm trạng',
            'swings': 'Thay đổi',
            'movement': 'Chuyển động',
            'stiffness': 'Cứng',
            'mucoid': 'Nhầy',
            'sputum': 'Đờm',
            'wasting': 'Teo',
            'neck': 'Cổ',
            'nodal': 'Hạch',
            'skin': 'Da',
            'eruptions': 'Nổi mẩn',
            'obesity': 'Béo phì',
            'behind': 'Sau',
            'eyes': 'Mắt',
            'during': 'Trong khi',
            'bowel': 'Ruột',
            'movements': 'Vận động',
            'anal': 'Hậu môn',
            'region': 'Vùng',
            'walking': 'Đi lại',
            'palpitations': 'Đánh trống ngực',
            'passage': 'Thải',
            'gases': 'Hơi',
            'patches': 'Đốm',
            'throat': 'Họng',
            'phlegm': 'Đờm',
            'polyuria': 'Tiểu nhiều',
            'prominent': 'Nổi',
            'veins': 'Tĩnh mạch',
            'calf': 'Bắp chân',
            'puffy': 'Sưng',
            'face': 'Mặt',
            'pus': 'Mủ',
            'filled': 'Chứa',
            'pimples': 'Mụn',
            'receiving': 'Nhận',
            'blood': 'Máu',
            'transfusion': 'Truyền',
            'unsterile': 'Không vô trùng',
            'injections': 'Tiêm',
            'red': 'Đỏ',
            'sore': 'Loét',
            'around': 'Quanh',
            'nose': 'Mũi',
            'spots': 'Đốm',
            'body': 'Cơ thể',
            'redness': 'Đỏ',
            'rusty': 'Rỉ sắt',
            'scurring': 'Sẹo',
            'shivering': 'Run rẩy',
            'silver': 'Bạc',
            'like': 'Như',
            'dusting': 'Bụi',
            'sinus': 'Xoang',
            'pressure': 'Áp lực',
            'peeling': 'Bong',
            'slurred': 'Lắp',
            'speech': 'Nói',
            'small': 'Nhỏ',
            'dents': 'Lõm',
            'spinning': 'Xoay',
            'spotting': 'Nhỏ giọt',
            'stiff': 'Cứng',
            'stomach': 'Dạ dày',
            'bleeding': 'Chảy máu',
            'sunken': 'Lõm',
            'sweating': 'Đổ mồ hôi',
            'swelled': 'Sưng',
            'lymph': 'Bạch huyết',
            'nodes': 'Hạch',
            'joints': 'Khớp',
            'stomach': 'Bụng',
            'swollen': 'Sưng',
            'vessels': 'Mạch máu',
            'extremeties': 'Chi',
            'legs': 'Chân',
            'irritation': 'Kích ứng',
            'toxic': 'Nhiễm độc',
            'look': 'Vẻ',
            'typhos': 'Thương hàn',
            'ulcers': 'Loét',
            'tongue': 'Lưỡi',
            'unsteadiness': 'Không vững',
            'visual': 'Thị giác',
            'disturbances': 'Rối loạn',
            'watering': 'Chảy nước',
            'limbs': 'Chi',
            'side': 'Bên',
            'weight': 'Cân nặng',
            'yellow': 'Vàng',
            'crust': 'Vảy',
            'ooze': 'Chảy dịch',
            'yellowing': 'Vàng',
            'yellowish': 'Vàng nhạt'
        }
        
        # Convert to lowercase and replace underscores
        symptom_lower = symptom.lower().replace('_', ' ')
        
        # Try to translate common patterns
        for eng, vn in translations.items():
            if eng in symptom_lower:
                symptom_lower = symptom_lower.replace(eng, vn)
        
        # Capitalize first letter and return
        return symptom_lower.title()
    
    def get_available_diseases(self) -> List[str]:
        return sorted(self.diseases_list)
    
    def get_available_diseases_vn(self) -> List[Dict]:
        diseases_vn = []
        for disease in sorted(self.diseases_list):
            # Check if we have a Vietnamese translation
            if disease in self.disease_translations:
                vn_name = self.disease_translations[disease]
            else:
                # Auto-translate if not in our dictionary
                vn_name = self.auto_translate_disease(disease)
            diseases_vn.append({
                'en': disease,
                'vn': vn_name
            })
        return diseases_vn
    
    def auto_translate_disease(self, disease):
        """Auto-translate disease names to Vietnamese"""
        # Common disease terms translation
        translations = {
            'hepatitis': 'Viêm gan',
            'diabetes': 'Tiểu đường',
            'hypertension': 'Tăng huyết áp',
            'asthma': 'Hen phế quản',
            'arthritis': 'Viêm khớp',
            'pneumonia': 'Viêm phổi',
            'tuberculosis': 'Bệnh lao',
            'malaria': 'Sốt rét',
            'dengue': 'Sốt xuất huyết',
            'typhoid': 'Thương hàn',
            'cholera': 'Tả',
            'influenza': 'Cúm',
            'cold': 'Cảm lạnh',
            'fever': 'Sốt',
            'infection': 'Nhiễm trùng',
            'ulcer': 'Loét',
            'cancer': 'Ung thư',
            'tumor': 'Khối u',
            'cyst': 'U nang',
            'abscess': 'Áp xe',
            'allergy': 'Dị ứng',
            'anemia': 'Thiếu máu',
            'obesity': 'Béo phì',
            'anorexia': 'Chán ăn',
            'bulimia': 'Ăn ói',
            'depression': 'Trầm cảm',
            'anxiety': 'Rối loạn lo âu',
            'schizophrenia': 'Tâm thần phân liệt',
            'epilepsy': 'Động kinh',
            'stroke': 'Đột quỵ',
            'heart attack': 'Đau tim',
            'angina': 'Đau thắt ngực',
            'arrhythmia': 'Rối loạn nhịp tim',
            'kidney': 'Thận',
            'liver': 'Gan',
            'pancreas': 'Tụy',
            'thyroid': 'Tuyến giáp',
            'adrenal': 'Tuyến thượng thận',
            'pituitary': 'Tuyến yên',
            'chronic': 'Mạn tính',
            'acute': 'Cấp tính',
            'benign': 'Lành tính',
            'malignant': 'Ác tính'
        }
        
        # Convert to lowercase
        disease_lower = disease.lower()
        
        # Try to translate common patterns
        for eng, vn in translations.items():
            if eng in disease_lower:
                disease_lower = disease_lower.replace(eng, vn)
        
        # Capitalize first letter and return
        return disease_lower.title()
    
    def auto_translate_description(self, disease):
        """Auto-translate disease description to Vietnamese"""
        # Common medical descriptions
        descriptions = {
            'Common Cold': 'Nhiễm virus đường hô hấp trên gây ra các triệu chứng nhẹ như ho, sổ mũi, đau họng.',
            'Influenza': 'Nhiễm virus tấn công hệ hô hấp với triệu chứng sốt cao, đau cơ, mệt mỏi.',
            'Gastroenteritis': 'Viêm dạ dày và ruột gây tiêu chảy, nôn mửa, đau bụng.',
            'Hypertension': 'Huyết áp cao có thể dẫn đến các vấn đề tim mạch nghiêm trọng.',
            'Diabetes': 'Bệnh rối loạn chuyển hóa glucose, ảnh hưởng đến lượng đường trong máu.',
            'Migraine': 'Đau đầu dữ dội một bên, thường kèm theo buồn nôn và nhạy cảm với ánh sáng.',
            'Hepatitis': 'Viêm gan do virus hoặc các nguyên nhân khác, ảnh hưởng đến chức năng gan.',
            'Asthma': 'Bệnh viêm đường hô hấp mạn tính, gây khó thở và thở khò khè.',
            'Arthritis': 'Viêm khớp gây đau, sưng và cứng khớp, ảnh hưởng đến khả năng vận động.',
            'Pneumonia': 'Viêm phổi, nhiễm trùng phổi nghiêm trọng cần điều trị kháng sinh.',
            'Tuberculosis': 'Bệnh lao, nhiễm trùng phổi do vi khuẩn Mycobacterium tuberculosis.',
            'Malaria': 'Bệnh truyền nhiễm do ký sinh trùng Plasmodium, lây qua muỗi.',
            'Dengue': 'Bệnh truyền nhiễm do virus Dengue, lây qua muỗi Aedes.',
            'Typhoid': 'Bệnh thương hàn, nhiễm trùng đường ruột do vi khuẩn Salmonella.',
            'Urinary tract infection': 'Nhiễm trùng đường tiết niệu, thường gây tiểu buốt và đau.',
            'Skin infection': 'Nhiễm trùng da do vi khuẩn, nấm hoặc virus.',
            'Eye infection': 'Nhiễm trùng mắt có thể ảnh hưởng đến thị lực.',
            'Ear infection': 'Nhiễm trùng tai gây đau và có thể ảnh hưởng đến thính giác.',
            'Sinus infection': 'Viêm xoang, nhiễm trùng các khoang xoang trong hộp sọ.',
            'Throat infection': 'Viêm họng, nhiễm trùng cổ họng gây đau và khó nuốt.'
        }
        
        # Check if we have a specific description
        if disease in descriptions:
            return descriptions[disease]
        
        # Generate a generic description based on disease name
        disease_lower = disease.lower()
        
        if 'hepatitis' in disease_lower:
            return f'Viêm gan {disease.replace("Hepatitis", "").strip()} - bệnh viêm gan do virus hoặc các nguyên nhân khác.'
        elif 'diabetes' in disease_lower:
            return 'Bệnh rối loạn chuyển hóa glucose, ảnh hưởng đến lượng đường trong máu.'
        elif 'hypertension' in disease_lower:
            return 'Huyết áp cao, yếu tố nguy cơ chính của bệnh tim mạch.'
        elif 'asthma' in disease_lower:
            return 'Bệnh viêm đường hô hấp mạn tính, gây khó thở và thở khò khè.'
        elif 'arthritis' in disease_lower:
            return 'Viêm khớp gây đau, sưng và cứng khớp, ảnh hưởng đến khả năng vận động.'
        elif 'infection' in disease_lower:
            return f'Nhiễm trùng {disease.replace("infection", "").strip()} - cần điều trị kháng sinh phù hợp.'
        elif 'pain' in disease_lower:
            return f'Đau {disease.replace("pain", "").strip()} - có thể do nhiều nguyên nhân khác nhau.'
        elif 'fever' in disease_lower:
            return f'Sốt {disease.replace("fever", "").strip()} - có thể do nhiễm trùng hoặc các bệnh khác.'
        else:
            return f'Bệnh {disease} - cần tham khảo ý kiến bác sĩ để có chẩn đoán chính xác.'
    
    def auto_translate_precautions(self, disease):
        """Auto-translate disease precautions to Vietnamese"""
        # Common precautions based on disease type
        disease_lower = disease.lower()
        
        if 'hepatitis' in disease_lower:
            return ['Ngừng uống rượu hoàn toàn', 'Chế độ ăn lành mạnh', 'Khám gan định kỳ', 'Tập thể dục vừa phải']
        elif 'diabetes' in disease_lower:
            return ['Theo dõi đường huyết', 'Chế độ ăn kiêng', 'Tập thể dục', 'Dùng thuốc đúng giờ']
        elif 'hypertension' in disease_lower:
            return ['Giảm muối', 'Tập thể dục', 'Giảm cân', 'Dùng thuốc đều đặn']
        elif 'asthma' in disease_lower:
            return ['Tránh chất kích thích', 'Dùng thuốc hít theo chỉ định', 'Tập thở', 'Khám định kỳ']
        elif 'arthritis' in disease_lower:
            return ['Tập thể dục nhẹ nhàng', 'Giữ ấm khớp', 'Dùng thuốc giảm đau', 'Vật lý trị liệu']
        elif 'infection' in disease_lower:
            return ['Dùng thuốc kháng sinh', 'Vệ sinh sạch sẽ', 'Nghỉ ngơi đầy đủ', 'Tăng cường miễn dịch']
        elif 'fever' in disease_lower:
            return ['Nghỉ ngơi', 'Uống nhiều nước', 'Dùng thuốc hạ sốt', 'Theo dõi nhiệt độ']
        elif 'pain' in disease_lower:
            return ['Dùng thuốc giảm đau', 'Nghỉ ngơi', 'Chườm ấm/lạnh', 'Tránh vận động mạnh']
        elif 'cold' in disease_lower or 'flu' in disease_lower:
            return ['Nghỉ ngơi đầy đủ', 'Uống nhiều nước', 'Dùng thuốc không kê đơn', 'Tránh tiếp xúc với người khác']
        elif 'gastroenteritis' in disease_lower:
            return ['Uống nhiều nước', 'Nghỉ ngơi', 'Tránh thức ăn rắn ban đầu', 'Tìm kiếm sự chăm sóc y tế nếu nghiêm trọng']
        else:
            return ['Tham khảo ý kiến bác sĩ', 'Nghỉ ngơi', 'Uống nhiều nước', 'Theo dõi triệu chứng']
    
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





























