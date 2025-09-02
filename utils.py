import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime

class HealthAssessmentEngine:
    """Engine for assessing health symptoms and providing recommendations"""
    
    def __init__(self):
        self.red_flags = self._load_red_flags()
        self.topics = self._load_topics()
        self.rules = self._load_rules()
    
    def _load_red_flags(self) -> Dict[str, Any]:
        """Load red flags data"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'red_flags.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading red flags: {e}")
            return {}
    
    def _load_topics(self) -> List[Dict[str, Any]]:
        """Load health topics data"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'topics.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading topics: {e}")
            return []
    
    def _load_rules(self) -> Dict[str, Any]:
        """Load assessment rules"""
        try:
            data_path = os.path.join(os.path.dirname(__file__), 'data', 'rules.json')
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading rules: {e}")
            return {}
    
    def assess_symptoms(self, symptoms_text: str, age: int, days_sick: int, 
                       user_health_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Assess symptoms and provide recommendations"""
        symptoms_lower = symptoms_text.lower()
        
        # Check for emergency red flags
        emergency_result = self._check_emergency_flags(symptoms_lower)
        if emergency_result:
            return emergency_result
        
        # Check for high priority symptoms
        high_priority_result = self._check_high_priority_flags(symptoms_lower)
        if high_priority_result:
            return high_priority_result
        
        # Age-based assessment
        age_result = self._check_age_based_rules(age)
        if age_result:
            return age_result
        
        # Duration-based assessment
        duration_result = self._check_duration_rules(days_sick)
        if duration_result:
            return duration_result
        
        # Find relevant health topics
        relevant_topics = self._find_relevant_topics(symptoms_lower)
        
        # Get personalized recommendations
        personalized_recommendations = self._get_personalized_recommendations(
            symptoms_lower, user_health_info
        )
        
        # Default: home care
        result = {
            'priority': 'home_care',
            'message': 'Có thể chăm sóc tại nhà',
            'description': 'Triệu chứng có thể được chăm sóc tại nhà với các biện pháp phù hợp.',
            'color': 'success',
            'recommendations': ['Nghỉ ngơi đầy đủ', 'Uống nhiều nước', 'Theo dõi triệu chứng'],
            'topics': relevant_topics
        }
        
        if personalized_recommendations:
            result['personalized_recommendations'] = personalized_recommendations
        
        return result
    
    def _check_emergency_flags(self, symptoms_lower: str) -> Optional[Dict[str, Any]]:
        """Check for emergency symptoms"""
        emergency_keywords = self.red_flags.get('emergency_keywords', [])
        for keyword in emergency_keywords:
            if keyword.lower() in symptoms_lower:
                return {
                    'priority': 'emergency',
                    'message': 'CẦN ĐI CẤP CỨU NGAY!',
                    'description': f'Phát hiện dấu hiệu khẩn cấp: "{keyword}". Vui lòng đến bệnh viện gần nhất hoặc gọi 115.',
                    'color': 'danger',
                    'recommendations': self.red_flags.get('emergency_actions', [])
                }
        return None
    
    def _check_high_priority_flags(self, symptoms_lower: str) -> Optional[Dict[str, Any]]:
        """Check for high priority symptoms"""
        high_priority_keywords = self.red_flags.get('high_priority_keywords', [])
        for keyword in high_priority_keywords:
            if keyword.lower() in symptoms_lower:
                return {
                    'priority': 'high',
                    'message': 'Cần khám bác sĩ sớm',
                    'description': f'Triệu chứng "{keyword}" cần được đánh giá bởi bác sĩ trong vòng 24-48 giờ.',
                    'color': 'warning',
                    'recommendations': self.red_flags.get('high_priority_actions', [])
                }
        return None
    
    def _check_age_based_rules(self, age: int) -> Optional[Dict[str, Any]]:
        """Check age-based rules"""
        min_age = self.rules.get('min_age', 0)
        if age < min_age:
            return {
                'priority': 'consult_doctor',
                'message': 'Cần tư vấn bác sĩ',
                'description': f'Trẻ em dưới {min_age} tuổi cần được đánh giá bởi bác sĩ nhi khoa.',
                'color': 'info',
                'recommendations': ['Liên hệ bác sĩ nhi khoa', 'Không tự ý dùng thuốc']
            }
        return None
    
    def _check_duration_rules(self, days_sick: int) -> Optional[Dict[str, Any]]:
        """Check duration-based rules"""
        max_days_home = self.rules.get('max_days_home', 7)
        if days_sick > max_days_home:
            return {
                'priority': 'consult_doctor',
                'message': 'Cần tư vấn bác sĩ',
                'description': f'Triệu chứng kéo dài {days_sick} ngày, vượt quá thời gian tự điều trị tại nhà.',
                'color': 'info',
                'recommendations': ['Liên hệ bác sĩ để được tư vấn', 'Không tự ý dùng thuốc kéo dài']
            }
        return None
    
    def _find_relevant_topics(self, symptoms_lower: str) -> List[Dict[str, Any]]:
        """Find relevant health topics based on symptoms"""
        relevant_topics = []
        for topic in self.topics:
            if any(keyword.lower() in symptoms_lower for keyword in topic.get('keywords', [])):
                relevant_topics.append(topic)
        return relevant_topics
    
    def _get_personalized_recommendations(self, symptoms: str, 
                                        user_health_info: Optional[Dict[str, Any]]) -> Optional[List[str]]:
        """Get personalized recommendations based on user health data"""
        if not user_health_info:
            return None
        
        recommendations = []
        
        # Weight-based recommendations
        if user_health_info.get('weight'):
            if user_health_info['weight'] > 80:
                recommendations.append('Duy trì chế độ ăn cân bằng và tập thể dục đều đặn')
            elif user_health_info['weight'] < 50:
                recommendations.append('Tăng cường dinh dưỡng và protein trong chế độ ăn')
        
        # Age-based recommendations
        age = user_health_info.get('age', 0)
        if age > 60:
            recommendations.append('Khám sức khỏe định kỳ và theo dõi huyết áp')
        elif age < 18:
            recommendations.append('Đảm bảo ngủ đủ giấc và dinh dưỡng phù hợp với lứa tuổi')
        
        # Gender-specific recommendations
        if user_health_info.get('gender') == 'female':
            recommendations.append('Chú ý đến sức khỏe xương và canxi')
        elif user_health_info.get('gender') == 'male':
            recommendations.append('Kiểm tra sức khỏe tim mạch định kỳ')
        
        return recommendations

class HealthAnalyzer:
    """Analyze user health data and provide insights"""
    
    @staticmethod
    def analyze_user_health(user_health_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user health data and provide insights"""
        if not user_health_info:
            return {}
        
        analysis = {}
        
        # BMI calculation
        if user_health_info.get('height') and user_health_info.get('weight'):
            height_m = user_health_info['height'] / 100
            bmi = user_health_info['weight'] / (height_m * height_m)
            analysis['bmi'] = round(bmi, 1)
            
            if bmi < 18.5:
                analysis['bmi_status'] = 'Thiếu cân'
            elif bmi < 25:
                analysis['bmi_status'] = 'Bình thường'
            elif bmi < 30:
                analysis['bmi_status'] = 'Thừa cân'
            else:
                analysis['bmi_status'] = 'Béo phì'
        
        # Age-based recommendations
        age = user_health_info.get('age', 0)
        if age < 18:
            analysis['age_group'] = 'Trẻ em/Vị thành niên'
        elif age < 65:
            analysis['age_group'] = 'Người trưởng thành'
        else:
            analysis['age_group'] = 'Người cao tuổi'
        
        return analysis
    
    @staticmethod
    def get_health_guidance(user_health_info: Dict[str, Any]) -> Dict[str, List[str]]:
        """Get comprehensive health guidance based on user data"""
        if not user_health_info:
            return {}
        
        guidance = {
            'general_tips': [],
            'lifestyle_recommendations': [],
            'preventive_measures': []
        }
        
        # General health tips
        guidance['general_tips'].extend([
            'Duy trì chế độ ăn uống cân bằng và đa dạng',
            'Tập thể dục ít nhất 30 phút mỗi ngày',
            'Ngủ đủ 7-9 giờ mỗi đêm',
            'Uống đủ nước (2-3 lít/ngày)'
        ])
        
        # Age-specific recommendations
        age = user_health_info.get('age', 0)
        if age > 50:
            guidance['preventive_measures'].extend([
                'Khám sức khỏe định kỳ 6 tháng/lần',
                'Kiểm tra huyết áp và cholesterol'
            ])
        elif age < 30:
            guidance['lifestyle_recommendations'].extend([
                'Xây dựng thói quen tập thể dục từ sớm',
                'Hạn chế rượu bia và thuốc lá'
            ])
        
        return guidance

# Initialize assessment engine
assessment_engine = HealthAssessmentEngine()
health_analyzer = HealthAnalyzer()
