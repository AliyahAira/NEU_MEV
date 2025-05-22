
# 🎓 NEUMEV - Enrollment Eligibility Verification System

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.0%2B-lightgrey)
![SQLite](https://img.shields.io/badge/sqlite-3-green)

A web-based expert system that verifies student eligibility for enrollment based on medical and academic requirements.

## ✨ Features
- **College-specific verification** for 3 colleges
- **Comprehensive medical checklist** (physical exams, lab tests, vaccinations)
- **Automated eligibility determination**
- **CSV student import** functionality
- **Responsive web interface**

## 🛠️ Setup Guide (Local Development)

### Prerequisites
- Python 3.8+
- VS Code (recommended)
- Git (for cloning)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/NEUMEV.git
   cd NEUMEV
2. **Create virtual environment**:
   ```bash
   python -m venv venv
3. **Activate environment**:
   ```bash
   venv\Scripts\activate
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

### Running the Application
   python app.py

### Project Structure
NEUMEV/
├── app.py                # Main application
├── init_db.py            # Database initialization
├── models.py             # Database models
├── requirements.txt      # Dependencies
├── static/
│   └── style.css         # Custom styles
└── templates/            # HTML templates

### 💡 Usage Instructions

1. Import Students:
- Prepare CSV file with name,student_id columns
- Upload via college-specific page

2. Verify Eligibility:
- Click "Verify" on student record
- Complete the medical checklist
- System auto-determines eligibility
  
3. View Profiles:
- Check detailed verification status
- See missing requirements

   
   
   


   
