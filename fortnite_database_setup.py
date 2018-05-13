from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))

#Create User model for database
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	username = Column(String(32), index = True)
	email = Column(String)
	picture = Column(String)
	password_hash = Column(String(64))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password_hash)

	def generate_auth_token(self, expiration=600):
		s = Serializer(secret_key, expires_in = expiration)
		return s.dumps({'id': self.id })

#Static method to verity authentication token
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(secret_key)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None
		except BadSignature:
			return None
		user_id = data['id']
		return user_id

#Create Weapon model for database
class Weapon(Base):
	__tablename__ = 'weapon'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	user_id = Column(Integer,ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
		'name' : self.name,
		'id' : self.id
		}

#Create Weapon detail model for database
class WeaponDetail(Base):
	__tablename__ = 'weapon_detail'
	id = Column(Integer, primary_key = True)
	name = Column(String(250), nullable = False)
	description = Column(String, nullable = False)
	color = Column(String(250))
	damage = Column(Integer)
	weapon_id = Column(Integer,ForeignKey('weapon.id'))
	weapon = relationship(Weapon)
	user_id = Column(Integer,ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return {
		'id' : self.id,
		'name' : self.name,
		'description' : self.description,
		'color' : self.color,
		'damange' : self.damage
		}


engine = create_engine('sqlite:///fortniteweapondatabase.db')


Base.metadata.create_all(engine)


