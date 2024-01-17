import cloudinary
import cloudinary.uploader
# import cloudinary
          
cloudinary.config( 
  cloud_name = "drvovffv3", 
  api_key = "215414443671738", 
  api_secret = "Lb02uY521z21SbnnAB1vddodFcA" 
)
def cloudinry_custom_upload():
   return cloudinary.uploader.upload("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYbRUZydXzUfldYrF9KU9_i-zR-r4DuISWIQ&usqp=CAU")
   
print(cloudinry_custom_upload())
