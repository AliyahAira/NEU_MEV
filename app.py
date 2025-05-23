from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from models import db, Student, College, UploadedFile
from werkzeug.utils import secure_filename
import os
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
db.init_app(app)

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('templates/admin', exist_ok=True)
os.makedirs('templates/student', exist_ok=True)

# Initialize database
with app.app_context():
    db.create_all()
    if College.query.count() == 0:
        colleges = [
            College(name="College of Informatics and Computing Studies"),
            College(name="College of Arts and Sciences"),
            College(name="College of Engineering and Architecture")
        ]
        db.session.add_all(colleges)
        db.session.commit()

@app.route('/')
def welcome():
    return render_template('welcome.html')

# Admin routes
@app.route('/admin')
def admin_home():
    colleges = College.query.all()
    return render_template('admin/home.html', colleges=colleges)

@app.route('/admin/students/<int:college_id>', methods=['GET', 'POST'])
def admin_student_list(college_id):
    college = College.query.get_or_404(college_id)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            try:
                stream = file.stream.read().decode("UTF8")
                csv_reader = csv.DictReader(stream.splitlines())
                
                for row in csv_reader:
                    student = Student(
                        name=row['name'],
                        student_id=row['student_id'],
                        college_id=college_id
                    )
                    db.session.add(student)
                
                db.session.commit()
                flash('Students imported successfully!')
            except Exception as e:
                flash(f'Error importing students: {str(e)}')
    
    students = Student.query.filter_by(college_id=college_id).all()
    return render_template('admin/student_list.html', college=college, students=students)

@app.route('/admin/verify/<int:student_id>', methods=['GET', 'POST'])
def admin_verify_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.physical_exam = 'physical_exam' in request.form
        student.vital_signs = 'vital_signs' in request.form
        student.vision_test = 'vision_test' in request.form
        student.hearing_test = 'hearing_test' in request.form
        student.cbc_test = 'cbc_test' in request.form
        student.urinalysis = 'urinalysis' in request.form
        student.drug_test = 'drug_test' in request.form
        student.chest_xray = 'chest_xray' in request.form
        student.tb_screening = 'tb_screening' in request.form
        student.hepatitis_b = 'hepatitis_b' in request.form
        student.mmr = 'mmr' in request.form
        student.varicella = 'varicella' in request.form
        student.tdap = 'tdap' in request.form
        student.meningococcal = 'meningococcal' in request.form
        student.covid_vaccine = 'covid_vaccine' in request.form
        student.hiv_test = 'hiv_test' in request.form
        
        student.is_eligible = student.check_eligibility()
        
        db.session.commit()
        flash('Verification submitted successfully!')
        return redirect(url_for('admin_student_list', college_id=student.college_id))
    
    return render_template('admin/verify.html', student=student)

@app.route('/admin/profile/<int:student_id>')
def admin_student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    uploaded_files = UploadedFile.query.filter_by(student_id=student_id).all()
    return render_template('admin/profile.html', student=student, uploaded_files=uploaded_files)

# Student routes
@app.route('/student/dashboard/<student_id>')
def student_dashboard(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    uploaded_files = UploadedFile.query.filter_by(student_id=student.id).all()
    return render_template('student/dashboard.html', student=student, uploaded_files=uploaded_files)

@app.route('/student/upload/<student_id>', methods=['GET', 'POST'])
def student_upload(student_id):
    student = Student.query.filter_by(student_id=student_id).first_or_404()
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            uploaded_file = UploadedFile(
                filename=filename,
                filepath=filepath,
                student_id=student.id,
                file_type=request.form.get('file_type', 'other')
            )
            db.session.add(uploaded_file)
            db.session.commit()
            
            flash('File uploaded successfully!')
            return redirect(url_for('student_dashboard', student_id=student.student_id))
    
    return render_template('student/upload.html', student=student)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)