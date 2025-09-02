from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app, session
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from werkzeug.urls import url_parse
from models import db, User, HealthRecord, Assessment, Contact
from utils import assessment_engine, health_analyzer
from firebase_config import firebase_db
from ai_diagnosis import get_ai_diagnosis
import json
from datetime import datetime

# Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
api = Blueprint('api', __name__)
admin = Blueprint('admin', __name__)

# Main routes
@main.route('/')
def index():
    """Home page"""
    user_info = None
    if current_user.is_authenticated:
        user_info = current_user.to_dict()
        # Redirect admin to admin dashboard
        if current_user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
    return render_template('index.html', user_info=user_info)



@main.route('/resources')
def resources():
    """Legacy resources route -> redirect to new library page"""
    return redirect(url_for('main.library'))

@main.route('/privacy')
def privacy():
    """Privacy policy page"""
    return render_template('privacy.html')

@main.route('/contact')
def contact():
    """Legacy contact route -> redirect to new support page"""
    return redirect(url_for('main.support'))

# New content pages
@main.route('/guides')
def guides():
    """Care guides page"""
    return render_template('guides.html')

@main.route('/library')
def library():
    """Medical knowledge library page"""
    return render_template('library.html')

@main.route('/news')
def news():
    """Health news and blog page"""
    return render_template('news.html')

@main.route('/support')
def support():
    """Support and contact page"""
    return render_template('support.html')

@main.route('/profile')
@login_required
def profile():
    """User profile page"""
    return render_template('profile.html', user=current_user)

@main.route('/symptom-diagnosis')
def symptom_diagnosis():
    """Symptom diagnosis page with AI integration"""
    user = None
    if current_user.is_authenticated:
        user = current_user.to_dict()
    return render_template('symptom_diagnosis_ai.html', user=user)

# Auth routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Kiểm tra chế độ bảo trì
    try:
        import json
        import os
        settings_file = 'app_settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                if settings.get('maintenance_mode', False):
                    flash('Hệ thống đang trong chế độ bảo trì. Vui lòng thử lại sau.', 'warning')
                    return render_template('login.html')
    except:
        pass
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        print(f"[DEBUG] Login attempt for email: {email}")
        
        # Kiểm tra giới hạn đăng nhập sai
        failed_attempts_key = f'failed_login_{email}'
        failed_attempts = session.get(failed_attempts_key, 0)
        
        # Lấy cài đặt bảo mật
        try:
            import json
            import os
            settings_file = 'app_settings.json'
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    max_attempts = settings.get('login_attempts', 5)
                    lockout_duration = settings.get('lockout_duration', 30)
            else:
                max_attempts = 5
                lockout_duration = 30
        except:
            max_attempts = 5
            lockout_duration = 30
        
        # Kiểm tra xem tài khoản có bị khóa không
        lockout_key = f'lockout_{email}'
        if session.get(lockout_key):
            flash(f'Tài khoản đã bị khóa do đăng nhập sai quá nhiều lần. Vui lòng thử lại sau {lockout_duration} phút.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        if user:
            print(f"[DEBUG] User found: {user.email}, is_admin: {user.is_admin}")
            if user.check_password(password):
                # Đăng nhập thành công, reset số lần sai
                session.pop(failed_attempts_key, None)
                session.pop(lockout_key, None)
                
                login_user(user, remember=remember)
                print(f"[DEBUG] Login successful for: {email}")
                
                # Sync user data to Firebase
                firebase_db.save_user(user.to_dict())
                
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.index')
                return redirect(next_page)
            else:
                # Đăng nhập sai
                failed_attempts += 1
                session[failed_attempts_key] = failed_attempts
                
                if failed_attempts >= max_attempts:
                    # Khóa tài khoản
                    session[lockout_key] = True
                    flash(f'Đăng nhập sai {max_attempts} lần. Tài khoản đã bị khóa trong {lockout_duration} phút.', 'danger')
                else:
                    remaining = max_attempts - failed_attempts
                    flash(f'Mật khẩu không đúng. Còn {remaining} lần thử.', 'danger')
                
                print(f"[DEBUG] Password incorrect for: {email}")
        else:
            print(f"[DEBUG] User not found: {email}")
            flash('Email không tồn tại trong hệ thống', 'danger')
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        display_name = request.form.get('display_name')
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'danger')
            return render_template('login.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email đã tồn tại', 'danger')
            return render_template('login.html')
        
        user = User(
            email=email,
            display_name=display_name or email.split('@')[0]
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Save to Firebase
        user_data = {
            'id': user.id,
            'email': user.email,
            'display_name': user.display_name,
            'created_at': user.created_at,
            'is_admin': user.is_admin,
            'last_login': user.last_login
        }
        firebase_db.save_user(user_data)
        
        flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('main.index'))

# API routes
@api.route('/assess', methods=['POST'])
@login_required
def assess_symptoms():
    """Assess symptoms API - Enhanced with AI"""
    try:
        data = request.get_json()
        symptoms_text = data.get('symptoms', '').strip()
        age = int(data.get('age', 0))
        days_sick = int(data.get('days_sick', 0))
        
        if not symptoms_text:
            return jsonify({'error': 'Vui lòng nhập triệu chứng'}), 400
        
        # Get AI diagnosis
        ai_diagnosis_system = get_ai_diagnosis()
        if ai_diagnosis_system:
            # Extract symptoms from text
            symptoms_list = [s.strip() for s in symptoms_text.split(',') if s.strip()]
            
            # Get AI prediction
            ai_result = ai_diagnosis_system.predict_disease(symptoms_list, age, days_sick)
            
            # Enhanced result with AI data
            result = {
                'priority': ai_result['priority'],
                'message': f"AI chẩn đoán: {ai_result['disease']} (Độ tin cậy: {ai_result['confidence']}%)",
                'description': ai_result['description'],
                'recommendations': ai_result['recommendations'],
                'ai_data': {
                    'disease': ai_result['disease'],
                    'confidence': ai_result['confidence'],
                    'severity_score': ai_result['severity_score'],
                    'precautions': ai_result['precautions']
                }
            }
        else:
            # Fallback to original assessment
            user_health_info = {
                'age': current_user.age,
                'gender': current_user.gender,
                'height': current_user.height,
                'weight': current_user.weight,
                'medical_history': current_user.medical_history
            }
            
            result = assessment_engine.assess_symptoms(
                symptoms_text, age, days_sick, user_health_info
            )
        
        # Save assessment to database
        assessment = Assessment(
            user_id=current_user.id,
            symptoms=symptoms_text,
            age_at_assessment=age,
            days_sick=days_sick,
            priority=result['priority'],
            message=result['message'],
            description=result['description'],
            recommendations=json.dumps(result.get('recommendations', []))
        )
        
        db.session.add(assessment)
        db.session.commit()
        
        # Save to Firebase
        assessment_data = {
            'id': assessment.id,
            'user_id': assessment.user_id,
            'user_email': current_user.email,
            'symptoms': assessment.symptoms,
            'age_at_assessment': assessment.age_at_assessment,
            'days_sick': assessment.days_sick,
            'priority': assessment.priority,
            'message': assessment.message,
            'description': assessment.description,
            'recommendations': assessment.recommendations,
            'created_at': assessment.created_at
        }
        firebase_db.save_assessment(assessment_data)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500

@api.route('/health-topics')
def get_health_topics():
    """Get health topics API"""
    try:
        topics = assessment_engine.topics
        return jsonify(topics)
    except Exception as e:
        return jsonify({'error': f'Lỗi tải dữ liệu: {str(e)}'}), 500

@api.route('/user-health', methods=['GET', 'POST'])
@login_required
def user_health():
    """User health info API"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Update user health info
            current_user.gender = data.get('gender')
            current_user.age = int(data.get('age', 0))
            current_user.height = float(data.get('height', 0))
            current_user.weight = float(data.get('weight', 0))
            current_user.medical_history = data.get('medical_history', '')
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Thông tin sức khỏe đã được cập nhật thành công',
                'user': current_user.to_dict()
            })
        except Exception as e:
            return jsonify({'error': f'Lỗi: {str(e)}'}), 500
    else:
        return jsonify(current_user.to_dict())

@api.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """Update user profile API with enhanced fields"""
    try:
        data = request.get_json()
        
        # Update profile fields
        if 'display_name' in data:
            current_user.display_name = data['display_name'].strip()
        
        current_user.gender = data.get('gender')
        current_user.age = int(data.get('age', 0))
        current_user.height = float(data.get('height', 0))
        current_user.weight = float(data.get('weight', 0))
        current_user.medical_history = data.get('medical_history', '')
        
        # Enhanced fields (if your User model supports them)
        if hasattr(current_user, 'phone'):
            current_user.phone = data.get('phone', '')
        if hasattr(current_user, 'address'):
            current_user.address = data.get('address', '')
        if hasattr(current_user, 'emergency_contact'):
            current_user.emergency_contact = data.get('emergency_contact', '')
        if hasattr(current_user, 'blood_type'):
            current_user.blood_type = data.get('blood_type', '')
        if hasattr(current_user, 'allergies'):
            current_user.allergies = data.get('allergies', '')
        if hasattr(current_user, 'medications'):
            current_user.medications = data.get('medications', '')
        
        db.session.commit()
        
        # Update Firebase
        user_data = {
            'id': current_user.id,
            'email': current_user.email,
            'display_name': current_user.display_name,
            'username': getattr(current_user, 'username', ''),
            'gender': current_user.gender,
            'age': current_user.age,
            'height': current_user.height,
            'weight': current_user.weight,
            'medical_history': current_user.medical_history,
            'phone': getattr(current_user, 'phone', ''),
            'address': getattr(current_user, 'address', ''),
            'emergency_contact': getattr(current_user, 'emergency_contact', ''),
            'blood_type': getattr(current_user, 'blood_type', ''),
            'allergies': getattr(current_user, 'allergies', ''),
            'medications': getattr(current_user, 'medications', ''),
            'is_admin': current_user.is_admin,
            'is_active': getattr(current_user, 'is_active', True),
            'last_login': current_user.last_login,
            'updated_at': datetime.now()
        }
        firebase_db.update_user(current_user.id, user_data)
        
        return jsonify({
            'success': True,
            'message': 'Thông tin đã được cập nhật thành công!',
            'user': current_user.to_dict()
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi cập nhật: {str(e)}'}), 500

@api.route('/contact', methods=['POST'])
def submit_contact():
    """Submit contact form API"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        if not all([name, email, subject, message]):
            return jsonify({'error': 'Thiếu thông tin bắt buộc'}), 400
        
        contact = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        db.session.add(contact)
        db.session.commit()
        
        # Save to Firebase
        contact_data = {
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'subject': contact.subject,
            'message': contact.message,
            'created_at': contact.created_at
        }
        firebase_db.save_contact(contact_data)
        
        return jsonify({'success': True, 'message': 'Tin nhắn đã được gửi thành công!'})
    
    except Exception as e:
        return jsonify({'error': f'Lỗi gửi tin nhắn: {str(e)}'}), 500

# AI Diagnosis API routes
@api.route('/ai/symptoms', methods=['GET'])
def get_ai_symptoms():
    """Get available symptoms for AI diagnosis"""
    try:
        ai_diagnosis_system = get_ai_diagnosis()
        if ai_diagnosis_system:
            symptoms_vn = ai_diagnosis_system.get_available_symptoms_vn()
            return jsonify({
                'success': True,
                'symptoms': symptoms_vn,
                'total': len(symptoms_vn)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'AI system not available'
            }), 503
    except Exception as e:
        return jsonify({'error': f'Lỗi tải danh sách triệu chứng: {str(e)}'}), 500

@api.route('/ai/diseases', methods=['GET'])
def get_ai_diseases():
    """Get available diseases for AI diagnosis with detailed information"""
    try:
        ai_diagnosis_system = get_ai_diagnosis()
        if ai_diagnosis_system:
            diseases_vn = ai_diagnosis_system.get_available_diseases_vn()
            
            # Add additional information for each disease
            enhanced_diseases = []
            for disease in diseases_vn:
                enhanced_disease = {
                    'id': len(enhanced_diseases) + 1,
                    'en': disease['en'],
                    'vn': disease['vn'],
                    'description': ai_diagnosis_system.disease_descriptions.get(disease['en'], 'Mô tả bệnh sẽ được cập nhật'),
                    'prevention': ai_diagnosis_system.disease_precautions.get(disease['en'], ['Tham khảo ý kiến bác sĩ', 'Nghỉ ngơi', 'Uống nhiều nước']),
                    'symptoms': [],  # Will be populated based on disease type
                    'care': []  # Will be populated based on disease type
                }
                
                # Add common symptoms and care based on disease type
                disease_lower = disease['en'].lower()
                if 'hepatitis' in disease_lower:
                    enhanced_disease['symptoms'] = ['Vàng da', 'Mệt mỏi', 'Đau bụng', 'Chán ăn', 'Buồn nôn']
                    enhanced_disease['care'] = ['Tiêm vaccine', 'Tránh rượu bia', 'Khám gan định kỳ', 'Chế độ ăn lành mạnh']
                elif 'diabetes' in disease_lower:
                    enhanced_disease['symptoms'] = ['Khát nước nhiều', 'Tiểu nhiều', 'Mệt mỏi', 'Sụt cân', 'Mờ mắt']
                    enhanced_disease['care'] = ['Theo dõi đường huyết', 'Chế độ ăn kiêng', 'Tập thể dục', 'Dùng thuốc đúng giờ']
                elif 'hypertension' in disease_lower:
                    enhanced_disease['symptoms'] = ['Đau đầu', 'Chóng mặt', 'Mệt mỏi', 'Khó thở', 'Đau ngực']
                    enhanced_disease['care'] = ['Giảm muối', 'Tập thể dục', 'Giảm cân', 'Dùng thuốc đều đặn']
                elif 'asthma' in disease_lower:
                    enhanced_disease['symptoms'] = ['Khó thở', 'Thở khò khè', 'Ho', 'Tức ngực', 'Thở nhanh']
                    enhanced_disease['care'] = ['Dùng thuốc hít', 'Tránh chất kích thích', 'Tập thở', 'Khám định kỳ']
                elif 'arthritis' in disease_lower:
                    enhanced_disease['symptoms'] = ['Đau khớp', 'Sưng khớp', 'Cứng khớp', 'Giảm vận động', 'Mệt mỏi']
                    enhanced_disease['care'] = ['Tập thể dục nhẹ', 'Giữ ấm khớp', 'Dùng thuốc giảm đau', 'Vật lý trị liệu']
                elif 'cold' in disease_lower or 'flu' in disease_lower:
                    enhanced_disease['symptoms'] = ['Ho', 'Sổ mũi', 'Đau họng', 'Hắt hơi', 'Sốt', 'Mệt mỏi']
                    enhanced_disease['care'] = ['Nghỉ ngơi đầy đủ', 'Uống nhiều nước', 'Dùng thuốc không kê đơn', 'Tránh tiếp xúc']
                elif 'gastroenteritis' in disease_lower:
                    enhanced_disease['symptoms'] = ['Tiêu chảy', 'Nôn mửa', 'Đau bụng', 'Buồn nôn', 'Sốt nhẹ']
                    enhanced_disease['care'] = ['Uống nhiều nước', 'Nghỉ ngơi', 'Ăn thức ăn nhẹ', 'Vệ sinh sạch sẽ']
                elif 'migraine' in disease_lower:
                    enhanced_disease['symptoms'] = ['Đau đầu một bên', 'Buồn nôn', 'Nhạy cảm ánh sáng', 'Chóng mặt']
                    enhanced_disease['care'] = ['Nghỉ ngơi trong phòng tối', 'Dùng thuốc giảm đau', 'Tránh stress', 'Thư giãn']
                else:
                    enhanced_disease['symptoms'] = ['Triệu chứng sẽ được cập nhật']
                    enhanced_disease['care'] = ['Tham khảo ý kiến bác sĩ', 'Nghỉ ngơi', 'Uống nhiều nước']
                
                enhanced_diseases.append(enhanced_disease)
            
            return jsonify({
                'success': True,
                'diseases': enhanced_diseases,
                'total': len(enhanced_diseases)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'AI system not available'
            }), 503
    except Exception as e:
        return jsonify({'error': f'Lỗi tải danh sách bệnh: {str(e)}'}), 500

@api.route('/ai/symptom-info/<symptom>', methods=['GET'])
def get_symptom_info(symptom):
    """Get information about a specific symptom"""
    try:
        ai_diagnosis_system = get_ai_diagnosis()
        if ai_diagnosis_system:
            info = ai_diagnosis_system.get_symptom_info(symptom)
            return jsonify({
                'success': True,
                'symptom_info': info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'AI system not available'
            }), 503
    except Exception as e:
        return jsonify({'error': f'Lỗi tải thông tin triệu chứng: {str(e)}'}), 500

@api.route('/ai/quick-diagnosis', methods=['POST'])
def quick_ai_diagnosis():
    """Quick AI diagnosis without login requirement"""
    try:
        data = request.get_json()
        symptoms_text = data.get('symptoms', '').strip()
        age = int(data.get('age', 30))
        days_sick = int(data.get('days_sick', 3))
        
        if not symptoms_text:
            return jsonify({'error': 'Vui lòng nhập triệu chứng'}), 400
        
        ai_diagnosis_system = get_ai_diagnosis()
        if ai_diagnosis_system:
            # Extract symptoms from text
            symptoms_list = [s.strip() for s in symptoms_text.split(',') if s.strip()]
            
            # Get AI prediction
            ai_result = ai_diagnosis_system.predict_disease(symptoms_list, age, days_sick)
            
            return jsonify({
                'success': True,
                'result': ai_result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'AI system not available'
            }), 503
    
    except Exception as e:
        return jsonify({'error': f'Lỗi chẩn đoán: {str(e)}'}), 500

# Firebase Realtime Data API routes
@api.route('/firebase/users', methods=['GET'])
@login_required
def get_firebase_users():
    """Get all users from Firebase"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        users = firebase_db.get_all_users()
        return jsonify({
            'success': True,
            'users': users,
            'total': len(users)
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải dữ liệu người dùng: {str(e)}'}), 500

@api.route('/firebase/assessments', methods=['GET'])
@login_required
def get_firebase_assessments():
    """Get all assessments from Firebase"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        assessments = firebase_db.get_all_assessments()
        return jsonify({
            'success': True,
            'assessments': assessments,
            'total': len(assessments)
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải dữ liệu đánh giá: {str(e)}'}), 500

@api.route('/firebase/contacts', methods=['GET'])
@login_required
def get_firebase_contacts():
    """Get all contacts from Firebase"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        contacts = firebase_db.get_all_contacts()
        return jsonify({
            'success': True,
            'contacts': contacts,
            'total': len(contacts)
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải dữ liệu liên hệ: {str(e)}'}), 500

@api.route('/firebase/statistics', methods=['GET'])
@login_required
def get_firebase_statistics():
    """Get statistics from Firebase"""
    try:
        if not current_user.is_admin:
            return jsonify({'error': 'Unauthorized'}), 403
        
        stats = firebase_db.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải thống kê: {str(e)}'}), 500

@api.route('/firebase/user-history/<int:user_id>', methods=['GET'])
@login_required
def get_user_history(user_id):
    """Get user's health assessment history from Firebase"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        history = firebase_db.get_user_history(user_id)
        return jsonify({
            'success': True,
            'history': history,
            'total': len(history)
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải lịch sử: {str(e)}'}), 500

@api.route('/firebase/save-diagnosis', methods=['POST'])
@login_required
def save_ai_diagnosis():
    """Save AI diagnosis result to Firebase"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not data.get('user_id'):
            return jsonify({'error': 'Thiếu thông tin cần thiết'}), 400
        
        # Ensure user can only save their own diagnosis
        if str(data['user_id']) != str(current_user.id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Save to Firebase
        success = firebase_db.save_ai_diagnosis(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Kết quả chẩn đoán đã được lưu vào hồ sơ'
            })
        else:
            return jsonify({'error': 'Không thể lưu kết quả chẩn đoán'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Lỗi lưu chẩn đoán: {str(e)}'}), 500

@api.route('/firebase/diagnosis-history/<int:user_id>', methods=['GET'])
@login_required
def get_diagnosis_history(user_id):
    """Get user's AI diagnosis history from Firebase"""
    try:
        if not current_user.is_admin and current_user.id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        history = firebase_db.get_user_diagnosis_history(user_id)
        return jsonify({
            'success': True,
            'history': history,
            'total': len(history)
        })
    except Exception as e:
        return jsonify({'error': f'Lỗi tải lịch sử chẩn đoán: {str(e)}'}), 500

# Admin routes
@admin.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    # Get statistics
    total_users = User.query.count()
    total_assessments = Assessment.query.count()
    total_contacts = Contact.query.filter_by(status='new').count()
    
    # Get recent activities
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(5).all()
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    # Get Firebase stats if available
    firebase_stats = firebase_db.get_statistics()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         total_assessments=total_assessments,
                         total_contacts=total_contacts,
                         recent_assessments=recent_assessments,
                         recent_contacts=recent_contacts,
                         firebase_stats=firebase_stats)

@admin.route('/admin/users')
@login_required
def admin_users():
    """Admin users management"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    # Get all users without pagination
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin_users.html', users=users)

@admin.route('/admin/assessments')
@login_required
def admin_assessments():
    """Admin assessments management"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    # Get all assessments without pagination
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).all()
    return render_template('admin_assessments.html', assessments=assessments)
@admin.route('/admin/contacts')
@login_required
def admin_contacts():
    """Admin contacts management"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    contacts = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin_contacts.html', contacts=contacts)

# API endpoints for admin actions
@admin.route('/admin/user/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Toggle user active status"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        if user.is_admin:
            return jsonify({'error': 'Không thể thay đổi trạng thái admin'}), 400
        
        user.is_active = not user.is_active
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'Đã {"kích hoạt" if user.is_active else "vô hiệu hóa"} người dùng',
            'is_active': user.is_active
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/admin/user/<int:user_id>/delete', methods=['DELETE'])
@login_required
def delete_user(user_id):
    """Delete user"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        user = User.query.get_or_404(user_id)
        if user.is_admin:
            return jsonify({'error': 'Không thể xóa tài khoản admin'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Đã xóa người dùng thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/admin/assessment/<int:assessment_id>/delete', methods=['DELETE'])
@login_required
def delete_assessment(assessment_id):
    """Delete assessment"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        db.session.delete(assessment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Đã xóa đánh giá thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/admin/contact/<int:contact_id>/status', methods=['POST'])
@login_required
def update_contact_status(contact_id):
    """Update contact status"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        status = data.get('status')
        
        contact = Contact.query.get_or_404(contact_id)
        contact.status = status
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Cập nhật trạng thái thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/admin/contact/<int:contact_id>/delete', methods=['DELETE'])
@login_required
def delete_contact(contact_id):
    """Delete contact"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Đã xóa tin nhắn thành công'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin.route('/admin/reports')
@login_required
def admin_reports():
    """Admin reports page"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    # Get statistics for reports
    total_users = User.query.count()
    total_assessments = Assessment.query.count()
    total_contacts = Contact.query.count()
    
    # Get monthly data for charts
    from datetime import datetime, timedelta
    import calendar
    
    # Last 6 months data
    months_data = []
    for i in range(6):
        date = datetime.now() - timedelta(days=30*i)
        month_start = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end = month_start.replace(day=calendar.monthrange(date.year, date.month)[1], hour=23, minute=59, second=59)
        
        users_count = User.query.filter(User.created_at >= month_start, User.created_at <= month_end).count()
        assessments_count = Assessment.query.filter(Assessment.created_at >= month_start, Assessment.created_at <= month_end).count()
        
        months_data.append({
            'month': date.strftime('%m/%Y'),
            'users': users_count,
            'assessments': assessments_count
        })
    
    months_data.reverse()  # Show oldest to newest
    
    return render_template('admin_reports.html', 
                         total_users=total_users,
                         total_assessments=total_assessments,
                         total_contacts=total_contacts,
                         months_data=months_data)

@admin.route('/admin/settings')
@login_required
def admin_settings():
    """Admin settings page"""
    if not current_user.is_admin:
        flash('Bạn không có quyền truy cập trang này', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('admin_settings.html')

@admin.route('/admin/settings/update', methods=['POST'])
@login_required
def update_settings():
    """Update system settings"""
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Lưu cài đặt vào session để áp dụng ngay lập tức
        # Trong thực tế, bạn có thể lưu vào database hoặc file config
        settings = {
            'app_name': data.get('appName', 'HealthFirst'),
            'app_description': data.get('appDescription', 'Hệ thống hướng dẫn y tế và chăm sóc sức khỏe tại nhà'),
            'contact_email': data.get('contactEmail', 'admin@healthfirst.com'),
            'support_phone': data.get('supportPhone', '+84 123 456 789'),
            'two_factor_auth': data.get('twoFactorAuth', False),
            'login_attempts': data.get('loginAttempts', 5),
            'lockout_duration': data.get('lockoutDuration', 30),
            'email_notifications': data.get('emailNotifications', True),
            'contact_notifications': data.get('contactNotifications', True),
            'emergency_notifications': data.get('emergencyNotifications', True),
            'maintenance_mode': data.get('maintenanceMode', False),
            'session_timeout': data.get('sessionTimeout', 30),
            'backup_frequency': data.get('backupFrequency', 'weekly')
        }
        
        # Lưu vào session để áp dụng ngay lập tức
        session['app_settings'] = settings
        
        # Lưu vào file JSON để lưu trữ lâu dài
        import json
        import os
        
        settings_file = 'app_settings.json'
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'success': True, 
            'message': 'Cài đặt đã được cập nhật và áp dụng thành công!'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Lỗi cập nhật cài đặt: {str(e)}'})

@admin.route('/admin/settings/get')
@login_required
def get_settings():
    """Get current system settings"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        # Đọc cài đặt từ file JSON
        import json
        import os
        
        settings_file = 'app_settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
        else:
            # Cài đặt mặc định
            settings = {
                'app_name': 'HealthFirst',
                'app_description': 'Hệ thống hướng dẫn y tế và chăm sóc sức khỏe tại nhà',
                'contact_email': 'admin@healthfirst.com',
                'support_phone': '+84 123 456 789',
                'two_factor_auth': False,
                'login_attempts': 5,
                'lockout_duration': 30,
                'email_notifications': True,
                'contact_notifications': True,
                'emergency_notifications': True,
                'maintenance_mode': False,
                'session_timeout': 30,
                'backup_frequency': 'weekly'
            }
        
        return jsonify({'success': True, 'settings': settings})
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Lỗi lấy cài đặt: {str(e)}'})

