from fastapi import UploadFile
from sqlalchemy.orm import Session
from models import Image
from core.config import settings
import utils
import uuid

post_pic_dir = settings.post_pic_dir.replace("\\","/")
print(post_pic_dir)

def uploadImages(db: Session, 
                  files: list[UploadFile], 
                  post_id: int | None = None, 
                  profile_id: int | None = None):

    for file in files:
        filename = uuid.uuid4()
        image = Image(image_dir =  f"{post_pic_dir}/{filename}",
                    profile_id = profile_id,
                    post_id = post_id)
        db.add(image)
        db.commit()
        db.refresh(image)

        utils.writeFile(file = file, filename = filename, dir = post_pic_dir)
        


def deleteImages(
    db: Session,
    post_id: int,
    image_ids: list[int] | None = None
):
    db.query(Image).filter(Image.post_id == post_id, Image.id.in_(image_ids)).update({'status_code': -1})
    db.commit()


    