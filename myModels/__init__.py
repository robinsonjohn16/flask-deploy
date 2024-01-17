from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from db import *
import uuid
from dotenv import load_dotenv
from flask import  jsonify, request, session
import numpy as numpy
import cv2
import face_recognition
from datetime import datetime
from app import app
from ordered_set import OrderedSet
from myEncoding import TyEncodingFirst
from myEncoding  import TyEncodingSecond
from myEncoding import TyNameList
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import cloudinary 
import cloudinary.uploader 
load_dotenv()

UPLOAD_FOLDER = './static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User:
  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200


  def signup(self):
    db = client.user_login_system
    print(request.form)
    print(request.files)


    uploaded_img = request.files['imagefile'] 
    if uploaded_img:
      file_extension = uploaded_img.filename.rsplit('.', 1)[1].lower()
      allowed_extensions = {'jpg', 'jpeg', 'png'}
      if file_extension not in allowed_extensions:
        return jsonify({'error': 'Invalid file extension. Allowed extensions: jpg, jpeg, png'}), 400
      filename = secure_filename(uploaded_img.filename)
      uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      print('File uploaded successfully')
      print(uploaded_img)
      cloudinary_res = {}
      if filename != "":
        try:
          cloudinary.config(
            cloud_name = os.getenv("cloud_name"), 
            api_key = os.getenv("api_key"), 
            api_secret = os.getenv("api_secret") 
           )
          cloudinary_res = cloudinary.uploader.upload(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          print("url", cloudinary_res['url'])
        except Exception as e:
           return jsonify({'error': f'There is Certain Error in loading the file, try again later {e}', }), 400

    print(request.form.get('password'))
    if(len(request.form.get('password')) < 8):
       return jsonify({'error' : 'Password must contain atleast 8 character'}), 405
    
    if( "'" in request.form.get('password') or '"' in request.form.get('password')):
      return jsonify({"error": "Password cannot contain Single or Double Quotes"}), 405
             

    user = {
      "_id": uuid.uuid4().hex,
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password'),
      "roll": request.form.get('roll'),
      "year" : request.form["selectOption"],
      # "year": request.form.get('year'),
      "parentMail" : request.form.get('parMail'),
      "profile" : cloudinary_res['url']
    }

    # Encrypt the password
    user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if db.users.find_one({ "email": user['email'] }):
      return jsonify({ "error": "Email address already in use" }), 400
  

    if db.users.insert_one(user):
      return self.start_session(user)

    return jsonify({ "error": "Signup failed" }), 400
  
  def signout(self):
    session.clear()
    return redirect('/')
  
  def login(self):
    db = client.user_login_system
    user = db.users.find_one({
      "email": request.form.get('email')
    })

    if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
      return self.start_session(user)
    
    return jsonify({ "error": "Invalid login credentials" }), 401
  
  def checkAttendance(self):
    # user = db.users.find_one({"email": session['user'].mail})
    # if(False):
      # current_month = now.strftime("%B")
    db = client.user_login_system
    roll = request.form.get('roll')
    user = db.users.find_one({"roll": roll})
    month = request.form["selectMonth"]
    year = user['year']
    dbName = f'{year}-{month}'
    # print(dbName)
    # db = client.user_login_system
    subList = []
    if(year == "TY-IT"):
      subList = ["EIT", "AWP", "NGT", "AI", "LA"]
    if(year == "SY-IT"):
       subList = ["AM", "PP", "DBMS", "DS", "CN"]
    if(year == "FY-IT"):
      subList = ["WP", "DM", "CS", "IP", "DM"]
    session['chartYear'] = year
    attendanceDict = {}
    db = client[dbName]

    for subject in subList:
      sub = db[subject]
      attendance1 = sub.find({"_id" : user['roll']},  {"attendance": 1, "_id": 0})
      # print("Cursor", attendance1)
      subjectAttendance = 0
      for i in attendance1:
        # print(i['attendance'])
        subjectAttendance += int(i["attendance"])
        # print(i['attendance'])
      attendanceDict[subject] = subjectAttendance
      # print(attendanceDict)
    
    idealCollectionName = db["idealCollection"]
    idealColl = idealCollectionName.find()
    for ideal in idealColl:
      subject = ideal['_id']
      attendanceDict[subject] = [attendanceDict[subject], ideal['attendance']]
      session['monthAttendance'] = attendanceDict 
    return jsonify({ f"error": "Username or password is incorrect {attendanceDict}" }), 200

class Admin:
  def start_session(self, admin):
    del admin['password']
    session['admin_logged_in'] = True
    session['admin'] = admin
    return jsonify(admin), 200

  def login(self):
    print(request.form)

      # Create the user object
    admin = {
         "name": request.form.get('name'),
         "password": request.form.get('password')
      }
    username = os.getenv("admin_username")
    passw = os.getenv("admin_password")
    print(type(admin['name']))
    print(type(admin['password']))
    if(admin['name'] == username and admin['password'] == passw): 
      print("Came here")
      return self.start_session(admin)
    return jsonify({ "error": "Username or password is incorrect" }), 400
  
  # def defaultersCheck(self):
  #     selectedYeardefaulters = request.form["selectOption"]
  #     print(selectedYeardefaulters)
  #     if selectedYeardefaulters == "FY-IT":
  #         subjectList = ["EIT", "AWP", "NGT", "AI", "LA"]
  #     if selectedYeardefaulters == "SY-IT":
  #         subjectList = ["AM", "PP", "DBMS", "DS", "CN"]
  #     if selectedYeardefaulters == "TY-IT":
  #         subjectList = ["WP", "DM", "CS", "IP", "DM"]

  #     selectMonthDefaluters = request.form["selectMonth"]
  #     list2 = []
  #     dict_of_ty = TyNameList.TyNameDict
  #     for i, j in dict_of_ty.items():
  #         list2.append(i)
  #     rollNumList = []
  #     percentageList = []
  #     try:
  #         # app.config[
  #         #     "MONGO_URI"
  #         # ] = "mongodb+srv://robinsonjohnsies:Robinson#123@cluster0.nw9jhv3.mongodb.net/?retryWrites=true&w=majority"
  #         # mongo = PyMongo(app)
  #         idealAttendance = 0
  #         for subject in subjectList:
  #             dbName = f"{selectedYeardefaulters}-{selectMonthDefaluters}"
  #             # db = mongo.cx[dbName]
  #             db = client[dbName]
  #             collectionIdeal = db["idealCollection"]
  #             idealAttendanceForSubject = collectionIdeal.find(
  #                 {"_id": subject}, {"_id": 0, "attendance": 1}
  #             )

  #             for i in idealAttendanceForSubject:
  #                 idealAttendance = idealAttendance + i["attendance"]

  #         for rollNum in list2:
  #             total = 0
  #             for subject in subjectList:
  #                 print(subject)
  #                 collection = db[subject]
  #                 subjectAttendance = collection.find(
  #                     {"_id": rollNum}, {"_id": 0, "attendance": 1}
  #                 )
  #                 for att in subjectAttendance:
  #                     total = total + att["attendance"]

  #             final_percentage = (total / idealAttendance) * 100
  #             final_percentage = round(final_percentage, 2)
  #             final_percentage = round(final_percentage, 2)
  #             print(rollNum, final_percentage)
  #             # finalDict[rollNumString] = final_percentage
  #             rollNumList.append(rollNum)
  #             percentageList.append(final_percentage)

  #         session['rollNum'] = rollNumList
  #         session['percentage'] = percentageList
  #         return jsonify({"DONE"}), 20
  #     except Exception as e:
  #       return jsonify({ "error": "Signup failed" }), 400
  #         # return render_template("defaulters.html", err=f"Error!! Call Robinson {e}")
   

  def defaultersCheck(self):
      selectedYeardefaulters = request.form["selectOption"]
      print(selectedYeardefaulters)
      if selectedYeardefaulters == "FY-IT":
          subjectList = ["EIT", "AWP", "NGT", "AI", "LA"]
      if selectedYeardefaulters == "SY-IT":
          subjectList = ["AM", "PP", "DBMS", "DS", "CN"]
      if selectedYeardefaulters == "TY-IT":
          subjectList = ["WP", "DM", "CS", "IP", "DM"]

      selectMonthDefaluters = request.form["selectMonth"]
      list2 = []
      dict_of_ty = TyNameList.TyNameDict
      for i, j in dict_of_ty.items():
          list2.append(i)
      rollNumList = []
      percentageList = []
      try:
          # app.config[
          #     "MONGO_URI"
          # ] = "mongodb+srv://robinsonjohnsies:Robinson#123@cluster0.nw9jhv3.mongodb.net/?retryWrites=true&w=majority"

          dbName = f"{selectedYeardefaulters}-{selectMonthDefaluters}"
          # mongo = PyMongo(app)
          db = client[dbName]
          idealAttendance = 0
          for subject in subjectList:
              # db = [dbName]
              collectionIdeal = db["idealCollection"]
              idealAttendanceForSubject = collectionIdeal.find(
                  {"_id": subject}, {"_id": 0, "attendance": 1}
              )

              for i in idealAttendanceForSubject:
                  idealAttendance = idealAttendance + i["attendance"]

          for rollNum in list2:
              total = 0
              for subject in subjectList:
                  print(subject)
                  collection = db[subject]
                  subjectAttendance = collection.find(
                      {"_id": rollNum}, {"_id": 0, "attendance": 1}
                  )
                  for att in subjectAttendance:
                      total = total + att["attendance"]

              final_percentage = (total / idealAttendance) * 100
              final_percentage = round(final_percentage, 2)
              final_percentage = round(final_percentage, 2)
              print(rollNum, final_percentage)
              # finalDict[rollNumString] = final_percentage
              rollNumList.append(rollNum)
              percentageList.append(final_percentage)

          return jsonify({"DONE"}), 200
      except Exception as e:
          return jsonify({"ERROR"}), 400


  def signout(self):
    session.clear()
    return redirect('/')
  
  
# *Face Recoginition details

class FaceRecDetails:
  def yearCheck(self):
    session["year"] = request.form.get("selectOption")
    session['subjectSelected'] = ''

    if(session['year'] == "Select The Year"):
      return jsonify({ "error": "Select the Year to proceed" }), 401
    if(session['year'] == "TY-IT"):
      # session['subjectSelected'] = self.TYsubjectList
      session['subjects'] = ["EIT", "AWP", "NGT", "AI", "LA"]
      return jsonify("Done"), 200

    if(session['year'] == "SY-IT"):
      # session['subjectSelected'] = self.SYsubjectList
       session['subjects'] = ["AM", "PP", "DBMS", "DS", "CN"]
       return jsonify("Done"), 200

    if(session['year'] == "FY-IT"):
      # session['subjectSelected'] = self.FYsubjectList
      session['subjects'] = ["WP", "DM", "CS", "IP", "DM"]
      return jsonify("Done"), 200

    else:
      redirect("/admin/year/")
      

  def subjectCheck(self):
    session['selectedSubject']  = request.form.get("selectOption")
    session['lectureNum']  = request.form.get("lecnum")

    if( session['selectedSubject'] == "Select The Subject" or  session['lectureNum'] == ""):
      return jsonify({ "error": "Select the Subject" }), 401
    return jsonify("Done"), 200
  

  def process_frames(self):
    dict_of_ty = TyNameList.TyNameDict
    firstEncodingList = TyEncodingFirst.FirstEncodingList
    secondEncodingList = TyEncodingSecond.SecondEncodingList
    firstList = []
    for i, j in firstEncodingList.items():
        firstList.append(j)

    secondList = []
    for i, j in secondEncodingList.items():
        secondList.append(j)
    finalRollName = {}

    best_match_condition = 0.6
    result_roll_list = list(firstEncodingList.keys())
    try:
      response_data = {"message": "Face Not Detected"}
        # image_data = request.files["image_data"]
      image_data = request.files.get("image_data")

      nparr = numpy.frombuffer(image_data.read(), numpy.uint8)
      opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
      img_small = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
      face_current_frame = face_recognition.face_locations(img_small)
      encoding_current_frame = face_recognition.face_encodings(img_small)
      for encodeface, facelocation in zip(encoding_current_frame, face_current_frame):
        matches = face_recognition.compare_faces(firstList, encodeface)
        face_distance = face_recognition.face_distance(firstList, encodeface)
        match_index = numpy.argmin(face_distance)
        print(face_distance[match_index])
        if face_distance[match_index] < best_match_condition:
          if matches[match_index]:
            best_match_roll = result_roll_list[match_index]
            print(best_match_roll)
            finalSecond = secondEncodingList[best_match_roll]
            matches2 = face_recognition.compare_faces(finalSecond, encoding_current_frame)
            face_distance2 = face_recognition.face_distance(
                    finalSecond, encoding_current_frame
              )
            match_index2 = numpy.argmin(face_distance2)
            if face_distance2[match_index2]:
              detectedName = dict_of_ty[best_match_roll]
              finalRollName[best_match_roll] = detectedName
              now = datetime.now()
              current_time = now.strftime("%H:%M:%S")
              print("Current Time =", current_time)
              response_data = {"message": detectedName}
        else:
          continue
      session['DetectedList'] = finalRollName
      return jsonify(response_data), 200
    except Exception as e:
      return jsonify({"error": str(e)}), 500
    
  def move_forward(self):
    try:
        detecDist = session['DetectedList']
        # app.config["MONGO_URI"] = "mongodb+srv://robinsonjohnsies:Robinson#123@cluster0.nw9jhv3.mongodb.net/?retryWrites=true&w=majority"
        # mongo = PyMongo(app)
        now = datetime.now()
        current_month = now.strftime("%B")
        dbName = f"{session['year']}-{current_month}"
        # db = client.cx[dbName]
        
        db = client[dbName]
        # Making perfect attendance Collection
        idealCollection = db["idealCollection"]
        print("collection is working")
        idealAttendance = idealCollection.find(
            {"_id":  session['selectedSubject']}, {"attendance": 1, "_id": 0}
        )
        newLectureNum = int( session['lectureNum'] )
        print("Before for loop")

        for ideal in idealAttendance:
            newLectureNum = ideal["attendance"] + int( session['lectureNum'] )

        idealCollection.update_one(
            {"_id":  session['selectedSubject']},
            {"$set": {"attendance": int(newLectureNum), "currentMonth": current_month}},
            upsert=True,
        )

        myCollection = db[session['selectedSubject']]
        # print(finalList)
        # print(finalName)

        for rollNum, name in zip(detecDist.keys(), detecDist.values()):
            print(rollNum, name)
            newAtt = myCollection.find({"_id": rollNum}, {"attendance": 1, "_id": 0})
            lectureNumTemp = int(session['lectureNum'])
            for i in newAtt:
                print(i)
                lectureNumTemp = i["attendance"] + int( session['lectureNum'])

            myCollection.update_one(
                {"_id": rollNum},
                {
                    "$set": {
                        "name": name,
                        "attendance": int(lectureNumTemp),
                        "currentMonth": current_month,
                    }
                },
                upsert=True,
            )
        # session['DetectedList'].clear()
        return "Done"
        # finalList.clear()
        # finalName.clear()

        # selectedList.clear()
        # return render_template("index.html", forward_message=forward_message)
    except Exception as e:
       print(e)
       return "ERROR"
        # return render_template(
            # "index.html",
            # forward_message=f"DataBase Response : Something Went Wrong! TRY Again! or Call Robinson {e} ", )
    


