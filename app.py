from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Student, College
from werkzeug.utils import secure_filename
import os
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///enrollment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()
    # Add default colleges if they don't exist
    if College.query.count() == 0:
        colleges = [
            College(name="College of Informatics and Computing Studies"),
            College(name="College of Arts and Sciences"),
            College(name="College of Engineering and Architecture")
        ]
        db.session.add_all(colleges)
        db.session.commit()

@app.route('/')
def home():
    colleges = College.query.all()
    return render_template('home.html', colleges=colleges)

@app.route('/students/<int:college_id>', methods=['GET', 'POST'])
def student_list(college_id):
    college = College.query.get_or_404(college_id)
    
    if request.method == 'POST':
        # Handle CSV upload
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
            
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
            
        if file and file.filename.endswith('.csv'):
            try:
                # Read CSV and add students
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
    return render_template('student_list.html', college=college, students=students)

@app.route('/verify/<int:student_id>', methods=['GET', 'POST'])
def verify_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        # Process verification form
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
        
        # Check eligibility
        student.is_eligible = student.check_eligibility()
        
        db.session.commit()
        flash('Verification submitted successfully!')
        return redirect(url_for('student_list', college_id=student.college_id))
    
    return render_template('verify.html', student=student)

@app.route('/profile/<int:student_id>')
def student_profile(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('profile.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)