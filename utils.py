import os
from dotenv import load_dotenv
import boto3
from werkzeug.utils import secure_filename

load_dotenv()

ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("BUCKET_NAME")
PROFILE_PHOTO = "profile_photos"

S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id = ACCESS_KEY,
    aws_secret_access_key = SECRET_KEY ,
    region_name=REGION
    )

# upload photo
# def upload_user_photo(user, file_name):
#     try:
#         S3_CLIENT.upload_file(file_name, BUCKET_NAME, f"{PROFILE_PHOTO}/{user.userName}/{file_name}")

#     except:
#         print("Error uploading file")

def save_photo(photo, path):
    file_name = secure_filename(photo.filename)
    save_path = os.path.join(path, 'photos')
    os.makedirs(save_path, exist_ok=True)
    photo.save(os.path.join(save_path, file_name))

    return file_name