from celery_init import celery_app
from models import db, User, Student, Company, StudentSkill, Placement_Drive, Application, DriveSkill
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText
import smtplib 
from flask import render_template
import os
import csv

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS='rama@gmail.com'
SENDER_PASSWORD=''

def send_email(to_address,subject,message,content="text",attachment=None):
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html":
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    if attachment:
        filename = os.path.basename(attachment)
        with open(attachment,"rb") as a:
            part = MIMEBase("text", "csv")
            part.set_payload(a.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)          

    s = smtplib.SMTP(host=SERVER_SMTP_HOST, port=SERVER_SMTP_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()
    return True

@celery_app.task
def send_monthly_report():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        return "No admin user found."
    drives = Placement_Drive.query.all()
    drive_info = []
    for drive in drives:
        applications_count = Application.query.filter_by(drive_id=drive.drive_id).count()
        selected_students = Application.query.filter_by(status='Selected', drive_id = drive.drive_id).count()
        rejected_students = Application.query.filter_by(status='Rejected', drive_id = drive.drive_id).count()
        under_review_students = Application.query.filter_by(status='Under Review', drive_id = drive.drive_id).count()
        drive_info.append({
            'drive_id':drive.drive_id,
            'title':drive.title,
            'applied_count':applications_count,
            'company_name': drive.company.name,
            'selected_count':selected_students,
            'rejected_count':rejected_students,
            'under_review_count':under_review_students
        })
    html_content = render_template('monthly_report.html', drives=drive_info)
    send_email(admin.email, "Monthly Report", html_content, content="html")
    return("Monthly Report Done.")
    
@celery_app.task
def send_daily_reminder():
    students = Student.query.all()
    drives = Placement_Drive.query.filter_by(status='approved').all()
    if not students:
        return "NO STUDENTS FOUND."
    if not drives:
        return "No data to be sent."
    for student in students:
        drive_info = []
        for drive in drives:
            drive_info.append({
                'drive_id':drive.drive_id,
                'company_name':drive.company.name,
                'title':drive.title,
                'deadline':drive.deadline.date().isoformat()
            })
            
        html_content = render_template('student_daily_reminders.html', drives=drive_info)
        send_email(student.user.email, "Daily Reminders", html_content, content="html")
    return("Daily reminders sent.")
    
@celery_app.task
def company_monthly_report():
    companies = Company.query.all()
    if not companies:
        return "NO COMPANIES FOUND."
    for company in companies:
        drives = Placement_Drive.query.filter_by(company_id = company.company_id).all()
        if not drives:
            return "Drives not found."
        drive_info = []
        for drive in drives:
            applied_count = Application.query.filter_by(drive_id=drive.drive_id).count()
            selected_students = Application.query.filter_by(status='Selected', drive_id = drive.drive_id).count()
            rejected_students = Application.query.filter_by(status='Rejected', drive_id = drive.drive_id).count()
            under_review_students = Application.query.filter_by(status='Under Review', drive_id = drive.drive_id).count()
            drive_info.append({
                'drive_id':drive.drive_id,
                'applied_count':applied_count,
                'selected_count':selected_students,
                'rejected_count':rejected_students,
                'under_review_count':under_review_students,
                'title':drive.title
            })
        html_content = render_template('company_monthly_report.html', drives=drive_info)
        send_email(company.user.email, "Placement Statistics", html_content, content="html")
    return("Company monthly report sent.")
    
@celery_app.task
def export_application_history(studentId):
    student = Student.query.get(studentId)
    applications = Application.query.filter_by(student_id = studentId).all()
    filename = f"application_history_{studentId}.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Application ID', 'Drive ID', 'Job Title', 'Company Name', 'Applied On', 'Status'])
    
        for app in applications:
            writer.writerow([
                app.application_id,
                app.placement_drive.drive_id,
                app.placement_drive.title,
                app.placement_drive.company.name,
                app.applied_at.date().isoformat(),
                app.status
            ])
    
    email_body = "Hello, please find your application history attached."
    send_email(student.user.email, "Your Application History", message=email_body, content="text", attachment=filename)
    if os.path.exists(filename):
        os.remove(filename)
    return("Application History sent to the user.")
            