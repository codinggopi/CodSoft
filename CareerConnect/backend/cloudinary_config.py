
import cloudinary
import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "").strip('\"\''),
    api_key=os.getenv("CLOUDINARY_API_KEY", "").strip('\"\''),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "").strip('\"\''),
)
