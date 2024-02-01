from flask import Flask, render_template, session, redirect
from app import app
from functools import wraps
from myModels import *
# from recognitionProcess import *

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap


def admin_login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'admin_logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/login/admin/')
  return wrap

# Routes
@app.route('/')
def home():
  return render_template('home.html')

@app.route("/login/")
def loginHtml():
  return render_template('login.html')


@app.route("/admin/")
def adminLogin():
  return render_template("adminLogin.html")


@app.route('/dashboard/')
@login_required 
def dashboard():
  return render_template('dashboard.html')



@app.route('/user/signup/', methods=['POST'])
def signup():
  return User().signup()



@app.route('/user/signout/')
def signout():
  return User().signout()



@app.route('/user/login/', methods=['POST'])
def login():
  return User().login()


@app.route('/admin/login/', methods=['POST'])
def adminAuth():
  return Admin().login()


@app.route("/admin/signout/")
def adminSignout():
  return Admin().signout()


@app.errorhandler(404)
def error(error):
  return render_template('error.html'), 404



#? Face Recognition Processes

@app.route("/admin/year/")
@admin_login_required
def year():
  # FaceRec().selectYear()
  return render_template("year.html")

@app.route("/admin/yearCheck/", methods=['POST'])
@admin_login_required
def yearCheck():
  return FaceRecDetails().yearCheck()
  # return render_template("credentials.html")



# /admin/facerecognition/
@app.route("/admin/subject/")
@admin_login_required
def subject():

  return render_template("subject.html", year=session['year'], subjectList = session['subjects'])


@app.route("/admin/subjectCheck/", methods=['POST', 'GET'])
@admin_login_required
def subjectCheck():
  return FaceRecDetails().subjectCheck()



@app.route("/admin/facerecognition/")
@admin_login_required
def facerecognition():
  return render_template("facerecognition.html")

@app.route("/admin/facerecognition/process_frames/", methods=['POST'])
@admin_login_required 
def process():
  return FaceRecDetails().process_frames()

@app.route("/admin/detected/")
@admin_login_required
def detected():
  return render_template("detectedFaces.html")

@app.route("/admin/submit/")
@admin_login_required
def submit():
  return render_template("submit.html")

@app.route("/admin/submitCheck/", methods=['POST'])
@admin_login_required
def submitCheck():
  return FaceRecDetails().move_forward()
  # return render_template("submit.html")


@app.route("/user/select/", methods=['POST', 'GET'])
@login_required
def userSelect():
  return render_template("selectMonth.html")

@app.route("/user/attendanceCheck", methods=['POST'])
@login_required
def userMonth():
  return User().checkAttendance()


@app.route("/user/attendance", methods=['GET'])
@login_required
def userMonthDis():
  return render_template('attendanceChart.html', data = jsonify(session['monthAttendance']))

@app.route("/api/attenanceList/")
def listAttend():
    return jsonify(session['monthAttendance'])


# Defaulters

@admin_login_required
@app.route("/yearDefaulters", methods=["POST", "GET"])
def yearDefaulters():
  return render_template("month-defaulter.html")

@admin_login_required
@app.route("/admin/defaultersCheck/", methods=["POST"])
def defaultersCheck():
  return Admin().defaultersCheck()

@admin_login_required
@app.route("/admin/defaulters/", methods=["GET"])
def defaulters():
  return render_template(defaulters.html, res=zip(session['rollNum'], session['percentage']))