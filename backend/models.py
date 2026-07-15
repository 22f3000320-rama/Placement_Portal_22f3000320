from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'student', 'company'
    is_active     = db.Column(db.Boolean, nullable=False, default=True)
    
    student = db.relationship("Student", back_populates="user", uselist=False)
    company = db.relationship("Company", back_populates="user", uselist=False)


    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
    
class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    resume_file = db.Column(db.LargeBinary, nullable=True)
    
    user = db.relationship('User', back_populates='student')
    skills = db.relationship('StudentSkill', back_populates='student')
    applications = db.relationship('Application', back_populates='student')
    
    def __repr__(self):
        return f"<Student {self.name}>"
    
class StudentSkill(db.Model):
    """Student Skill model"""
    __tablename__ = 'student_skills'
    
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    
    student = db.relationship('Student', back_populates='skills')
    
    def __repr__(self):
        return f"<StudentSkill {self.skill_name}>"
    
class Company(db.Model):
    """Company model"""
    __tablename__ = 'companies'
    
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)
    approval_status = db.Column(db.String(20), nullable=False, default='pending')
    
    user = db.relationship('User', back_populates='company')
    placement_drives = db.relationship('Placement_Drive', back_populates='company')
    
    def __repr__(self):
        return f"<Company {self.name}>"
    

    
class Placement_Drive(db.Model):
    """Placement Drive model"""
    __tablename__ = 'placement_drives'

    drive_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ctc = db.Column(db.Float, nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    cgpa_threshold = db.Column(db.Float, nullable=False)
    year_threshold = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(12), nullable=False, default='pending')
    
    company = db.relationship('Company', back_populates='placement_drives')
    applications = db.relationship('Application', back_populates='placement_drive')
    skills = db.relationship('DriveSkill', back_populates='placement_drive')
    
    def __repr__(self):
        return f"<Placement_Drive {self.title} by {self.company.name}>"
    
class DriveSkill(db.Model):
    """Drive Skill model"""
    __tablename__ = 'drive_skills'
    
    skill_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.drive_id'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    
    placement_drive = db.relationship('Placement_Drive', back_populates='skills')
    
    def __repr__(self):
        return f"<DriveSkill {self.skill_name}>"
    
    
class Application(db.Model):
    """Application model"""
    __tablename__ = 'applications'
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),)
    
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.drive_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='applied')
    applied_at = db.Column(db.DateTime, default=datetime.now)
    
    student = db.relationship('Student', back_populates='applications')     
    placement_drive = db.relationship('Placement_Drive', back_populates='applications')
    
    def __repr__(self):
        return f"<Application {self.student.name} for {self.placement_drive.title}>"
    
