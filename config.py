import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard hard hard'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	UPLOADED_CAR_DEST = os.path.join(os.environ['HOME'], 'photos/car')

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

config = {
	'development': DevelopmentConfig,

	'default': DevelopmentConfig,
}

