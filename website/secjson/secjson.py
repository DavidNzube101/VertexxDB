from werkzeug.security import generate_password_hash, check_password_hash
import os
import random
import json
from .. import encrypt

base_dir = "_idbs/dbs/"

def convert(db_name, db_password, table="TABLE1", db_schema="", to="SecJSON"):
	
	if to == "SecJSON":
		db_password = generate_password_hash(db_password)

		temp_db = {}
		temp_db[f'0'] = {}
		temp_db[f'0'][f'id'] = '0'

		for col in db_schema:
			temp_db[f'0'][f'{col}'] = 'NULL'

		temp_db = str(temp_db)

		file_content = f"""
{{
"NAME": "{db_name}",
"PASSWORD": "{db_password}",
"CONTENT": {{
		"{table}": [{temp_db}, {db_schema}]
	}}
}}
"""

		with open(f"{base_dir}{db_name}.secjson", "w") as secjsonfile:
			secjsonfile.write(str(encrypt.encrypter(file_content)))

		try:
			os.remove(f"{base_dir}{db_name}.json")
		except:
			pass

	else:

		with open(f"{base_dir}{db_name}.secjson", "r") as __:
			decrypted_dict = encrypt.decrypter(__.read())
		
		cnt = eval(decrypted_dict)

		_dbs = os.listdir(base_dir)
		databases = []
		for _d in _dbs:
			databases.append(_d.replace(".secjson", ""))


		if db_name in databases:
			if check_password_hash(cnt['PASSWORD'], db_password):
				for i, j in cnt['CONTENT'].items():
					if table == i:
						db_requested = cnt['CONTENT'][f'{table}'][0]
						db_requested_copy = db_requested

						for __k, __v in db_requested.items():
							if "FILE64--" in __v:
								with open(f"_idbs/FILEENCODED/{__v}.fileencoded") as _file:
									file64 = _file.read()

								db_requested_copy[__k][__v] = file64

						return db_requested_copy

						break
				
				return "[ERR]: TABLE NOT FOUND"

			else:
				return "[ERR]: PASSWORD INCORRECT"

		else:
			return "[ERR]: DB NOT FOUND"
		
	
def withopen(name, table_, password, new=[False, []]):
	if new[0] == True:
		with open(f"{base_dir}{name}.secjson", "r") as db_file:
			db_content = db_file.read()

		db_content = eval(encrypt.decrypter(db_content))
		if check_password_hash(db_content['PASSWORD'], password):
			valid_tables = []
			for i, j in db_content['CONTENT'].items():
				valid_tables.append(i)

			if table_ in valid_tables:
				return f"[ERR]: CAN'T CREATE TABLE. `{table_}` ALREADY EXISTS"

			else:
				template_data = {}

				template_data[f'0'] = {}
				template_data[f'0'][f'id'] = '0'

				for col in new[1]:
					template_data[f'0'][f'{col}'] = 'NULL'

				db_content['CONTENT'][f'{table_}'] = [template_data, new[1]]

				with open(f"{base_dir}{name}.secjson", "w") as db_file:
					db_file.write(encrypt.encrypter(str(db_content)))

				return f"CREATED TABLE: {table_}"
			
		else:
			return "[ERR]: CAN'T ACCESS SECJSON. INCORRECT PASSWORD"

	else:
		try:
			return convert(db_name=name, table=table_, db_password=password, to="JSON")
		except:
			return "[ERR]: DB NOT FOUND"
	

def get_schema(db_name, table, db_password):
	with open(f"{base_dir}{db_name}.secjson", "r") as __:
		decrypted_dict = encrypt.decrypter(__.read())
	
	cnt = eval(decrypted_dict)

	_dbs = os.listdir(base_dir)
	databases = []
	for _d in _dbs:
		databases.append(_d.replace(".secjson", ""))


	if db_name in databases:
		if check_password_hash(cnt['PASSWORD'], db_password):
			for i, j in cnt['CONTENT'].items():
				if table == i:
					return cnt['CONTENT'][f'{table}'][1]
					break
			
			return "[ERR]: TABLE NOT FOUND"

		else:
			return "[ERR]: PASSWORD INCORRECT"

	else:
		return "[ERR]: DB NOT FOUND"

def commit_db(db_name, table, db_password, new_db):
	with open(f"{base_dir}{db_name}.secjson", "r") as __:
		decrypted_dict = encrypt.decrypter(__.read())
	
	cnt = eval(decrypted_dict)

	_dbs = os.listdir(base_dir)
	databases = []
	for _d in _dbs:
		databases.append(_d.replace(".secjson", ""))


	if db_name in databases:
		if check_password_hash(cnt['PASSWORD'], db_password):
			for i, j in cnt['CONTENT'].items():
				if table == i:
					cnt['CONTENT'][f'{table}'][0] = new_db
					with open(f"{base_dir}{db_name}.secjson", "w") as _to_write:
						_to_write.write(encrypt.encrypter(str(cnt)))
					return "[SUCCESS]: UPDATED"
					break
			
			return "[ERR]: TABLE NOT FOUND"

		else:
			return "[ERR]: PASSWORD INCORRECT"

	else:
		return "[ERR]: DB NOT FOUND"

class SecJSON:
	"""docstring for SecJSON"""
	def __init__(self, init=True):
		self.init = init
		
	def get_db_raw(self, auth):

		with open(f"{base_dir}{auth[0]}.secjson", "r") as _raw:
			_ = _raw.read()

		return _

	def genarate_db(self, db_name, db_password, table_name, db_info):
		db_info_decrypted = eval((db_info))

		with open(f"{base_dir}{db_name}.json", "w") as _d:
			_d.write('{}')

		with open(f"{base_dir}{db_name}.json", "r") as _:
			db_to_create = json.load(_)

		convert(db_name=db_name, db_password=db_password, db_schema=db_info_decrypted, table=table_name)

		return None

	def create_table(self, auth, table_name, table_schema):
		table_name = table_name.capitalize()
		table_schema_decrypted = eval((table_schema))

		db_to_add_table = withopen(auth[0], table_name, auth[1], new=[True, table_schema_decrypted])

		return f"{db_to_add_table}"

	def get_all(self, auth, table):
		db_to_get = withopen(name=auth[0], table_=table, password=auth[1])

		return db_to_get

	def add_entry(self, auth, table, entry):
		entry = eval((entry))

		db_to_add, db_schema = withopen(auth[0], table, auth[1]), get_schema(auth[0], table, auth[1])

		for key, value in db_to_add.items():
			key_ = int(key)

		db_to_add[f'{key_ + 1}'] = {}
		db_to_add[f'{key_ + 1}']['id'] = f'{key_ + 1}'

		for col in db_schema:
			db_to_add[f'{key_ + 1}'][f'{col}'] = 'NULL'

		for k, v in entry.items():
			db_to_add[f'{key_ + 1}'][f'{k}'] = f"{v}"

		commit_db(auth[0], table, auth[1], db_to_add)

		return None

	def find_all(self, auth, table, find_pair):
		find_pair_decrypted = eval((find_pair))
		db_to_search = withopen(auth[0], table, auth[1])

		for h, i in find_pair_decrypted.items():
		    column = h
		    value = i

		_ = []
		for k, v in db_to_search.items():
			for vs in v:
				if vs == column:
					if (db_to_search[f"{k}"][f"{vs}"]) == str(value):
						_.append(db_to_search[f'{k}'])

		if len(_) == 0:
			return []
		else:
			return _

	def find_one(self, auth, table, find_pair):
		find_pair_decrypted = eval((find_pair))
		db_to_search = withopen(auth[0], table, auth[1])

		for search_key, search_pair in find_pair_decrypted.items():
			search_item = f"{search_key} -> {search_pair}"

		def find():
			for key, value in db_to_search.items():
				for keys, values in value.items():
					search_model = f"{keys} -> {values}"
					if search_item == search_model:
						return key#[key, keys]

		if find() == None:
			return None
		else:
			return find()

	def update_entry(self, auth, table, column_to_update, entry):
		entry_decrypted = eval((entry))
		
		db_to_update = withopen(auth[0], table, auth[1])

		for k, v in db_to_update.items():
			for kn, vn in entry_decrypted.items():
				db_to_update[f'{column_to_update}'][kn] = vn

		commit_db(auth[0], table, auth[1], db_to_update)

		return None

	def update_entry_dnd(self, auth, table, column_to_update, entry):
		entry_decrypted = eval(entry)
		
		db_to_update = withopen(auth[0], table, auth[1])

		for k, v in db_to_update.items():
			for kn, vn in entry_decrypted.items():
				rad_n = f"{random.choice(range(100))}{random.choice(range(100))}{random.choice(range(100))}{random.choice(range(100))}" 
				db_to_update[f'{column_to_update}'][kn] = f"FILE64--{rad_n}"

				with open(f"_idbs/FILEENCODED/FILE64--{rad_n}.fileencoded", 'w') as _fe:
					_fe.write(str(vn))

			break

		commit_db(auth[0], table, auth[1], db_to_update)

		return None

	def delete_entry(self, auth, table, column_to_delete):
		db_to_delete = withopen(auth[0], table, auth[1])

		for k, v in db_to_delete.items():
			if k == str(column_to_delete):
				del db_to_delete[f'{k}']
				break

		commit_db(auth[0], table, auth[1], db_to_delete)

		return None