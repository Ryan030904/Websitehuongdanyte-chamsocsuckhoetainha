from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from argon2 import PasswordHasher

db = SQLAlchemy()
password_hasher = PasswordHasher()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    pw_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(20), nullable=True)  # 'male', 'female', 'other'
    age = db.Column(db.Integer, nullable=True)
    height = db.Column(db.Float, nullable=True)  # cm
    weight = db.Column(db.Float, nullable=True)  # kg
    medical_history = db.Column(db.Text, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    health_records = db.relationship('HealthRecord', backref='user', lazy='dynamic')
    assessments = db.relationship('Assessment', backref='user', lazy='dynamic')
    
    def set_password(self, password: str):
        """Hash password using Argon2"""
        self.pw_hash = password_hasher.hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password"""
        try:
            return password_hasher.verify(self.pw_hash, password)
        except Exception:
            return False
    
    def get_bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None
    
    def get_bmi_category(self):
        """Get BMI category"""
        bmi = self.get_bmi()
        if bmi is None:
            return None
        elif bmi < 18.5:
            return "Thiếu cân"
        elif bmi < 25:
            return "Bình thường"
        elif bmi < 30:
            return "Thừa cân"
        else:
            return "Béo phì"
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'display_name': self.display_name,
            'gender': self.gender,
            'age': self.age,
            'height': self.height,
            'weight': self.weight,
            'bmi': self.get_bmi(),
            'bmi_category': self.get_bmi_category(),
            'medical_history': self.medical_history,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)  # 'symptoms', 'medication', 'appointment'
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'record_type': self.record_type,
            'title': self.title,
            'description': self.description,
            'date_recorded': self.date_recorded.isoformat() if self.date_recorded else None
        }

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    age_at_assessment = db.Column(db.Integer, nullable=False)
    days_sick = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.String(50), nullable=False)  # 'emergency', 'high', 'consult_doctor', 'home_care'
    message = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recommendations = db.Column(db.Text, nullable=True)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'symptoms': self.symptoms,
            'age_at_assessment': self.age_at_assessment,
            'days_sick': self.days_sick,
            'priority': self.priority,
            'message': self.message,
            'description': self.description,
            'recommendations': self.recommendations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Contact(db.Model):
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # 'new', 'read', 'replied'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
