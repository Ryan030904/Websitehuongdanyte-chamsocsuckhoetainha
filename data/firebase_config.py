import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import json

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account"""
    try:
        # Check if Firebase is already initialized
        if not firebase_admin._apps:
            # Use service account key file if available
            service_account_path = "firebase-service-account.json"
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
                firebase_admin.initialize_app(cred)
            else:
                # Use environment variables or default credentials
                firebase_admin.initialize_app()
        
        # Get Firestore client
        db = firestore.client()
        print("✅ Firebase initialized successfully")
        return db
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        return None

# Database operations
class FirebaseDB:
    def __init__(self):
        self.db = initialize_firebase()
    
    def save_user(self, user_data):
        """Save user data to Firestore"""
        try:
            if not self.db:
                return False
            
            user_ref = self.db.collection('người dùng').document(str(user_data['id']))
            
            # Enhanced user data with more fields
            enhanced_user_data = {
                'id': user_data['id'],
                'email': user_data.get('email', ''),
                'display_name': user_data.get('display_name', ''),
                'username': user_data.get('username', ''),
                'gender': user_data.get('gender', ''),
                'age': user_data.get('age', 0),
                'height': user_data.get('height', 0),
                'weight': user_data.get('weight', 0),
                'medical_history': user_data.get('medical_history', ''),
                'phone': user_data.get('phone', ''),
                'address': user_data.get('address', ''),
                'emergency_contact': user_data.get('emergency_contact', ''),
                'blood_type': user_data.get('blood_type', ''),
                'allergies': user_data.get('allergies', ''),
                'medications': user_data.get('medications', ''),
                'is_admin': user_data.get('is_admin', False),
                'is_active': user_data.get('is_active', True),
                'last_login': user_data.get('last_login'),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            user_ref.set(enhanced_user_data)
            print(f"✅ User {user_data['id']} saved to Firebase with enhanced data")
            return True
        except Exception as e:
            print(f"❌ Error saving user: {e}")
            return False
    
    def save_assessment(self, assessment_data):
        """Save health assessment to Firestore"""
        try:
            if not self.db:
                return False
            
            assessment_ref = self.db.collection('đánh giá').document(str(assessment_data['id']))
            
            # Enhanced assessment data with more fields
            enhanced_assessment_data = {
                'id': assessment_data['id'],
                'user_id': assessment_data.get('user_id', 0),
                'user_email': assessment_data.get('user_email', ''),
                'user_name': assessment_data.get('user_name', ''),
                'symptoms': assessment_data.get('symptoms', ''),
                'symptoms_list': assessment_data.get('symptoms_list', []),
                'age_at_assessment': assessment_data.get('age_at_assessment', 0),
                'days_sick': assessment_data.get('days_sick', 0),
                'priority': assessment_data.get('priority', ''),
                'message': assessment_data.get('message', ''),
                'description': assessment_data.get('description', ''),
                'recommendations': assessment_data.get('recommendations', ''),
                'ai_diagnosis': assessment_data.get('ai_diagnosis', {}),
                'severity_score': assessment_data.get('severity_score', 0),
                'confidence_level': assessment_data.get('confidence_level', 0),
                'disease_predicted': assessment_data.get('disease_predicted', ''),
                'precautions': assessment_data.get('precautions', []),
                'follow_up_needed': assessment_data.get('follow_up_needed', False),
                'follow_up_date': assessment_data.get('follow_up_date', ''),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            assessment_ref.set(enhanced_assessment_data)
            print(f"✅ Assessment {assessment_data['id']} saved to Firebase with enhanced data")
            return True
        except Exception as e:
            print(f"❌ Error saving assessment: {e}")
            return False
    
    def save_contact(self, contact_data):
        """Save contact message to Firestore"""
        try:
            if not self.db:
                return False
            
            contact_ref = self.db.collection('liên hệ').document(str(contact_data['id']))
            
            # Enhanced contact data with more fields
            enhanced_contact_data = {
                'id': contact_data['id'],
                'name': contact_data.get('name', ''),
                'email': contact_data.get('email', ''),
                'phone': contact_data.get('phone', ''),
                'subject': contact_data.get('subject', ''),
                'message': contact_data.get('message', ''),
                'category': contact_data.get('category', 'general'),
                'priority': contact_data.get('priority', 'normal'),
                'status': contact_data.get('status', 'new'),
                'assigned_to': contact_data.get('assigned_to', ''),
                'response': contact_data.get('response', ''),
                'response_date': contact_data.get('response_date', ''),
                'user_agent': contact_data.get('user_agent', ''),
                'ip_address': contact_data.get('ip_address', ''),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            contact_ref.set(enhanced_contact_data)
            print(f"✅ Contact {contact_data['id']} saved to Firebase with enhanced data")
            return True
        except Exception as e:
            print(f"❌ Error saving contact: {e}")
            return False
    
    def get_user_history(self, user_id):
        """Get user's health assessment history"""
        try:
            if not self.db:
                return []
            
            assessments = self.db.collection('đánh giá').where('user_id', '==', user_id).order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            history = []
            for assessment in assessments:
                data = assessment.to_dict()
                data['id'] = assessment.id
                history.append(data)
            
            return history
        except Exception as e:
            print(f"❌ Error getting user history: {e}")
            return []
    
    def get_all_users(self):
        """Get all users from Firestore"""
        try:
            if not self.db:
                return []
            
            users = self.db.collection('người dùng').stream()
            
            user_list = []
            for user in users:
                data = user.to_dict()
                data['id'] = user.id
                user_list.append(data)
            
            return user_list
        except Exception as e:
            print(f"❌ Error getting users: {e}")
            return []
    
    def get_all_assessments(self):
        """Get all health assessments from Firestore"""
        try:
            if not self.db:
                return []
            
            assessments = self.db.collection('đánh giá').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            assessment_list = []
            for assessment in assessments:
                data = assessment.to_dict()
                data['id'] = assessment.id
                assessment_list.append(data)
            
            return assessment_list
        except Exception as e:
            print(f"❌ Error getting assessments: {e}")
            return []
    
    def get_all_contacts(self):
        """Get all contact messages from Firestore"""
        try:
            if not self.db:
                return []
            
            contacts = self.db.collection('liên hệ').order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            contact_list = []
            for contact in contacts:
                data = contact.to_dict()
                data['id'] = contact.id
                contact_list.append(data)
            
            return contact_list
        except Exception as e:
            print(f"❌ Error getting contacts: {e}")
            return []
    
    def update_user(self, user_id, update_data):
        """Update user data in Firestore"""
        try:
            if not self.db:
                return False
            
            user_ref = self.db.collection('người dùng').document(str(user_id))
            update_data['last_sync'] = datetime.now()
            
            user_ref.update(update_data)
            print(f"✅ User {user_id} updated in Firebase")
            return True
        except Exception as e:
            print(f"❌ Error updating user: {e}")
            return False
    
    def delete_user(self, user_id):
        """Delete user from Firestore"""
        try:
            if not self.db:
                return False
            
            user_ref = self.db.collection('người dùng').document(str(user_id))
            user_ref.delete()
            print(f"✅ User {user_id} deleted from Firebase")
            return True
        except Exception as e:
            print(f"❌ Error deleting user: {e}")
            return False
    
    def get_statistics(self):
        """Get statistics from Firestore"""
        try:
            if not self.db:
                return {}
            
            # Get counts for all collections
            users_count = len(list(self.db.collection('người dùng').stream()))
            assessments_count = len(list(self.db.collection('đánh giá').stream()))
            contacts_count = len(list(self.db.collection('liên hệ').stream()))
            health_records_count = len(list(self.db.collection('hồ_sơ_sức_khỏe').stream()))
            appointments_count = len(list(self.db.collection('lịch_hẹn').stream()))
            notifications_count = len(list(self.db.collection('thông_báo').stream()))
            
            # Get recent activity
            recent_assessments = list(self.db.collection('đánh giá').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream())
            recent_contacts = list(self.db.collection('liên hệ').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream())
            recent_health_records = list(self.db.collection('hồ_sơ_sức_khỏe').order_by('created_at', direction=firestore.Query.DESCENDING).limit(5).stream())
            
            stats = {
                'total_users': users_count,
                'total_assessments': assessments_count,
                'total_contacts': contacts_count,
                'total_health_records': health_records_count,
                'total_appointments': appointments_count,
                'total_notifications': notifications_count,
                'recent_assessments': [doc.to_dict() for doc in recent_assessments],
                'recent_contacts': [doc.to_dict() for doc in recent_contacts],
                'recent_health_records': [doc.to_dict() for doc in recent_health_records]
            }
            
            return stats
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}

    def save_health_record(self, record_data):
        """Save health record to Firestore"""
        try:
            if not self.db:
                return False
            
            record_ref = self.db.collection('hồ_sơ_sức_khỏe').document(str(record_data['id']))
            
            enhanced_record_data = {
                'id': record_data['id'],
                'user_id': record_data.get('user_id', 0),
                'user_email': record_data.get('user_email', ''),
                'record_type': record_data.get('record_type', 'general'),
                'title': record_data.get('title', ''),
                'description': record_data.get('description', ''),
                'symptoms': record_data.get('symptoms', ''),
                'diagnosis': record_data.get('diagnosis', ''),
                'treatment': record_data.get('treatment', ''),
                'medications': record_data.get('medications', []),
                'test_results': record_data.get('test_results', {}),
                'doctor_name': record_data.get('doctor_name', ''),
                'hospital': record_data.get('hospital', ''),
                'visit_date': record_data.get('visit_date', ''),
                'next_visit': record_data.get('next_visit', ''),
                'attachments': record_data.get('attachments', []),
                'notes': record_data.get('notes', ''),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            record_ref.set(enhanced_record_data)
            print(f"✅ Health record {record_data['id']} saved to Firebase")
            return True
        except Exception as e:
            print(f"❌ Error saving health record: {e}")
            return False

    def save_appointment(self, appointment_data):
        """Save appointment to Firestore"""
        try:
            if not self.db:
                return False
            
            appointment_ref = self.db.collection('lịch_hẹn').document(str(appointment_data['id']))
            
            enhanced_appointment_data = {
                'id': appointment_data['id'],
                'user_id': appointment_data.get('user_id', 0),
                'user_email': appointment_data.get('user_email', ''),
                'appointment_type': appointment_data.get('appointment_type', 'consultation'),
                'doctor_name': appointment_data.get('doctor_name', ''),
                'specialty': appointment_data.get('specialty', ''),
                'appointment_date': appointment_data.get('appointment_date', ''),
                'appointment_time': appointment_data.get('appointment_time', ''),
                'duration': appointment_data.get('duration', 30),
                'location': appointment_data.get('location', ''),
                'reason': appointment_data.get('reason', ''),
                'symptoms': appointment_data.get('symptoms', ''),
                'status': appointment_data.get('status', 'scheduled'),
                'notes': appointment_data.get('notes', ''),
                'reminder_sent': appointment_data.get('reminder_sent', False),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            appointment_ref.set(enhanced_appointment_data)
            print(f"✅ Appointment {appointment_data['id']} saved to Firebase")
            return True
        except Exception as e:
            print(f"❌ Error saving appointment: {e}")
            return False

    def save_notification(self, notification_data):
        """Save notification to Firestore"""
        try:
            if not self.db:
                return False
            
            notification_ref = self.db.collection('thông_báo').document(str(notification_data['id']))
            
            enhanced_notification_data = {
                'id': notification_data['id'],
                'user_id': notification_data.get('user_id', 0),
                'user_email': notification_data.get('user_email', ''),
                'type': notification_data.get('type', 'general'),
                'title': notification_data.get('title', ''),
                'message': notification_data.get('message', ''),
                'priority': notification_data.get('priority', 'normal'),
                'read': notification_data.get('read', False),
                'action_url': notification_data.get('action_url', ''),
                'expires_at': notification_data.get('expires_at', ''),
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'last_sync': datetime.now()
            }
            
            notification_ref.set(enhanced_notification_data)
            print(f"✅ Notification {notification_data['id']} saved to Firebase")
            return True
        except Exception as e:
            print(f"❌ Error saving notification: {e}")
            return False

    def save_ai_diagnosis(self, diagnosis_data):
        """Save AI diagnosis result to Firestore"""
        try:
            if not self.db:
                return False
            
            # Generate unique ID for diagnosis
            diagnosis_id = f"ai_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{diagnosis_data.get('user_id', 'unknown')}"
            
            diagnosis_ref = self.db.collection('chẩn_đoán_ai').document(diagnosis_id)
            
            enhanced_diagnosis_data = {
                'id': diagnosis_id,
                'user_id': diagnosis_data.get('user_id', ''),
                'age': diagnosis_data.get('age', 0),
                'days_sick': diagnosis_data.get('days_sick', 0),
                'symptoms': diagnosis_data.get('symptoms', []),
                'custom_symptoms': diagnosis_data.get('custom_symptoms', ''),
                'profile_data': diagnosis_data.get('profile_data', {}),
                'diagnosis': diagnosis_data.get('diagnosis', {}),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            diagnosis_ref.set(enhanced_diagnosis_data)
            print(f"✅ AI Diagnosis {diagnosis_id} saved to Firebase")
            return True
        except Exception as e:
            print(f"❌ Error saving AI diagnosis: {e}")
            return False

    def get_user_diagnosis_history(self, user_id):
        """Get user's AI diagnosis history"""
        try:
            if not self.db:
                return []
            
            diagnosis_ref = self.db.collection('chẩn_đoán_ai')
            query = diagnosis_ref.where('user_id', '==', str(user_id)).order_by('created_at', direction=firestore.Query.DESCENDING)
            
            diagnoses = []
            for doc in query.stream():
                diagnosis_data = doc.to_dict()
                diagnosis_data['id'] = doc.id
                diagnoses.append(diagnosis_data)
            
            return diagnoses
        except Exception as e:
            print(f"❌ Error getting diagnosis history: {e}")
            return []

# Initialize Firebase DB instance
firebase_db = FirebaseDB()

