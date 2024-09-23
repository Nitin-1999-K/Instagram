from typing import Any, Dict, List
from pydantic_settings import BaseSettings
from pathlib import Path
import os

current_directory = os.getcwd() # current working directory
parent_directory = os.path.abspath(os.path.join(current_directory, '.')) # Absolute path of parent directory
post_pic_dir = os.path.join(parent_directory, "post_pics") # Image directory (Assuming)
profile_pic_dir = os.path.join(parent_directory, "profile_pics")

if not os.path.exists(post_pic_dir): # Creating a new directory if image directory does not exist
    os.makedirs(post_pic_dir)
    
if not os.path.exists(profile_pic_dir): # Creating a new directory if image directory does not exist
    os.makedirs(profile_pic_dir)
    
class Settings(BaseSettings):
    PROJECT_NAME: str = "Social Media"
    PROJECT_VERSION: str = "1.0.0"
    SECRET_KEY: str = "72b6dc51f41263d45c111670951419ef171a16abaccb201189144ea9d5ea13a6"
    EXPIRE_MINUTES: int = 60
    DATA_BASE: str = "mysql+pymysql://root:Nitin%401999@localhost:3306/Instagram"
    post_pic_dir: str | None = None
    profile_pic_dir: str | None = None

    class Config:
        case_sensitive = True


settings = Settings()
settings.post_pic_dir = post_pic_dir
settings.profile_pic_dir = profile_pic_dir





