
# views.py

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import random
from flask_login import login_required, current_user
from sqlalchemy.sql import func  # Import the 'func' module
from .models import User
from . import db
from .secjson import secjson
from . import vef_source
from . import encrypt

import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)
sjson = secjson.SecJSON()

@views.route('/')
def index():
  return render_template("login.html")

@views.route('/home')
def home():
  return render_template("home.html")

# http://127.0.0.1:2781/handler/create-db/&004;&001;&022;&009;&004;&st;&022;&005;&018;&020;&005;&024;&004;&002;&at;&012;&005;&004;&009;&020;&019;&016;&001;&003;&005;&st;&003;&015;&013;/&18;&008;&009;&016;&013;&001;&014;&&4;&&2;&ast;/&012;&005;&004;&009;&020;&und;&021;&019;&005;&018;&019;&und;&004;&001;&020;&001;&002;&001;&019;&005;/&&2;&&3;&024;&004;&005;&hyph;&024;&bc;&ast;&bo;&020;&018;&009;&013;&&1;&&2;&hs;&&2;/&20;&18;&04;&17;/&so;&sq;&014;&001;&013;&005;&sq;&cm;&ws;&sq;&021;&019;&005;&018;&014;&001;&013;&005;&sq;&cm;&ws;&sq;&005;&013;&001;&009;&012;&sq;&cm;&ws;&sq;&001;&016;&016;&und;&020;&008;&005;&013;&005;&sq;&cm;&ws;&sq;&001;&016;&016;&und;&009;&004;&sq;&sc;


# VXDINFO = &co;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&004;&001;&022;&009;&004;&st;&022;&005;&018;&020;&005;&024;&004;&002;&at;&012;&005;&004;&009;&020;&019;&016;&001;&003;&005;&st;&003;&015;&013;&sq;&cm;&ws;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&18;&008;&009;&016;&013;&001;&014;&&4;&&2;&ast;&sq;&cm;&ws;&sq;&03;&01;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&012;&005;&004;&009;&020;&und;&021;&019;&005;&018;&019;&und;&004;&001;&020;&001;&002;&001;&019;&005;&sq;&cm;&ws;&sq;&03;&01;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&&2;&&3;&024;&004;&005;&hyph;&024;&bc;&ast;&bo;&020;&018;&009;&013;&&1;&&2;&hs;&&2;&sq;&cc;

# http://127.0.0.1:2781/handler/get-all/&co;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&004;&001;&022;&009;&004;&st;&022;&005;&018;&020;&005;&024;&004;&002;&at;&012;&005;&004;&009;&020;&019;&016;&001;&003;&005;&st;&003;&015;&013;&sq;&cm;&ws;&sq;&00;&02;&02;&14;&20;&13;&19;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&18;&008;&009;&016;&013;&001;&014;&&4;&&2;&ast;&sq;&cm;&ws;&sq;&03;&01;&ws;&13;&00;&12;&04;&sq;&fc;&ws;&sq;&012;&005;&004;&009;&020;&und;&021;&019;&005;&018;&019;&und;&004;&001;&020;&001;&002;&001;&019;&005;&sq;&cm;&ws;&sq;&03;&01;&ws;&15;&00;&18;&18;&22;&14;&17;&03;&sq;&fc;&ws;&sq;&&2;&&3;&024;&004;&005;&hyph;&024;&bc;&ast;&bo;&020;&018;&009;&013;&&1;&&2;&hs;&&2;&sq;&cc;/&20;&18;&04;&17;

@views.route("/handler/exchtk/<string:AUTHENTICATION>") # EXCHANGE TOKENS
def exchangeTokens(AUTHENTICATION):
  is_verified = vef_source.verify_AUTH(AUTHENTICATION)

  if is_verified[0] is True:
    sid = User.query.filter_by(email=is_verified[3]).first().session_id
    return f"['{is_verified[3]}', '{sid}']"
  else:
    return "Invalid Request"

@views.route("/handler/get-db-raw/<string:AUTHENTICATION>")
def get_db_raw(AUTHENTICATION):
  is_verified = vef_source.verify_AUTH(AUTHENTICATION)

  if is_verified[0] is True:
    query = sjson.get_db_raw([is_verified[1], is_verified[2]])

    return str(query)
  else:
    return "Invalid Request"

@views.route("/handler/create-db/<string:ACCOUNT_NAME>/<string:ACCOUNT_PASSCODE>/<string:DB_NAME>/<string:DB_PASSCODE>/<string:DEF_TABLE>/<string:DB_INFO>")#/<string:DB_NAME>/<string:DB_PASSCODE>
def create_db(ACCOUNT_NAME, ACCOUNT_PASSCODE, DB_NAME, DB_PASSCODE, DEF_TABLE, DB_INFO):
  is_verified = vef_source.verify(encrypt.decrypter(ACCOUNT_NAME), encrypt.decrypter(ACCOUNT_PASSCODE))

  if is_verified is True:
    sjson.genarate_db(encrypt.decrypter(DB_NAME), encrypt.decrypter(DB_PASSCODE), encrypt.decrypter(DEF_TABLE), DB_INFO)
    u = User.query.filter_by(email=encrypt.decrypter(ACCOUNT_NAME)).first()
    
    try:
      current_db = eval(u.databases)
    except:
      current_db = []
    
    if encrypt.decrypter(DB_NAME) in current_db:
      pass

    else:
      new_dbs = current_db.append(encrypt.decrypter(DB_NAME))
      u.databases = f"{current_db}"
      db.session.commit()
    
    return f"{encrypt.decrypter(DEF_TABLE)}"
  else:
    return "Invalid Request"
  
@views.route("/handler/get-all", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def get_all():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.get_all([is_verified[1], is_verified[2]], request.form['TABLE'])

    return str(query)
  else:
    return "Invalid Request"

@views.route("/handler/create-table/<string:AUTHENTICATION>/<string:TABLE_NAME>/<string:TABLE_SCHEMA>", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def create_table(AUTHENTICATION, TABLE_NAME, TABLE_SCHEMA):
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.create_table([is_verified[1], is_verified[2]], TABLE_NAME, TABLE_SCHEMA)

    return str(query)
  else:
    return "Invalid Request"

@views.route("/handler/add-entry", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def add_entry():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.add_entry([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['ENTRY'])

    return "None"
  else:
    return "Invalid Request"

@views.route("/handler/find-one", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def find_one():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.find_one([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['FIND_PAIR'])

    return str(query)
  else:
    return "Invalid Request"

@views.route("/handler/find-all", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def find_all():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.find_all([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['FIND_PAIR'])

    return str(query)
  else:
    return "Invalid Request"

@views.route("/handler/update-entry", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def update_entry():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.update_entry([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['COLUMN'], request.form['ENTRY'])

    return "None"
  else:
    return "Invalid Request"

@views.route("/handler/update-entry-dnd", methods=['POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def update_entry_dnd():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.update_entry_dnd([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['COLUMN'], request.form['ENTRY'])

    return "None"
  else:
    return "Invalid Request"

@views.route("/handler/delete-entry", methods=['GET', 'POST'])#/<string:DB_NAME>/<string:DB_PASSCODE>
def delete_entry():
  is_verified = vef_source.verify_TOKEN(request.form['SESSION TOKEN'])

  if is_verified[0] is True:
    query = sjson.delete_entry([is_verified[1], is_verified[2]], request.form['TABLE'], request.form['COLUMN'])

    return "None"
  else:
    return "Invalid Request"

