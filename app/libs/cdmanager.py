import os
from cloudinary.uploader import upload
from cloudinary import config

# class in charge of upload images
class CloudinaryHandler:
    @classmethod
    def LoadImage (cls, base64):
        config( 
            cloud_name = os.environ.get("CLOUD_NAME"), 
            api_key = os.environ.get("CLOUD_API_KEY"), 
            api_secret = os.environ.get("CLOUD_API_SECRET")
            )
        
        result = upload(base64)
        return result["url"]