from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .secjson import secjson
from . import encrypt

def verify(email_name, password):
	user = User.query.filter_by(email=email_name).first()
	if user:
		if check_password_hash(user.password, password):
			return True

		return False

	else:
		return False
    
def verify_AUTH(raw_dictionary):
	
	AUTH = eval(encrypt.decrypter(raw_dictionary))

	if verify(email_name=AUTH['ACCOUNT NAME'], password=AUTH['ACCOUNT PASSWORD']) == True:
		return [True, AUTH['DB NAME'], AUTH['DB PASSWORD'], AUTH['ACCOUNT NAME']]

	else:
		return [False]

def verify_TOKEN(token):
	token = eval(encrypt.decrypter(token))

	try:
		if f"{User.query.filter_by(email=token[0]).first().session_id}" == f"{token[1]}":
			return [True, token[2], token[3]]

		else:
			return [False]
	except:
		return [False]