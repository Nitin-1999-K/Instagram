from .user import User
from .profile import Profile
from .post import Post
from .post_like import PostLike
from .otp_log import OtpLog
from .image import Image
from .comment import Comment
from .chat import Chat











# from sqlalchemy.orm import sessionmaker
# db = sessionmaker(bind=engine)()


# users = [
#     {'username': 'user1', 'email': 'user1@example.com', 'mobile_number': '111-222-3333', 'hashed_password': 'hashed_password1', 
#      'status': 'Active', 'account_type': 'Public', 'otp_key': 'otp_key_1234'},
#     {'username': 'user2', 'email': 'user2@example.com', 'mobile_number': '222-333-4444', 'hashed_password': 'hashed_password2', 
#      'status': 'Inactive', 'account_type': 'Friends', 'otp_key': 'otp_key_5678'},
#     {'username': 'user3', 'email': 'user3@example.com', 'mobile_number': '333-444-5555', 'hashed_password': 'hashed_password3', 
#      'status': 'Active', 'account_type': 'Public', 'otp_key': 'otp_key_9101'},
#     {'username': 'user4', 'email': 'user4@example.com', 'mobile_number': '444-555-6666', 'hashed_password': 'hashed_password4', 
#      'status': 'Active', 'account_type': 'Public', 'otp_key': 'otp_key_1121'},
#     {'username': 'user5', 'email': 'user5@example.com', 'mobile_number': '555-666-7777', 'hashed_password': 'hashed_password5', 
#      'status': 'Inactive', 'account_type': 'Friends', 'otp_key': 'otp_key_3141'}
# ]


# profiles = [
#     {'first_name': 'Alice', 'last_name': 'Smith', 'about': 'Alice is a software developer.', 'user_id': 1},
#     {'first_name': 'Bob', 'last_name': 'Johnson', 'about': 'Bob loves photography.', 'user_id': 2},
#     {'first_name': 'Charlie', 'last_name': 'Williams', 'about': 'Charlie enjoys hiking.', 'user_id': 3},
#     {'first_name': 'Diana', 'last_name': 'Brown', 'about': 'Diana is a graphic designer.', 'user_id': 4},
#     {'first_name': 'Eve', 'last_name': 'Davis', 'about': 'Eve is a digital marketer.', 'user_id': 5}
# ]

# posts = [
#     {'post_type': 'Public', 'text': 'This is a public post by user1.', 'user_id': 1},
#     {'post_type': 'Friends', 'text': 'This is a friends-only post by user2.', 'user_id': 2},
#     {'post_type': 'Private', 'text': 'This is a private post by user3.', 'user_id': 3},
#     {'post_type': 'Public', 'text': 'This is another public post by user4.', 'user_id': 4},
#     {'post_type': 'Public', 'text': 'Yet another public post by user5.', 'user_id': 5}
# ]

# images = [
#     {'file_path': 'path/to/image1.jpg', 'image_type': 'post', 'post_id': 1},
#     {'file_path': 'path/to/image2.jpg', 'image_type': 'post', 'post_id': 2},
#     {'file_path': 'path/to/image3.jpg', 'image_type': 'profile', 'profile_id': 1},
#     {'file_path': 'path/to/image4.jpg', 'image_type': 'profile', 'profile_id': 1},
#     {'file_path': 'path/to/image5.jpg', 'image_type': 'post', 'post_id': 3}
# ]



# for user in users:
#     db.add(User(**user))
# db.commit()

# for post in posts:
#     db.add(Post(**post))
# db.commit()

# for profile in profiles:
#     db.add(Profile(**profile))
# db.commit()

# for image in images:
#     db.add(Image(**image))
# db.commit()




