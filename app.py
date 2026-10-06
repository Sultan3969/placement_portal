from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session

student_applications = []


def parse_requirements(raw_text):
    raw_text = (raw_text or '').strip()
    if not raw_text:
        return {
            "CGPA": "As per company policy",
            "Skills": "Not specified",
            "Rounds": "As per company policy"
        }

    requirements = {}
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue
        if ':' in line:
            key, value = [part.strip() for part in line.split(':', 1)]
            requirements[key] = value
        else:
            requirements["Details"] = line

    if not requirements:
        requirements["Details"] = raw_text

    return requirements


company_requirements = {
    "Google": {
        "CGPA": ">= 8.0",
        "Skills": "DSA, OOP, Problem Solving",
        "Rounds": "Aptitude, Technical Interview, HR"
    },
    "Microsoft": {
        "CGPA": ">= 8.5",
        "Skills": "Data Structures, System Design, C++/Java",
        "Rounds": "Online Assessment, Technical, Managerial"
    },
    "Amazon": {
        "CGPA": ">= 7.5",
        "Skills": "DSA, Java/Python, Leadership Principles",
        "Rounds": "Aptitude, Technical, Final Interview"
    },
    "TCS": {
        "CGPA": ">= 6.0",
        "Skills": "Communication, Basics of Programming, Aptitude",
        "Rounds": "Aptitude, Technical, HR"
    },
    "Infosys": {
        "CGPA": ">= 6.0",
        "Skills": "Core Java / Python, Logical Reasoning",
        "Rounds": "Aptitude, Technical, HR"
    }
}

# --- User Data ---
valid_users = {
    "R23EF330": "Reva@123",
    "R23EF331": "Reva@123",
    "R23EF334": "Reva@123",
    "R23EF335": "Reva@123",
    "R23EF336": "Reva@123",
    "R23EF337": "Reva@123"
}

admin_username = "R23EF337"
admin_password = "Reva@123"

# --- Company Data ---
technical_companies = [
    {"name": "Google", "date": "2026-10-08"},
    {"name": "Microsoft", "date": "2026-10-10"},
    {"name": "Amazon", "date": "2026-10-12"},
    {"name": "TCS", "date": "2026-10-15"},
    {"name": "Infosys", "date": "2026-10-17"},
    {"name": "Cisco", "date": "2026-10-19"},
    {"name": "Oracle", "date": "2026-10-21"},
    {"name": "IBM", "date": "2026-10-23"},
    {"name": "Adobe", "date": "2026-10-25"},
    {"name": "Samsung R&D", "date": "2026-10-27"},
    {"name": "Qualcomm", "date": "2026-10-29"},
    {"name": "NVIDIA", "date": "2026-10-31"},
    {"name": "Wipro", "date": "2026-11-02"},
    {"name": "HCL Technologies", "date": "2026-11-04"},
    {"name": "Capgemini", "date": "2026-11-06"},
    {"name": "ZS Associates", "date": "2026-11-08"},
    {"name": "Hexaware", "date": "2026-11-10"},
    {"name": "Tech Mahindra", "date": "2026-11-12"},
    {"name": "Mindtree", "date": "2026-11-14"},
    {"name": "Publicis Sapient", "date": "2026-11-16"},
    {"name": "Atlassian", "date": "2026-11-18"},
    {"name": "Meta", "date": "2026-11-20"},
    {"name": "PayPal", "date": "2026-11-22"},
    {"name": "Salesforce", "date": "2026-11-24"},
    {"name": "SAP", "date": "2026-11-26"}
]


non_technical_companies = [
    {"name": "Deloitte", "date": "2026-10-09"},
    {"name": "Accenture", "date": "2026-10-11"},
    {"name": "KPMG", "date": "2026-10-13"},
    {"name": "EY", "date": "2026-10-16"},
    {"name": "Genpact", "date": "2026-10-18"},
    {"name": "Cognizant", "date": "2026-10-20"},
    {"name": "Infosys BPM", "date": "2026-10-22"},
    {"name": "WNS Global", "date": "2026-10-24"},
    {"name": "Tata Communications", "date": "2026-10-26"},
    {"name": "HDFC Life", "date": "2026-10-28"},
    {"name": "ICICI Prudential", "date": "2026-10-30"},
    {"name": "Sutherland", "date": "2026-11-01"},
    {"name": "Capita", "date": "2026-11-03"},
    {"name": "Teleperformance", "date": "2026-11-05"},
    {"name": "Firstsource", "date": "2026-11-07"},
    {"name": "Concentrix", "date": "2026-11-09"},
    {"name": "Randstad", "date": "2026-11-11"},
    {"name": "Byju’s", "date": "2026-11-13"},
    {"name": "UpGrad", "date": "2026-11-15"},
    {"name": "Unacademy", "date": "2026-11-17"},
    {"name": "PwC", "date": "2026-11-19"},
    {"name": "Morgan Stanley", "date": "2026-11-21"},
    {"name": "HSBC", "date": "2026-11-23"},
    {"name": "JPMorgan Chase", "date": "2026-11-25"},
    {"name": "Barclays", "date": "2026-11-27"}
]


# --- Home Page ---
@app.route('/')
def home():
    return render_template("index.html")

# --- Admin Login ---
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template("error.html", message="❌ Invalid Admin Credentials")
    return render_template("admin_login.html")

# --- Admin Dashboard ---
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    # Delete logic
    delete_type = request.args.get('type')
    delete_index = request.args.get('index')
    if delete_type and delete_index is not None:
        try:
            index = int(delete_index)
            if delete_type == 'technical':
                deleted_company = technical_companies.pop(index)
                company_requirements.pop(deleted_company['name'], None)
            elif delete_type == 'nontechnical':
                deleted_company = non_technical_companies.pop(index)
                company_requirements.pop(deleted_company['name'], None)
        except Exception as e:
            print("Delete error:", e)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'update_requirements':
            company_name = request.form.get('company_name')
            category = request.form.get('category')
            requirements_text = request.form.get('requirements', '')
            if company_name:
                company_requirements[company_name] = parse_requirements(requirements_text)
                for company_list, list_name in [(technical_companies, 'technical'), (non_technical_companies, 'nontechnical')]:
                    if list_name == category:
                        for item in company_list:
                            if item.get('name') == company_name:
                                item['requirements'] = requirements_text
                                break
        else:
            name = request.form['company']
            category = request.form['category']
            date = request.form['date']
            requirements_text = request.form.get('requirements', '')
            if category == 'technical':
                technical_companies.append({
                    "name": name,
                    "date": date,
                    "requirements": requirements_text
                })
            else:
                non_technical_companies.append({
                    "name": name,
                    "date": date,
                    "requirements": requirements_text
                })
            company_requirements[name] = parse_requirements(requirements_text)

    technical_list = []
    for company in technical_companies:
        technical_list.append({
            "name": company["name"],
            "date": company["date"],
            "requirements": company.get("requirements") or company_requirements.get(company["name"], {
                "CGPA": "As per company policy",
                "Skills": "Not specified",
                "Rounds": "As per company policy"
            })
        })

    nontechnical_list = []
    for company in non_technical_companies:
        nontechnical_list.append({
            "name": company["name"],
            "date": company["date"],
            "requirements": company.get("requirements") or company_requirements.get(company["name"], {
                "CGPA": "As per company policy",
                "Skills": "Not specified",
                "Rounds": "As per company policy"
            })
        })

    return render_template("admin.html",
                           technical=technical_list,
                           nontechnical=nontechnical_list,
                           applications=list(reversed(student_applications)))


# ✅ FIXED: Only one definition of admin logout
@app.route('/admin-logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

# --- Student Login ---
@app.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_users.get(username) == password:
            session['user'] = username
            return redirect(url_for('select_category'))
        else:
            return render_template('error.html', message="Invalid username or password")
    return render_template("student_login.html")

# --- Category Selector Before Dashboard ---
@app.route('/select-category', methods=['GET', 'POST'])
def select_category():
    if not session.get('user'):
        return redirect(url_for('student_login'))

    if request.method == 'POST':
        category = request.form['category']
        if category == "technical":
            return render_template("student_dashboard.html",
                                   category="Technical Companies",
                                   category_key="technical",
                                   companies=technical_companies)
        else:
            return render_template("student_dashboard.html",
                                   category="Non-Technical Companies",
                                   category_key="non-technical",
                                   companies=non_technical_companies)
    return render_template("select_category.html")


@app.route('/student/company-details', methods=['GET'])
def student_company_details():
    if not session.get('user'):
        return redirect(url_for('student_login'))

    company_name = request.args.get('company')
    category = request.args.get('category')
    if not company_name or not category:
        return redirect(url_for('select_category'))

    requirements = company_requirements.get(company_name, {
        "CGPA": "As per company policy",
        "Skills": "Good communication and technical basics",
        "Rounds": "Screening, Technical, HR"
    })
    applied = request.args.get('applied') == '1'

    return render_template(
        'company_details.html',
        company=company_name,
        category=category,
        requirements=requirements,
        applied=applied
    )


@app.route('/student/apply', methods=['POST'])
def apply_company():
    if not session.get('user'):
        return redirect(url_for('student_login'))

    company_name = request.form.get('company')
    category = request.form.get('category')
    student_name = session.get('user')

    if not company_name or not category:
        return redirect(url_for('select_category'))

    already_applied = any(
        app_item["student"] == student_name and
        app_item["company"] == company_name and
        app_item["category"] == category
        for app_item in student_applications
    )

    if not already_applied:
        student_applications.append({
            "student": student_name,
            "company": company_name,
            "category": category,
            "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return redirect(url_for('student_company_details', company=company_name, category=category, applied=1))

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True)
