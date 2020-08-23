import os

# # sql alchemy
# SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI','postgresql://postgres:Q.654321o@localhost:5432/agnitu')

# jwt
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')