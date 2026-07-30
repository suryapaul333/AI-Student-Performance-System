from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3, os
from urllib.parse import quote_plus

app=Flask(__name__)
app.secret_key="ai-student-performance-final"
BASE=os.path.dirname(os.path.abspath(__file__))
DB=os.path.join(BASE,"student_performance.db")

CATALOG={'CSE': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Data Structures', 'Digital Logic Design', 'Object Oriented Programming'], '3': ['Discrete Mathematics', 'Database Management Systems', 'Operating Systems', 'Computer Networks', 'Computer Organization & Architecture'], '4': ['Design and Analysis of Algorithms', 'Software Engineering', 'Web Technologies', 'Theory of Computation', 'Artificial Intelligence'], '5': ['Machine Learning', 'Compiler Design', 'Computer Graphics', 'Distributed Systems', 'Professional Elective I'], '6': ['Cloud Computing', 'Data Mining', 'Cyber Security', 'Professional Elective II', 'Open Source Technologies'], '7': ['Internet of Things', 'Big Data Analytics', 'Professional Elective III', 'Project / Internship', 'Technical Seminar'], '8': ['Project Work', 'Professional Elective IV', 'Professional Elective V', 'Technical Seminar / Viva', 'Comprehensive Viva']}, 'AI & ML': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Data Structures', 'Object Oriented Programming', 'Digital Logic Design'], '3': ['Probability & Statistics', 'Database Management Systems', 'Operating Systems', 'Computer Networks', 'Artificial Intelligence'], '4': ['Machine Learning', 'Design and Analysis of Algorithms', 'Deep Learning', 'Theory of Computation', 'Web Technologies'], '5': ['Natural Language Processing', 'Computer Vision', 'Reinforcement Learning', 'Data Mining', 'Professional Elective I'], '6': ['Big Data Analytics', 'Generative AI', 'Cloud Computing', 'MLOps', 'Professional Elective II'], '7': ['Advanced Machine Learning', 'Deep Learning Applications', 'Professional Elective III', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective IV', 'Professional Elective V', 'Project Viva', 'Comprehensive Viva']}, 'AI & DS': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Data Structures', 'Object Oriented Programming', 'Digital Logic Design'], '3': ['Probability & Statistics', 'Database Management Systems', 'Data Visualization', 'Python for Data Science', 'Computer Networks'], '4': ['Machine Learning', 'Design and Analysis of Algorithms', 'Data Mining', 'Artificial Intelligence', 'Web Technologies'], '5': ['Big Data Analytics', 'Natural Language Processing', 'Deep Learning', 'Data Warehousing', 'Professional Elective I'], '6': ['Cloud Computing', 'Generative AI', 'MLOps', 'Business Intelligence', 'Professional Elective II'], '7': ['Advanced Data Analytics', 'Deep Learning Applications', 'Professional Elective III', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective IV', 'Professional Elective V', 'Project Viva', 'Comprehensive Viva']}, 'IT': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Data Structures', 'Object Oriented Programming', 'Digital Logic Design'], '3': ['Database Management Systems', 'Operating Systems', 'Computer Networks', 'Computer Organization', 'Software Engineering'], '4': ['Design and Analysis of Algorithms', 'Web Technologies', 'Theory of Computation', 'Artificial Intelligence', 'Professional Elective I'], '5': ['Machine Learning', 'Cloud Computing', 'Cyber Security', 'Data Mining', 'Professional Elective II'], '6': ['Big Data Analytics', 'Mobile Application Development', 'DevOps', 'Internet of Things', 'Professional Elective III'], '7': ['Advanced Web Technologies', 'Cloud Security', 'Professional Elective IV', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective V', 'Professional Elective VI', 'Project Viva', 'Comprehensive Viva']}, 'ECE': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Basic Electrical Engineering', 'Electronic Devices', 'Digital Logic Design'], '3': ['Signals and Systems', 'Network Analysis', 'Analog Circuits', 'Digital Electronics', 'Electromagnetic Waves'], '4': ['Control Systems', 'Microprocessors and Microcontrollers', 'Communication Systems', 'Linear IC Applications', 'Probability and Random Processes'], '5': ['Digital Signal Processing', 'VLSI Design', 'Embedded Systems', 'Antenna and Wave Propagation', 'Professional Elective I'], '6': ['Computer Architecture', 'IoT Systems', 'Wireless Communications', 'Optical Communications', 'Professional Elective II'], '7': ['Advanced VLSI', 'Embedded AI', 'RF and Microwave Engineering', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective III', 'Professional Elective IV', 'Project Viva', 'Comprehensive Viva']}, 'EEE': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Basic Electronics', 'Electrical Circuit Analysis', 'Electrical Machines I'], '3': ['Electrical Machines II', 'Power Systems I', 'Power Electronics', 'Control Systems', 'Measurements and Instrumentation'], '4': ['Power Systems II', 'Microprocessors and Microcontrollers', 'Electrical Drives', 'Signals and Systems', 'Power System Protection'], '5': ['High Voltage Engineering', 'Switchgear and Protection', 'Renewable Energy Sources', 'Digital Signal Processing', 'Professional Elective I'], '6': ['Power System Analysis', 'Smart Grid', 'Electric Vehicle Technology', 'Industrial Automation', 'Professional Elective II'], '7': ['Advanced Power Electronics', 'Power Quality', 'Energy Management', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective III', 'Professional Elective IV', 'Project Viva', 'Comprehensive Viva']}, 'MECH': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Engineering Mechanics', 'Basic Electrical Engineering', 'Manufacturing Processes'], '3': ['Thermodynamics', 'Fluid Mechanics', 'Strength of Materials', 'Machine Drawing', 'Material Science'], '4': ['Theory of Machines', 'Heat Transfer', 'Machine Design I', 'Manufacturing Technology', 'Metrology and Measurements'], '5': ['Machine Design II', 'Internal Combustion Engines', 'Refrigeration and Air Conditioning', 'CAD/CAM', 'Professional Elective I'], '6': ['Finite Element Methods', 'Robotics', 'Automobile Engineering', 'Industrial Engineering', 'Professional Elective II'], '7': ['Additive Manufacturing', 'Mechatronics', 'Advanced Manufacturing', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective III', 'Professional Elective IV', 'Project Viva', 'Comprehensive Viva']}, 'CIVIL': {'1': ['Engineering Mathematics I', 'Engineering Physics', 'Programming for Problem Solving', 'Engineering Graphics', 'English / Communication Skills'], '2': ['Engineering Mathematics II', 'Engineering Chemistry', 'Engineering Mechanics', 'Basic Electrical Engineering', 'Building Materials'], '3': ['Strength of Materials', 'Fluid Mechanics', 'Surveying', 'Structural Analysis I', 'Concrete Technology'], '4': ['Structural Analysis II', 'Geotechnical Engineering I', 'Hydrology and Water Resources', 'Transportation Engineering I', 'Environmental Engineering I'], '5': ['Design of Reinforced Concrete Structures', 'Geotechnical Engineering II', 'Transportation Engineering II', 'Environmental Engineering II', 'Professional Elective I'], '6': ['Design of Steel Structures', 'Estimation and Costing', 'Construction Management', 'Hydraulic Engineering', 'Professional Elective II'], '7': ['Advanced Structural Engineering', 'Remote Sensing and GIS', 'Earthquake Engineering', 'Project / Internship', 'Technical Seminar'], '8': ['Major Project', 'Professional Elective III', 'Professional Elective IV', 'Project Viva', 'Comprehensive Viva']}}

RESOURCE_MAP={
"c programming":("https://www.geeksforgeeks.org/c-programming-language/","https://www.youtube.com/results?search_query=C+Programming+Full+Course+freeCodeCamp"),
"python":("https://docs.python.org/3/tutorial/","https://www.youtube.com/results?search_query=Python+Full+Course+freeCodeCamp"),
"data structures":("https://www.geeksforgeeks.org/data-structures/","https://www.youtube.com/results?search_query=Data+Structures+Full+Course+freeCodeCamp"),
"database management systems":("https://www.geeksforgeeks.org/dbms/","https://www.youtube.com/results?search_query=DBMS+Full+Course+NPTEL"),
"operating systems":("https://www.geeksforgeeks.org/operating-systems/","https://www.youtube.com/results?search_query=Operating+Systems+Full+Course+NPTEL"),
"computer networks":("https://www.geeksforgeeks.org/computer-network-tutorials/","https://www.youtube.com/results?search_query=Computer+Networks+Full+Course+NPTEL"),
"machine learning":("https://www.geeksforgeeks.org/machine-learning/","https://www.youtube.com/results?search_query=Machine+Learning+Full+Course+NPTEL"),
"artificial intelligence":("https://www.geeksforgeeks.org/artificial-intelligence/","https://www.youtube.com/results?search_query=Artificial+Intelligence+Full+Course+NPTEL"),
"design and analysis of algorithms":("https://www.geeksforgeeks.org/fundamentals-of-algorithms/","https://www.youtube.com/results?search_query=Design+and+Analysis+of+Algorithms+Full+Course+NPTEL"),
"web technologies":("https://www.w3schools.com/","https://www.youtube.com/results?search_query=Web+Technologies+Full+Course"),
"java":("https://dev.java/learn/","https://www.youtube.com/results?search_query=Java+Full+Course+freeCodeCamp"),
"theory of computation":("https://www.geeksforgeeks.org/theory-of-computation-automata-tutorials/","https://www.youtube.com/results?search_query=Theory+of+Computation+Full+Course"),
"compiler design":("https://www.geeksforgeeks.org/compiler-design-tutorials/","https://www.youtube.com/results?search_query=Compiler+Design+Full+Course"),
"computer organization & architecture":("https://www.geeksforgeeks.org/computer-organization-and-architecture-tutorials/","https://www.youtube.com/results?search_query=Computer+Organization+Architecture+Full+Course"),
"software engineering":("https://www.geeksforgeeks.org/software-engineering/","https://www.youtube.com/results?search_query=Software+Engineering+Full+Course"),
"cloud computing":("https://www.geeksforgeeks.org/cloud-computing/","https://www.youtube.com/results?search_query=Cloud+Computing+Full+Course"),
"cyber security":("https://www.geeksforgeeks.org/cyber-security-tutorial/","https://www.youtube.com/results?search_query=Cyber+Security+Full+Course"),
"computer graphics":("https://www.geeksforgeeks.org/computer-graphics/","https://www.youtube.com/results?search_query=Computer+Graphics+Full+Course"),
"engineering mathematics i":("https://nptel.ac.in/courses/111105090","https://www.youtube.com/results?search_query=Engineering+Mathematics+1+Full+Course"),
"engineering mathematics ii":("https://nptel.ac.in/courses/111105035","https://www.youtube.com/results?search_query=Engineering+Mathematics+2+Full+Course"),
"engineering physics":("https://nptel.ac.in/courses/115105099","https://www.youtube.com/results?search_query=Engineering+Physics+Full+Course"),
"engineering chemistry":("https://nptel.ac.in/courses/104106096","https://www.youtube.com/results?search_query=Engineering+Chemistry+Full+Course")
}

def init_db():
    c=sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,phone TEXT UNIQUE,password TEXT)""")
    c.execute("""CREATE TABLE IF NOT EXISTS semester_subjects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    branch TEXT NOT NULL,
    year TEXT NOT NULL,
    semester TEXT NOT NULL,
    subject_names TEXT NOT NULL,
    UNIQUE(user_id,branch,year,semester)
)""")
    c.execute("""CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,name TEXT,year TEXT,semester TEXT,branch TEXT,
    attendance REAL,subject_names TEXT,subject_marks TEXT,assignment_marks TEXT,internal_marks TEXT,
    study_hours REAL,prediction TEXT,score REAL,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS custom_subjects(
    id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,branch TEXT,year TEXT,semester TEXT,
    subjects TEXT, UNIQUE(user_id,branch,year,semester))""")
    c.commit(); c.close()

def resources(subject):
    """Return subject-specific learning links for every subject.
    Existing curated links are preferred. For subjects without a curated
    resource, create a subject-specific PDF-notes search and video search.
    """
    k=subject.strip().lower()
    if k in RESOURCE_MAP:
        return RESOURCE_MAP[k]

    q=quote_plus(subject.strip())
    notes=f"https://www.google.com/search?q={q}+notes+filetype%3Apdf"
    video=f"https://www.youtube.com/results?search_query={q}+full+course+lecture"
    return (notes, video)


@app.route("/")
def home():
    return redirect(url_for("details") if session.get("user_id") else url_for("login"))

@app.route("/api/subjects")
def api_subjects():
    branch=request.args.get("branch","CSE")
    year=request.args.get("year","1")
    sem=request.args.get("semester","1")
    semester_no=(int(year)-1)*2+int(sem)
    subjects=CATALOG.get(branch,CATALOG["CSE"]).get(str(semester_no),[])
    if session.get("user_id"):
        c=sqlite3.connect(DB)
        row=c.execute("SELECT subjects FROM custom_subjects WHERE user_id=? AND branch=? AND year=? AND semester=?",
                      (session["user_id"],branch,year,sem)).fetchone()
        c.close()
        if row and row[0]: subjects=row[0].split("|")
    return jsonify({"subjects":subjects,"semester_number":semester_no})

@app.route("/api/save-subjects",methods=["POST"])
def save_subjects():
    if not session.get("user_id"): return jsonify({"ok":False,"error":"Login required"}),401
    data=request.get_json(force=True)
    branch=str(data.get("branch","CSE")); year=str(data.get("year","1")); sem=str(data.get("semester","1"))
    subjects=[str(x).strip() for x in data.get("subjects",[]) if str(x).strip()]
    if not subjects: return jsonify({"ok":False,"error":"Enter at least one subject"}),400
    subjects=subjects[:10]
    c=sqlite3.connect(DB)
    c.execute("INSERT INTO custom_subjects(user_id,branch,year,semester,subjects) VALUES(?,?,?,?,?) ON CONFLICT(user_id,branch,year,semester) DO UPDATE SET subjects=excluded.subjects",
              (session["user_id"],branch,year,sem,"|".join(subjects)))
    c.commit(); c.close()
    return jsonify({"ok":True,"subjects":subjects})

@app.route("/register",methods=["GET","POST"])
def register():
    error=""
    if request.method=="POST":
        try:
            c=sqlite3.connect(DB)
            c.execute("INSERT INTO users(name,email,phone,password) VALUES(?,?,?,?)",
                      (request.form["name"],request.form["email"],request.form["phone"],request.form["password"]))
            c.commit(); c.close(); return redirect(url_for("login"))
        except sqlite3.IntegrityError: error="Email or phone number is already registered."
    return render_template("register.html",error=error)

@app.route("/login",methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        x=request.form["identity"]
        c=sqlite3.connect(DB)
        row=c.execute("SELECT id,name FROM users WHERE (email=? OR phone=?) AND password=?",
                      (x,x,request.form["password"])).fetchone()
        c.close()
        if row:
            session["user_id"],session["user_name"]=row
            return redirect(url_for("details"))
        error="Invalid email/phone or password."
    return render_template("login.html",error=error)


@app.route("/api/saved-subjects")
def saved_subjects():
    if not session.get("user_id"):
        return jsonify({"subjects":[]})
    branch=request.args.get("branch","")
    year=request.args.get("year","")
    sem=request.args.get("semester","")
    c=sqlite3.connect(DB)
    row=c.execute("""SELECT subjects FROM custom_subjects
                     WHERE user_id=? AND branch=? AND year=? AND semester=?""",
                  (session["user_id"],branch,year,sem)).fetchone()
    c.close()
    return jsonify({"subjects": row[0].split("|") if row and row[0] else []})

@app.route("/details",methods=["GET","POST"])
def details():
    if not session.get("user_id"): return redirect(url_for("login"))
    error=""
    if request.method=="POST":
        try:
            year=request.form["year"]; sem=request.form["semester"]; branch=request.form["branch"]
            count=int(request.form.get("subject_count","5"))
            names=[request.form[f"subject{i}_name"].strip() for i in range(1,count+1)]
            marks=[float(request.form[f"subject{i}"]) for i in range(1,count+1)]
            assigns=[float(request.form[f"assignment{i}"]) for i in range(1,count+1)]
            internals=[float(request.form[f"internal{i}"]) for i in range(1,count+1)]
            attendance=float(request.form["attendance"]); study=float(request.form["study_hours"])
            if len(names)<2: raise ValueError("Please enter at least 2 subjects.")
            if not all(names): raise ValueError("Please enter a name for every subject.")
            if any(x<0 or x>100 for x in [attendance]): raise ValueError("Attendance must be between 0 and 100.")
            if any(x<0 or x>70 for x in marks): raise ValueError("External marks must be between 0 and 70.")
            if any(x<0 or x>30 for x in internals): raise ValueError("Internal marks must be between 0 and 30.")
            if any(x<0 or x>25 for x in assigns): raise ValueError("Assignment marks must be between 0 and 25.")
            # Convert each component to percentage before combining so the model is scale-independent.
            ext_pct=[m/70*100 for m in marks]
            int_pct=[m/30*100 for m in internals]
            ass_pct=[m/25*100 for m in assigns]
            avg=sum(ext_pct)/len(ext_pct)
            score=round(attendance*.25+avg*.35+sum(ass_pct)/len(ass_pct)*.10+sum(int_pct)/len(int_pct)*.20+min(study*10,100)*.10,2)
            label="Excellent" if score>=80 else "Good" if score>=65 else "Average" if score>=50 else "Needs Improvement"
            message={"Excellent":"Excellent performance. Keep your routine.",
                     "Good":"Good performance. Strengthen the weaker subjects.",
                     "Average":"Follow the study plan consistently and practice more.",
                     "Needs Improvement":"Focus on weak subjects and revise every day."}[label]
            weak=sorted(zip(names,ext_pct),key=lambda x:x[1])[:2]
            weak_names={n for n,_ in weak}
            all_subjects=[
                {"name":n,"mark":round(m,2),"notes":resources(n)[0],"video":resources(n)[1],
                 "weak":n in weak_names}
                for n,m in zip(names,ext_pct)
            ]
            weak_data=[{"name":n,"mark":m,"notes":resources(n)[0],"video":resources(n)[1]} for n,m in weak]
            plan=[
              ("Day 1",weak_data[0]["name"],"Concepts + notes","60 min"),
              ("Day 2",weak_data[1]["name"],"Concepts + examples","60 min"),
              ("Day 3",weak_data[0]["name"],"Practice questions","75 min"),
              ("Day 4",weak_data[1]["name"],"Practice problems","75 min"),
              ("Day 5",weak_data[0]["name"],"Revision + previous questions","60 min"),
              ("Day 6",weak_data[1]["name"],"Revision + previous questions","60 min"),
              ("Day 7","Both weak subjects","Mock test + error review","90 min")]
            c=sqlite3.connect(DB)
            c.execute("INSERT INTO custom_subjects(user_id,branch,year,semester,subjects) VALUES(?,?,?,?,?) ON CONFLICT(user_id,branch,year,semester) DO UPDATE SET subjects=excluded.subjects",
                      (session["user_id"],branch,year,sem,"|".join(names)))
            c.execute("""INSERT INTO predictions(user_id,name,year,semester,branch,attendance,subject_names,subject_marks,assignment_marks,internal_marks,study_hours,prediction,score)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",(session["user_id"],request.form["name"],year,sem,branch,attendance,
            "|".join(names),"|".join(map(str,marks)),"|".join(map(str,assigns)),"|".join(map(str,internals)),study,label,score))
            c.commit(); c.close()
            session["result"]={"score":score,"label":label,"message":message,"weak":weak_data,
                               "all_subjects":all_subjects,"plan":plan,
                               "year":year,"semester":sem,"branch":branch}
            return redirect(url_for("prediction"))
        except ValueError as e: error=str(e)
    return render_template("details.html",catalog=CATALOG,user_name=session.get("user_name",""),error=error)

@app.route("/prediction")
def prediction():
    if not session.get("user_id"): return redirect(url_for("login"))
    return render_template("prediction.html",result=session.get("result"))

@app.route("/history")
def history():
    if not session.get("user_id"): return redirect(url_for("login"))
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row
    rows=c.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC",(session["user_id"],)).fetchall()
    c.close(); return render_template("history.html",rows=rows)

@app.route("/logout")
def logout(): session.clear(); return redirect(url_for("login"))

if __name__=="__main__":
    init_db(); app.run(debug=True)
