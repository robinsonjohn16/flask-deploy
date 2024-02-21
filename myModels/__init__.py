from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from db import *
import uuid
from dotenv import load_dotenv
from flask import jsonify, request, session
import numpy as numpy
import os
import cv2
import face_recognition
from datetime import datetime
from app import app
from ordered_set import OrderedSet
import smtplib
from myEncoding import TyEncodingFirst
from myEncoding import TyEncodingSecond
from myEncoding import TyNameList
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

load_dotenv()

UPLOAD_FOLDER = "./static/upload"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


class User:
    def start_session(self, user):
        del user["password"]
        session["logged_in"] = True
        session["user"] = user
        return jsonify(user), 200

    def signup(self):
        db = client.user_login_system
        print(request.form)
        print(request.files)

        uploaded_img = request.files["imagefile"]
        if uploaded_img:
            file_extension = uploaded_img.filename.rsplit(".", 1)[1].lower()
            allowed_extensions = {"jpg", "jpeg", "png"}
            if file_extension not in allowed_extensions:
                return (
                    jsonify(
                        {
                            "error": "Invalid file extension. Allowed extensions: jpg, jpeg, png"
                        }
                    ),
                    400,
                )
            filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            print("File uploaded successfully")
            print(uploaded_img)
            cloudinary_res = {}
            if filename != "":
                try:
                    cloudinary.config(
                        cloud_name=os.getenv("CLOUD_NAME"),
                        api_key=os.getenv("API_KEY"),
                        api_secret=os.getenv("API_SECRET"),
                    )
                    cloudinary_res = cloudinary.uploader.upload(
                        os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    )
                    print("url", cloudinary_res["url"])
                except Exception as e:
                    return (
                        jsonify(
                            {
                                "error": f"There is Certain Error in loading the file, try again later {e}",
                            }
                        ),
                        400,
                    )

        if request.form.get("Re-password") != request.form.get("password"):
            return (
                jsonify(
                    {
                        "error": "Re-Enter password and password is not Same",
                    }
                ),
                400,
            )

        print(request.form.get("password"))
        if len(request.form.get("password")) < 8:
            return jsonify({"error": "Password must contain atleast 8 character"}), 405

        if "'" in request.form.get("password") or '"' in request.form.get("password"):
            return (
                jsonify({"error": "Password cannot contain Single or Double Quotes"}),
                405,
            )

        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": request.form.get("password"),
            "roll": request.form.get("roll"),
            "year": request.form["selectOption"],
            # "year": request.form.get('year'),
            "parentMail": request.form.get("pmail"),
            "profile": cloudinary_res["url"],
        }

        # Encrypt the password
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        # Check for existing email address
        if db.users.find_one({"email": user["email"]}):
            return jsonify({"error": "Email address already in use"}), 400

        # Check for existing Roll Number
        if db.users.find_one({"roll": user["roll"]}):
            return (
                jsonify(
                    {
                        "error": "Roll Number already in use, Login to your Account Instead"
                    }
                ),
                400,
            )

        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect("/")

    def login(self):
        db = client.user_login_system
        user = db.users.find_one({"email": request.form.get("email")})

        if user and pbkdf2_sha256.verify(
            request.form.get("password"), user["password"]
        ):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def checkAttendance(self):
        # user = db.users.find_one({"email": session['user'].mail})
        # if(False):
        # current_month = now.strftime("%B")
        db = client.user_login_system
        roll = request.form.get("roll")
        user = db.users.find_one({"roll": roll})
        month = request.form["selectMonth"]
        year = user["year"]
        dbName = f"{year}-{month}"
        # print(dbName)
        # db = client.user_login_system
        subList = []
        if year == "TY-IT":
            subList = ["EIT", "AWP", "NGT", "AI", "LA"]
        if year == "SY-IT":
            subList = ["AM", "PP", "DBMS", "DS", "CN"]
        if year == "FY-IT":
            subList = ["WP", "DM", "CS", "IP", "DM"]
        session["chartYear"] = year
        attendanceDict = {}
        db = client[dbName]

        for subject in subList:
            sub = db[subject]
            attendance1 = sub.find({"_id": user["roll"]}, {"attendance": 1, "_id": 0})
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
            subject = ideal["_id"]
            attendanceDict[subject] = [attendanceDict[subject], ideal["attendance"]]
            session["monthAttendance"] = attendanceDict
        return (
            jsonify({f"error": "Username or password is incorrect {attendanceDict}"}),
            200,
        )

    def edit(self):
        return


class Admin:

    subject = "Important: Your Child's Monthly Attendance Report"

    def emailContent(self, nameParent, studentName, finalAttendance, teacherName):
        return f"""
Dear {nameParent},
I hope this email finds you well. We would like to bring to your attention the attendance report for your child, {studentName}, for the month of this Month. Unfortunately, the final attendance percentage falls below the required criteria of 75%.

Monthly Attendance Summary:
Final Attendance: {finalAttendance}%

We understand that circumstances may vary, and there could be reasons for absenteeism. However, maintaining regular attendance is crucial for academic success. Consistent attendance ensures that your child remains engaged in the learning process and benefits fully from the educational experience.

If there are any specific challenges or concerns affecting your child's attendance, please feel free to reach out to us. We are here to support and work together to address any issues that may be impacting attendance.

We encourage open communication between parents, students, and teachers to ensure the best possible educational outcomes. Your involvement and support are integral to the success of your child's academic journey.

Thank you for your attention to this matter, and we look forward to working together to maintain a positive and supportive learning environment.

Best Regards,

{teacherName}
SIES College of Arts, Science and Commerce. Sion(West)
"""

    def start_session(self, admin):
        del admin["password"]
        session["admin_logged_in"] = True
        session["admin"] = admin
        return jsonify(admin), 200

    def login(self):
        print(request.form)

        # Create the user object
        admin = {
            "name": request.form.get("name"),
            "password": request.form.get("password"),
        }
        username = os.getenv("ADMIN_USERNAME")
        passw = os.getenv("ADMIN_PASSWORD")
        print(type(admin["name"]))
        print(type(admin["password"]))
        if admin["name"] == username and admin["password"] == passw:
            print("Came here")
            return self.start_session(admin)
        return jsonify({"error": "Username or password is incorrect"}), 400

    def defaultersCheck(self):
        # if not request.session.get("updatedDefaulters", False):
        #     session.pop("updatedDefaulters")

        selectedYeardefaulters = request.form["selectOption"]
        print(selectedYeardefaulters)
        if selectedYeardefaulters == "FY-IT":
            subjectList = ["WP", "DM", "CS", "IP", "DM"]
        if selectedYeardefaulters == "SY-IT":
            subjectList = ["AM", "PP", "DBMS", "DS", "CN"]
        if selectedYeardefaulters == "TY-IT":
            subjectList = ["EIT", "AWP", "NGT", "AI", "LA"]

        selectMonthDefaluters = request.form["selectMonth"]
        list2 = []
        session["monthDefaulters"] = selectMonthDefaluters
        dict_of_ty = TyNameList.TyNameDict
        for i, j in dict_of_ty.items():
            list2.append(i)
        # print(list2)
        rollNumList = []
        final_def = {}
        percentageList = []
        try:
            idealAttendance = 0
            for subject in subjectList:
                # db = [dbName]
                dbName = f"{selectedYeardefaulters}-{selectMonthDefaluters}"
                # mongo = PyMongo(app)
                db = client[dbName]
                collectionIdeal = db["idealCollection"]
                idealAttendanceForSubject = collectionIdeal.find(
                    {"_id": subject}, {"_id": 0, "attendance": 1}
                )
                # print(idealAttendanceForSubject)
                for i in idealAttendanceForSubject:
                    idealAttendance = idealAttendance + i["attendance"]
                    # print("i", i["attendance"])
            # print("Ideal Total", idealAttendance)

            for rollNum in list2:
                total = 0
                # print(rollNum)
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
                # print(rollNum, final_percentage)
                rollNumList.append(rollNum)
                # session("rollNum")
                # session("final_percentage")
                percentageList.append(final_percentage)

                final_def[rollNum] = final_percentage
            session["defaulters"] = final_def
            return jsonify({"message": "Success"}), 200
        except Exception as e:
            return jsonify({"error": f"Error While Calculating {e}"}), 400

    def signout(self):
        session.clear()
        return redirect("/")

    def finalList(self):
        tempDict = {}
        data = float(request.args.get("percentageSelected"))

        if not data:
            return jsonify({"error": "Data didn't Reached Backend"}), 400
        for i, j in dict(session["defaulters"]).items():
            if j > data:
                tempDict[i] = j
                print(j)
            else:
                continue
        session["updatedDefaulters"] = tempDict
        return jsonify({"message": session["updatedDefaulters"]}), 200

    def sendMail(self):
        data = str(request.args.get("teacherName"))
        if not session["updatedDefaulters"]:
            return jsonify({"error": "No defaulters Data"}), 400
        # parentMailList = []
        for roll in session["updatedDefaulters"].keys():
            print(roll)
            db = client.user_login_system
            dbUser = db.users.find_one({"roll": roll})
            if dbUser is None or dbUser["parentMail"] is None:
                return jsonify(
                    {
                        "error": f"Roll Number : {roll} Haven't Provided their Parent Mail id"
                    }
                )
            # if not dbUser["parentMail"]:
            # continue
            # print("i", dbUser["parentMail"])
            # parentMailList.append(dbUser["parentMail"])
            # Sending the mail
            try:
                senderEmailId = os.getenv("SMTP_EMAIL_ID")
                appPassword = os.getenv("SMTP_EMAIL_PASSWORD")
                mailContent = f"""Subject: {self.subject} \n\n {self.emailContent(dbUser["parentMail"], dbUser['name'], session["updatedDefaulters"][roll], data)}"""
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(senderEmailId, appPassword)
                server.sendmail(senderEmailId, dbUser["parentMail"], mailContent)
            except Exception as e:
                session.pop("updatedDefaulters")
                return jsonify({"error": "Error While sending the mail"}), 401
        session.pop("updatedDefaulters")
        return jsonify({"message": "Success"}), 200

        # for email in parentMailList:

    def pullForm(self):
        return (
            jsonify(
                {"subject": self.subject, "content": self.emailContent("", "", "", "")}
            ),
            200,
        )


# *Face Recoginition details
class FaceRecDetails:
    def end_session(self, session_name):
        session.pop(session_name)
        return 0

    def yearCheck(self):
        session["year"] = request.form.get("selectOption")
        session["subjectSelected"] = ""

        if session["year"] == "Select The Year":
            return jsonify({"error": "Select the Year to proceed"}), 401
        if session["year"] == "TY-IT":
            session["subjects"] = ["EIT", "AWP", "NGT", "AI", "LA"]
            return jsonify("Done"), 200

        if session["year"] == "SY-IT":
            session["subjects"] = ["AM", "PP", "DBMS", "DS", "CN"]
            return jsonify("Done"), 200

        if session["year"] == "FY-IT":
            session["subjects"] = ["WP", "DM", "CS", "IP", "DM"]
            return jsonify("Done"), 200
        else:
            redirect("/admin/year/")

    def subjectCheck(self):
        session["selectedSubject"] = request.form.get("selectOption")
        session["lectureNum"] = request.form.get("lecnum")

        if (
            session["selectedSubject"] == "Select The Subject"
            or session["lectureNum"] == ""
        ):
            return jsonify({"error": "Select the Subject"}), 401
        session["DetectedList"] = {}
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
        temp = 0
        best_match_condition = 0.53
        result_roll_list = list(firstEncodingList.keys())
        try:
            response_data = {"message": "Face Not Detected"}
            image_data = request.files.get("image_data")
            nparr = numpy.frombuffer(image_data.read(), numpy.uint8)
            opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            img_small = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)
            face_current_frame = face_recognition.face_locations(img_small)
            encoding_current_frame = face_recognition.face_encodings(img_small)
            for encodeface, facelocation in zip(
                encoding_current_frame, face_current_frame
            ):
                matches = face_recognition.compare_faces(firstList, encodeface)
                face_distance = face_recognition.face_distance(firstList, encodeface)
                match_index = numpy.argmin(face_distance)
                print(face_distance[match_index])
                if face_distance[match_index] < best_match_condition:
                    if matches[match_index]:
                        best_match_roll = result_roll_list[match_index]
                        print(best_match_roll)
                        finalSecond = secondEncodingList[best_match_roll]
                        matches2 = face_recognition.compare_faces(
                            finalSecond, encoding_current_frame
                        )
                        face_distance2 = face_recognition.face_distance(
                            finalSecond, encoding_current_frame
                        )
                        match_index2 = numpy.argmin(face_distance2)
                        if face_distance2[match_index2]:
                            detectedName = dict_of_ty[best_match_roll]
                            finalRollName[best_match_roll] = detectedName
                            now = datetime.now()
                            current_time = now.strftime("%H:%M:%S")
                            temp = session["DetectedList"]
                            # print("TEMP ", temp)
                            print(temp, finalRollName)
                            temp.update(finalRollName)
                            session["DetectedList"] = temp
                            # print("Session", session["DetectedList"])
                            print("Current Time =", current_time)
                            response_data = {"message": detectedName}
                else:
                    continue
            return jsonify(response_data), 200
        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 501

    def move_forward(self):
        name = request.form.get("name")
        password = request.form.get("password")
        if not name or not password:
            return jsonify({"error": "Name and Password is required"}), 400

        if name == os.getenv("SUBMIT_ID") and password == os.getenv("SUBMIT_PASSWORD"):
            return jsonify({"error": "Credentials are not correct"}), 401
        try:
            detecDist = session["DetectedList"]
            now = datetime.now()
            current_month = now.strftime("%B")
            dbName = f"{session['year']}-{current_month}"

            db = client[dbName]

            # * Making perfect attendance Collection
            idealCollection = db["idealCollection"]
            print("collection is working")
            idealAttendance = idealCollection.find(
                {"_id": session["selectedSubject"]}, {"attendance": 1, "_id": 0}
            )
            newLectureNum = int(session["lectureNum"])
            print("Before for loop")

            for ideal in idealAttendance:
                newLectureNum = ideal["attendance"] + int(session["lectureNum"])

            idealCollection.update_one(
                {"_id": session["selectedSubject"]},
                {
                    "$set": {
                        "attendance": int(newLectureNum),
                        "currentMonth": current_month,
                    }
                },
                upsert=True,
            )
            myCollection = db[session["selectedSubject"]]

            for rollNum, name in zip(detecDist.keys(), detecDist.values()):
                print(rollNum, name)
                newAtt = myCollection.find(
                    {"_id": rollNum}, {"attendance": 1, "_id": 0}
                )
                lectureNumTemp = int(session["lectureNum"])
                for i in newAtt:
                    print(i)
                    lectureNumTemp = i["attendance"] + int(session["lectureNum"])

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
            self.end_session("DetectedList")
            return jsonify({"message": "Successfully Submitted to the database"}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Database Submit Issue, Try Again later"}), 200
