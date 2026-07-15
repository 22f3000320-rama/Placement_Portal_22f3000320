from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, User, Student, Company, StudentSkill, Placement_Drive, Application, DriveSkill
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, DEBUG, CACHE_TYPE, CACHE_REDIS_URL
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from flask_caching import Cache 
from sqlalchemy.orm import joinedload
from tasks import export_application_history

app = Flask(__name__)   
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
app.config['DEBUG'] = DEBUG
app.config['CACHE_TYPE'] = CACHE_TYPE
app.config['CACHE_REDIS_URL'] = CACHE_REDIS_URL

CORS(app)
db.init_app(app)
jwt = JWTManager(app)
cache = Cache(app)
    

@app.route('/api/student/register', methods=['POST'])
def register_student():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'This email is already registered with another student! Please log in or use a different email.'}), 400
    
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='student'
    )
    student = Student(
        user=user,
        name=data['name'],
        department=data['department'],
        cgpa=data['cgpa'],
        year=data['year'],
        contact=data['contact']
    )
    skills = data.get("skills", [])
    try:
        db.session.add(student)
    
        for skill in skills:
            student_skill = StudentSkill(
                student = student,
                skill_name = skill
            )
            db.session.add(student_skill)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Unable to register student with the provided details.'}), 400

    return jsonify({'message': 'Student registered successfully!'}), 201

@app.route('/api/student/login', methods=['POST'])
def login_student():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message':'Invalid email. Please try again.'}), 404
    student = Student.query.filter_by(user_id = user.user_id).first()
    
    if not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid password.'}), 401
    if user.role != 'student':
        return jsonify({'message': 'Only students can log in.'}), 403
    if not user.is_active:
        return jsonify({'message':'You are not allowed to access the dashboard. Please contact the admin.'}), 403
    access_token = create_access_token(identity=user.email, additional_claims={'role': user.role})
    return jsonify({'access_token': access_token, 'message': 'Login successful!', 'data': {'email': user.email, 'studentId':student.student_id, 'name': user.student.name, 'role': user.role}})

@app.route('/api/company/register', methods=['POST'])
def register_company():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'This email is already registered with another company! Please log in or use a different email.'}), 400
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='company'
    )
    company = Company(
        user=user,
        name=data['name'],
        description=data['description'],
        website=data['website'],
        contact=data['contact']
    )

    try:
        db.session.add(company)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Unable to register company with the provided details.'}), 400

    return jsonify({'message': 'Company registered successfully!'})

@app.route('/api/company/login', methods=['POST'])
def login_company():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message':'Invalid email. Please try again.'}), 404
    company = Company.query.filter_by(user_id = user.user_id).first()
    
    if not user.is_active:
        return jsonify({'message':'You are not allowed to acess the dashboard. Please contact the admin.'}), 403
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid email or password.'}), 401
    if user.role != 'company':
        return jsonify({'message': 'Company access only.'}), 403
    if company.approval_status == 'pending':
        return jsonify({'message': 'Pending approval from the admin.'}), 403
    access_token = create_access_token(identity=user.email, additional_claims={'role': user.role})
    return jsonify({'access_token': access_token, 'message': 'Login successful!', 'data': {'email': user.email, 'name': user.company.name, 'role': user.role}})

@app.route('/api/company/post-drive', methods=['POST'])
@jwt_required()
def create_drive():
    if get_jwt().get('role') != 'company':
        return jsonify({'message': 'Access forbidden: Company access only.'}), 403
    data = request.get_json()
    
    company_email = get_jwt_identity()
    company = Company.query.join(User).filter(User.email == company_email).first()
    
    if not company:
        return jsonify({'message': 'Company not found.'}), 404
    
    drive = Placement_Drive(
        company_id=company.company_id,
        title=data['title'],
        description=data['description'],
        branch=data['department'],
        cgpa_threshold=data['cgpa_threshold'],
        year_threshold=data['year'],
        deadline=datetime.fromisoformat(data['deadline']),
        ctc=data['ctc']
    )
    
    db.session.add(drive)
    db.session.flush()
    
    skills = data.get("skills", [])
    
    for skill in skills:
        drive_skill = DriveSkill(
            drive_id = drive.drive_id,
            skill_name = skill
        )
        db.session.add(drive_skill)
        
    db.session.commit()
    return jsonify({'message': 'Placement drive submitted successfully! It is now pending approval from the admin.'})


@app.route('/api/admin/login', methods=['POST'])
def login_admin():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid email or password.'}), 401
    if user.role != 'admin':
        return jsonify({'message': 'Admin access only.'}), 403
    access_token = create_access_token(identity=user.email, additional_claims={'role': user.role})
    return jsonify({'access_token': access_token, 'message': 'Login successful!', 'data': {'email': user.email, 'role': user.role}})


@app.route('/api/get-companies', methods=['GET'])
@jwt_required()
def get_companies():
    role = get_jwt().get('role')
    if role not in ['admin', 'student']:
        return jsonify({'message': 'Access forbidden.'}), 403

    companies = Company.query.filter_by(approval_status="approved").order_by(func.lower(Company.name).asc()).all()
    if companies:
        companyCount = len(companies)
    else:
        return jsonify({'message': 'No companies found at the moment. Please try again.'}), 404
    company_list = []
    for company in companies:
        company_info = {
            'company_id': company.company_id,
            'name': company.name,
            'email': company.user.email,
            'website': company.website,
            'is_active': company.user.is_active,
            'status': company.approval_status
        }
        company_list.append(company_info)
    return jsonify({'companies': company_list, 'companyCount' : companyCount})

@app.route('/api/admin/get-company-applications', methods=['GET'])
@jwt_required()
def get_company_applications():
    role = get_jwt().get('role')
    if role != "admin":
        return jsonify({'message': 'Access forbidden.'}), 403
    
    companies = Company.query.filter_by(approval_status="pending").order_by(func.lower(Company.name).asc()).all()
    company_list = []
    for company in companies:
        company_info = {
            'company_id': company.company_id,
            'name': company.name,
            'email': company.user.email,
            'website': company.website
        }   
        company_list.append(company_info)
    return jsonify({'companyApplications': company_list})

@app.route('/api/admin/approve-company/<int:company_id>', methods=['PATCH'])
@jwt_required()
def approve_company(company_id):
    role = get_jwt().get('role')
    if role != "admin":
        return jsonify({'message':'Access Forbidden'}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message':'Company does not exist.'}), 404
    if company.approval_status == "approved":
        return jsonify({'message': 'Company has already been approved.'})
    
    company.approval_status = "approved"
    db.session.commit()
    
    return jsonify({'message':f'Company {company.name} has been approved successfully.'})

@app.route('/api/admin/reject-company/<int:company_id>', methods=['PATCH'])
@jwt_required()
def reject_company(company_id):
    role = get_jwt().get('role')
    if role != "admin":
        return jsonify({'message':'Access Forbidden'}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message':'Company does not exist.'}), 404
    if company.approval_status == "rejected":
        return jsonify({'message': 'Company has already been rejected.'})
    
    company.approval_status = "rejected"
    db.session.commit()
    
    return jsonify({'message':f'Company {company.name} has been rejected successfully.'})

@app.route('/api/admin/blacklist-unblacklist-company/<int:company_id>', methods=['POST'])
@jwt_required()
def blacklist_unblacklist_company(company_id):
    role = get_jwt().get('role')
    if role != "admin":
        return jsonify({'message':'Access Forbidden'}), 403
    
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'message':'Company does not exist.'}), 404
    if not company.user.is_active:
        company.user.is_active = True
        db.session.commit()
        return jsonify({'message':f'Company {company.name} has been unblocked successfully.'}), 200
    if company.user.is_active:
        company.user.is_active = False
        db.session.commit()
        return jsonify({'message':f'Company {company.name} has been blocked successfully.'}), 200
    
    
@app.route('/api/get-company-details/<int:company_id>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=60)
def get_company_details(company_id):
    role = get_jwt().get('role')
    if role not in ['admin', 'student']:
        return jsonify({'message':'Access forbidden.'}), 403
    
    company = Company.query.get_or_404(company_id)
    drives_query = Placement_Drive.query.filter_by(company_id = company.company_id)
    if role == "student":
        if not company.user.is_active:
            return jsonify({'message':'Company has been blacklisted.'}), 404
        today = datetime.now()
        drives_query = Placement_Drive.query.filter(Placement_Drive.status=='approved', Placement_Drive.deadline>=today)

    drives = drives_query.all()
    company_info = {
            'name': company.name,
            'email': company.user.email,
            'description': company.description,
            'website': company.website,
            'contact': company.contact,
            'status':company.user.is_active,
            'company_drives': []
        }
    for drive in drives:
        company_info['company_drives'].append(
            {
                'drive_id':drive.drive_id,
                'title': drive.title,
                'status':drive.status,
                'deadline': drive.deadline.isoformat()
            }
        )
    return jsonify({'company':company_info}), 200

@app.route('/api/admin/get-students', methods=['GET'])
@jwt_required()
def get_students():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admin access only.'}), 403

    students = Student.query.join(User).order_by(func.lower(Student.name).asc()).all()
    if students:
        studentCount = len(students)
    else:
        return jsonify({'message': 'No students found at the moment. Please try again.'}), 404
    student_list = []
    for student in students:
        student_info = {
            'student_id': student.student_id,
            'name': student.name,
            'email': student.user.email,
            'department': student.department
        }
        student_list.append(student_info)
    return jsonify({'students': student_list, 'studentCount':studentCount})

@app.route('/api/get-pending-drives', methods=['GET'])
@jwt_required()
def get_pending_drives():
    role = get_jwt().get('role')
    if role == 'admin':
        drives = Placement_Drive.query.join(Company).join(User).filter(Placement_Drive.status=='pending', User.is_active == True).order_by(Placement_Drive.deadline.asc()).all()
        
    elif role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        drives = Placement_Drive.query.filter_by(company_id=company.company_id, status='pending').order_by(Placement_Drive.deadline.asc()).all()
        
    else:
        return jsonify({"message": "Unauthorized access"}), 403
        
    pending_drives = []
    for drive in drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        pending_drives.append(drive_info)
    return jsonify({'pendingDrives': pending_drives})

@app.route('/api/get-ongoing-drives', methods=['GET'])
@jwt_required()
def get_ongoing_drives():
    role = get_jwt().get('role')
    driveCount = 0
    if role == 'admin':
        drives = Placement_Drive.query.join(Company).join(User).filter(Placement_Drive.status=='approved', User.is_active == True).order_by(Placement_Drive.deadline.asc()).all()
        driveCount = len(drives)
    if role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        drives = Placement_Drive.query.filter_by(company_id=company.company_id, status='approved').order_by(Placement_Drive.deadline.asc()).all()
    if role=='student':
        drives = Placement_Drive.query.join(Company).join(User).filter(Placement_Drive.status=='approved', User.is_active == True).all()

    ongoing_drives = []
    for drive in drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        ongoing_drives.append(drive_info)
    return jsonify({'ongoingDrives': ongoing_drives, 'driveCount':driveCount}), 200

@app.route('/api/get-closed-drives', methods=['GET'])
@jwt_required()
def get_closed_drives():
    role = get_jwt().get('role')
    if role == 'admin':
        drives = Placement_Drive.query.filter_by(status='closed').order_by(Placement_Drive.deadline.asc()).all()
        
    elif role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        drives = Placement_Drive.query.filter_by(company_id=company.company_id, status='closed').order_by(Placement_Drive.deadline.asc()).all()
    else:
        return jsonify({'message': 'Access forbidden.'}), 403

    closed_drives = []
    for drive in drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        closed_drives.append(drive_info)
    return jsonify({'closedDrives': closed_drives})

@app.route('/api/get-rejected-drives', methods=['GET'])
@jwt_required()
def get_rejected_drives():
    role = get_jwt().get('role')
    if role == 'admin':
        drives = Placement_Drive.query.filter_by(status='rejected').order_by(Placement_Drive.deadline.asc()).all()
        
    elif role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        drives = Placement_Drive.query.filter_by(company_id=company.company_id, status='rejected').order_by(Placement_Drive.deadline.asc()).all()
    else:
        return jsonify({'message': 'Access forbidden.'}), 403

    rejected_drives = []
    for drive in drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        rejected_drives.append(drive_info)
    return jsonify({'rejectedDrives': rejected_drives})

@app.route('/api/admin/get-applications', methods=['GET'])
@jwt_required()
def get_applications():
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admin access only.'}), 403

    applications = Application.query.all()
    
    application_list = []
    for app in applications:
        app_info = {
            'student_name': app.student.name,
            'drive_id': app.placement_drive.drive_id,
            'company_name': app.placement_drive.company.name,
            'status': app.status,
            'applied_at': app.applied_at.isoformat()
        }
        application_list.append(app_info)
    return jsonify({'applications': application_list})

@app.route('/api/get-drive-details/<int:driveId>', methods=['GET'])
@jwt_required()
def get_drive_details(driveId):
    role = get_jwt().get('role')
    drive=None
    has_applied=False
    if role == 'company':
        company = Company.query.join(User).filter(User.email==get_jwt_identity()).first()
        if company:
            drive = Placement_Drive.query.filter_by(company_id=company.company_id, drive_id = driveId).first()
        else:
            return jsonify({'message':'Company not found.'}), 404
    if role == "admin":
        drive = Placement_Drive.query.filter_by(drive_id = driveId).first()
    if role == "student":
        student = Student.query.join(User).filter(User.email==get_jwt_identity()).first()
        drive = Placement_Drive.query.filter(Placement_Drive.status == "approved", Placement_Drive.drive_id == driveId).first()
        existing_application = Application.query.filter_by(student_id = student.student_id, drive_id = driveId).first()
        has_applied = True if existing_application else False
    if not drive:
        return jsonify({'message':'Drive not found.'}), 404
    
    drive_info = {
        'drive_id' : drive.drive_id,
        'title' : drive.title,
        'company_name' : drive.company.name,
        'description' : drive.description,
        'ctc' : drive.ctc,
        'deadline' : drive.deadline.date().isoformat(),
        'year_threshold' : drive.year_threshold,
        'cgpa_threshold' : drive.cgpa_threshold,
        'branch' : drive.branch,
        'skills':[skill.skill_name for skill in drive.skills]
    }
    if role == "student":
        drive_info["has_applied"] = has_applied 
    return jsonify({'drive':drive_info}), 200
    
@app.route('/api/admin/approve-drive/<int:drive_id>', methods=['PATCH'])
@jwt_required()
def approve_drive(drive_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admin access only.'}), 403
    
    drive = Placement_Drive.query.get(drive_id)
    
    if not drive:
        return jsonify({'message': 'Placement drive not found.'}), 404
    
    drive.status = 'approved'
    db.session.commit()
    
    return jsonify({'message': f'Placement drive with drive id {drive.drive_id} and title "{drive.title}" posted by "{drive.company.name}" is now live!'})

@app.route('/api/admin/reject-drive/<int:drive_id>', methods=['PATCH'])
@jwt_required()
def reject_drive(drive_id):
    if get_jwt().get('role') != 'admin':
        return jsonify({'message': 'Access forbidden: Admin access only.'}), 403
    
    drive = Placement_Drive.query.get(drive_id)
    
    if not drive:
        return jsonify({'message': 'Placement drive not found.'}), 404
    
    drive.status = 'rejected'
    db.session.commit()
    
    return jsonify({'message': f'Placement drive with drive id {drive.drive_id} and title "{drive.title}" posted by "{drive.company.name}" has been rejected and will not be visible to students.'})        

@app.route('/api/company/update-drive/<int:drive_id>', methods=['PUT'])
@jwt_required()
def update_drive(drive_id):
    if get_jwt().get('role') != 'company':
        return jsonify({'message': 'Access forbidden: Company access only.'}), 403

    drive = Placement_Drive.query.get(drive_id)

    if not drive:
        return jsonify({'message': 'Placement drive not found.'}), 404

    data = request.get_json()
    drive.title = data.get('title', drive.title)
    drive.description = data.get('description', drive.description)
    drive.branch = data.get('branch', drive.branch)
    drive.cgpa_threshold = data.get('cgpa_threshold', drive.cgpa_threshold)
    drive.year_threshold = data.get('year_threshold', drive.year_threshold)
    drive.deadline = datetime.fromisoformat(data['deadline']) if data.get('deadline') else drive.deadline
    drive.ctc = data.get('ctc', drive.ctc)

    db.session.commit()

    return jsonify({'message': f'Placement drive with drive id {drive.drive_id} updated successfully!'})

@app.route('/api/get-student-details/<int:studentId>', methods=['GET'])
@jwt_required()
def get_student_details(studentId):
    role = get_jwt().get('role')
    if role == 'company':
        return jsonify({'message':'Access forbidden.'}), 403
    student = Student.query.get(studentId)
    if not student:
        return jsonify({'message':'Student not found.'}), 404
    if role in ['admin', 'student']:
        student_info = {
            'student_id':student.student_id,
            'email':student.user.email,
            'name':student.name,
            'department':student.department,
            'cgpa':student.cgpa,
            'year':student.year,
            'contact':student.contact,
            'skills':[skill.skill_name for skill in student.skills]
        }
        return jsonify({'student':student_info})
    
@app.route('/api/student/update-profile/<int:studentId>', methods=['PUT'])
@jwt_required()
def update_profile(studentId):
    role = get_jwt().get('role')
    if role != 'student':
        return jsonify({'message':'Access forbidden.'}), 403
    student = Student.query.get(studentId)
    if not student:
        return jsonify({'message':'Student not found.'}), 404
    data = request.get_json()
    student.cgpa = data.get('cgpa', student.cgpa)
    student.year = data.get('year', student.year)
    student.contact = data.get('contact', student.contact)
    
    if "skills" in data:
        requested_skills = set(data["skills"])
        
        current_skill_objects = StudentSkill.query.filter_by(student_id = student.student_id).all()
        current_skills = {skill.skill_name for skill in current_skill_objects}
        
        new_skills = requested_skills - current_skills
        remove_skills = current_skills - requested_skills
    
        for skill_name in new_skills:
            new_skill = StudentSkill(skill_name=skill_name, student_id = student.student_id)
            db.session.add(new_skill)
            
        if remove_skills:
            StudentSkill.query.filter(StudentSkill.student_id==student.student_id, StudentSkill.skill_name.in_(remove_skills)).delete(synchronize_session=False)
    try:
        db.session.commit()
        return jsonify({'message':'Profile Details updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'message':'Something went wrong. Please try again'}), 500
        
@app.route('/api/get-student-application-history/<int:studentId>', methods=['GET'], strict_slashes = False)
@jwt_required()
def get_student_application_history(studentId):
    role = get_jwt().get('role')
    if role not in ['admin', 'student']:
        return jsonify({'message':'Access Forbidden.'}), 403
    if role == 'admin':
        applications = Application.query.filter_by(student_id = studentId).all()
    elif role == 'student':
        student = Student.query.join(User).filter_by(email=get_jwt_identity()).first()
        applications = Application.query.filter_by(student_id=student.student_id).all()
    if not applications:
        return jsonify({'message':'No applications found.'}), 404
    application_list=[]
    for app in applications:
        app_info = {
            'application_id': app.application_id,
            'student_id': app.student_id,
            'student_name': app.student.name,
            'student_department': app.student.department,
            'drive_id': app.placement_drive.drive_id,
            'title': app.placement_drive.title,
            'company_name': app.placement_drive.company.name,
            'status': app.status,
            'applied_at': app.applied_at.date().isoformat()
        }
        application_list.append(app_info)
    return jsonify({'applications':application_list}), 200
        
        
@app.route('/api/close-drive/<int:drive_id>', methods=['PATCH'])
@jwt_required()
def close_drive(drive_id):
    role = get_jwt().get("role")
    if role not in ["admin", "company"]:
        return jsonify({'message': 'Access forbidden: Company access only.'}), 403

    drive = Placement_Drive.query.get(drive_id)
    if not drive:
        return jsonify({'message': 'Placement drive not found.'}), 404
    if drive.status == "pending":
        return jsonify({'message': 'Drive is pending with admin.'}), 403
    if drive.status == "closed":
        return jsonify({'message': 'Drive is already closed.'}), 403
    if role == "company":
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        if drive.company_id != company.company_id:
            return jsonify({'message':'Access forbidden.'}), 403
    drive.status = 'closed'
    db.session.commit()

    return jsonify({'message': f'Placement drive with drive id {drive.drive_id} and title "{drive.title}" has been closed. It will no longer be visible to students and no new applications will be accepted.'})

@app.route('/api/student/apply-drive/<int:drive_id>', methods=['POST'])
@jwt_required()
def drive_application(drive_id):
    if get_jwt().get('role') != 'student':
        return jsonify({'message': 'Access forbidden: Student access only.'}), 403

    drive = Placement_Drive.query.get(drive_id)

    if not drive or drive.status != 'approved':
        return jsonify({'message': 'Placement drive not found or not open for applications.'}), 404

    student_email = get_jwt_identity()
    student = Student.query.join(User).filter(User.email == student_email).first()

    if not student:
        return jsonify({'message': 'Student not found.'}), 404

    existing_application = Application.query.filter_by(student_id=student.student_id, drive_id=drive.drive_id).first()
    if existing_application:
        return jsonify({'message': 'You have already applied for this placement drive.'}), 400

    application = Application(student_id=student.student_id, drive_id=drive.drive_id)
    db.session.add(application)
    db.session.commit()

    return jsonify({'message': f'Application submitted successfully for the placement drive "{drive.title}" by "{drive.company.name}".'})

@app.route('/api/get-student-applications', methods=['GET'])
@jwt_required()
def get_student_applications():
    driveId = request.args.get('driveId')
    role = get_jwt().get('role')
    applications = []
    if role == 'student':
        student = Student.query.join(User).filter_by(email=get_jwt_identity()).first()
        if not student:
            return jsonify({'message': 'Student not found.'}), 404
        applications = Application.query.join(Placement_Drive).filter(Application.student_id==student.student_id, Placement_Drive.status=='approved').all()
    if role == 'admin':
        applications = Application.query.all()
    if role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        if not company:
            return jsonify({'message': 'Company not found.'}), 404
        if not driveId:
            return jsonify({'message':'Drive ID missing.'}), 400
        applications = Application.query.join(Placement_Drive).filter(Placement_Drive.drive_id == driveId, Placement_Drive.company_id == company.company_id, Placement_Drive.status == "approved").all()
        
    application_list = []
    for app in applications:
        app_info = {
            'application_id': app.application_id,
            'student_name': app.student.name,
            'drive_id': app.placement_drive.drive_id,
            'title': app.placement_drive.title,
            'company_name': app.placement_drive.company.name,
            'status': app.status,
            'applied_at': app.applied_at.date().isoformat()
        }
        application_list.append(app_info)
    
    return jsonify({'studentApplications': application_list}), 200

@app.route('/api/get-application-details/<int:applicationId>', methods=['GET'])
@jwt_required()
def get_application_details(applicationId):
    role = get_jwt().get('role')
    application = None
    if role == 'admin':
        application = Application.query.get(applicationId)
    if role == 'company':
        company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
        application = Application.query.join(Placement_Drive).filter(Application.application_id==applicationId, Placement_Drive.company_id==company.company_id).first()
    if role == 'student':
        student = Student.query.join(User).filter_by(email=get_jwt_identity()).first()
        application = Application.query.filter_by(application_id = applicationId, student_id = student.student_id).first()

    if not application:
        return jsonify({'message':'Application Details not found'}), 404
    application_info = {
        'application_id':application.application_id,
        'student_name':application.student.name,
        'student_department':application.student.department,
        'drive_id':application.drive_id,
        'drive_title':application.placement_drive.title,
        'student_contact':application.student.contact,
        'status':application.status,
        'student_cgpa':application.student.cgpa
    }
    return jsonify({'application':application_info}), 200

@app.route('/api/company/save-application-status/<int:applicationId>', methods=['PATCH'])
@jwt_required()
def save_application_status(applicationId):
    role = get_jwt().get('role')
    data = request.get_json()
    if role != 'company':
        return jsonify({'message':'Access forbidden'}), 403
    company = Company.query.join(User).filter_by(email=get_jwt_identity()).first()
    if not company:
        return jsonify({'message':'Company not found.'}), 404
    application = Application.query.join(Placement_Drive).filter(Application.application_id==applicationId, Placement_Drive.company_id == company.company_id).first()
    if not application:
        return jsonify({'message':'Application not found.'}), 404
    application.status = data.get('status', application.status)
    
    try:
        db.session.commit()
        return jsonify({'message':'Candidate status has been updated successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'Something went wrong. Please try again.'}), 500

@app.route('/api/get-searched-drives', methods=['GET'])
@jwt_required()
def get_searched_drives():
    role = get_jwt().get('role')
    if role not in ['admin', 'student']:
        return jsonify({'message':'Access Forbidden'}), 403
    drives = Placement_Drive.query.join(Company).join(User).filter(Placement_Drive.status=='approved', User.is_active == True)
    
    grad_year = request.args.get('gradYear')
    cgpa = request.args.get('cgpa')
    department = request.args.get('department')
    skills_query = request.args.get('skills')
    skills = skills_query.split(',') if skills_query else []
    
    if grad_year:
        drives = drives.filter(Placement_Drive.year_threshold >= int(grad_year))
    if cgpa:
        drives = drives.filter(Placement_Drive.cgpa_threshold<=float(cgpa))
    if department:
        drives = drives.filter(Placement_Drive.branch == department)
    if skills:
        drives = drives.join(Placement_Drive.skills).filter(DriveSkill.skill_name.in_(skills))
            
    selected_drives = drives.all()
    
    drives_list = []
    for drive in selected_drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        drives_list.append(drive_info)
    return jsonify({'drives':drives_list}), 200

@app.route('/api/get-eligible-drives', methods=['GET'])
@jwt_required()
def get_eligible_drives():
    role = get_jwt().get('role')
    if role != 'student':
        return jsonify({'message':'Access Forbidden.'}), 403
    student = Student.query.join(User).filter_by(email = get_jwt_identity()).first()
    if not student:
        return jsonify({'message':'Student not found,'}), 404
    drives = Placement_Drive.query.join(Company).join(User).filter(
        User.is_active == True,
        Placement_Drive.status == 'approved',
        Placement_Drive.cgpa_threshold <= student.cgpa,
        Placement_Drive.year_threshold >= student.year,
        Placement_Drive.branch == student.department
    )
    eligible_drives = drives.all()
    
    drives_list = []
    for drive in eligible_drives:
        drive_info = {
            'drive_id': drive.drive_id,
            'company_name': drive.company.name,
            'title': drive.title
        }
        drives_list.append(drive_info)
    return jsonify({'drives': drives_list}), 200
    
@app.route('/api/get-searched-students', methods=['GET'])
@jwt_required()
def get_searched_students():
    role = get_jwt().get('role')
    if role != 'admin':
        return jsonify({'message':'Access Forbidden'}), 403
    
    students =  Student.query.join(User).filter_by(is_active = True)
    grad_year = request.args.get('gradYear')
    cgpa = request.args.get('cgpa')
    department = request.args.get('department')
    skills_query = request.args.get('skills')
    skills = skills_query.split(',') if skills_query else []
    
    if grad_year:
        students = students.filter(Student.year == int(grad_year))
    if cgpa:
        students = students.filter(Student.cgpa<=float(cgpa))
    if department:
        students = students.filter(Student.department == department)
    if skills:
        students = students.join(Student.skills).filter(StudentSkill.skill_name.in_(skills))
    
    selected_students = students.all()
    
    students_list = []
    for student in selected_students:
        student_info = {
            'student_id': student.student_id,
            'name':student.name,
            'department': student.department,
            'year': student.year,
            'cgpa':student.cgpa,
            'skills':[skill.skill_name for skill in student.skills]
        }
        students_list.append(student_info)
    return jsonify({'students':students_list}), 200

@app.route('/api/student/export-application-history', methods=['GET'])
@jwt_required()
def export_applications():
    student = Student.query.join(User).filter(User.email==get_jwt_identity()).first()
    export_application_history.delay(student.student_id)
    return jsonify({'message':'Application History has been exported. Please check your email.'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(email='admin@portal.com').first():
            admin = User(email='admin@portal.com', password_hash=generate_password_hash('adminpass'), role='admin')
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True)


