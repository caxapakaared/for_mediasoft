LOGIN = 'admin'
PASSWORD = ''
HOST = 'localhost:5432'
DATABASE_NAME ='shops'
db_uri = 'postgresql://{}:{}@{}/{}'.format(LOGIN, PASSWORD, HOST, DATABASE_NAME)

class Config(object):
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = db_uri
	JSON_AS_ASCII = False