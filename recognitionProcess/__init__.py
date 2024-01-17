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


class processFrame:
   def process_frames(self):
      dict_of_ty = TyNameList.TyNameDict
      firstEncodingList = TyEncodingFirst.FirstEncodingList
      secondEncodingList = TyEncodingSecond.SecondEncodingList
      finalList = OrderedSet()
      finalName = OrderedSet()
      firstList = []
      for i, j in firstEncodingList.items():
         firstList.append(j)

      secondList = []
      for i, j in secondEncodingList.items():
         secondList.append(j)


      best_match_condition = 0.48
      # best_match_condition2 = 0.48
      result_roll_list = list(firstEncodingList.keys())
      try:
         response_data = {"message": "Face Not Detected"}
         # image_data = request.files["image_data"]
         image_data = request.files.get("image_data")

         nparr = numpy.frombuffer(image_data.read(), numpy.uint8)
         opencv_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

         cv2.imwrite("received_image_opencv.jpg", opencv_image)

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
                     matches2 = face_recognition.compare_faces(
                           finalSecond, encoding_current_frame
                     )
                     face_distance2 = face_recognition.face_distance(
                           finalSecond, encoding_current_frame
                     )
                     match_index2 = numpy.argmin(face_distance2)
                     if face_distance2[match_index2]:
                           finalList.add(best_match_roll)
                           detectedName = dict_of_ty[best_match_roll]
                           finalName.add(detectedName)
                           now = datetime.now()
                           current_time = now.strftime("%H:%M:%S")
                           print("Current Time =", current_time)
                           response_data = {"message": detectedName}
               else:
                  continue
         return jsonify(response_data), 200
      except Exception as e:
         return jsonify({"error": str(e)}), 500
      

   