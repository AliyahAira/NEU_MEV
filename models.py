from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    students = db.relationship('Student', backref='college', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    is_eligible = db.Column(db.Boolean, default=False)
    
    # Medical examination fields
    physical_exam = db.Column(db.Boolean, default=False)
    vital_signs = db.Column(db.Boolean, default=False)
    vision_test = db.Column(db.Boolean, default=False)
    hearing_test = db.Column(db.Boolean, default=False)
    cbc_test = db.Column(db.Boolean, default=False)
    urinalysis = db.Column(db.Boolean, default=False)
    drug_test = db.Column(db.Boolean, default=False)
    chest_xray = db.Column(db.Boolean, default=False)
    tb_screening = db.Column(db.Boolean, default=False)
    hepatitis_b = db.Column(db.Boolean, default=False)
    mmr = db.Column(db.Boolean, default=False)
    varicella = db.Column(db.Boolean, default=False)
    tdap = db.Column(db.Boolean, default=False)
    meningococcal = db.Column(db.Boolean, default=False)
    covid_vaccine = db.Column(db.Boolean, default=False)
    hiv_test = db.Column(db.Boolean, default=False)
    
    def check_eligibility(self):
        """Determine if student meets all requirements"""
        basic_requirements = [
            self.physical_exam,
            self.vital_signs,
            self.cbc_test,
            self.urinalysis,
            self.chest_xray,
            self.tb_screening,
            self.hepatitis_b,
            self.mmr,
            self.varicella,
            self.tdap,
        ]
        
        # Engineering students need vision test
        if self.college.name == "College of Engineering and Architecture":
            basic_requirements.append(self.vision_test)
            
        return all(basic_requirements)

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
    student = db.relationship('Student', backref='uploaded_files')