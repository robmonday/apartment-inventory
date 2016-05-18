# Flask configuration
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


# SQLalchemy Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Floorplan, Unit, User
engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.bind = engine

# Import libraries used in initial 3rd-party authentication
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Import libraries used for login_required decorator
from functools import wraps
from flask import g, request, redirect, url_for

engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

"""================================================= Authentication Code"""


# Start of initial 3rd-party authentication

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id'] # this is how Google identifies the app
APPLICATION_NAME = "Apartment Unit Availability"

# Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user email exists, if not make a new user
    user_records = session.query(User).filter_by(email=login_session['email']).all()
    if (len(user_records)<1):
    	print "New user in database"
    else:
    	print "Existing user in database"

    # Store user_id for login session:  see if user email exists, if not make a new user
    user_id = getUserID(login_session['email'])
    if not user_id:
    	user_id = createUser(login_session) 
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
            -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/logout/')
def logout():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	# return "The current session state is %s" % login_session['state']
	floorplans = session.query(Floorplan).all()
	units = session.query(Unit).all()
	return render_template('index.html', floorplans = floorplans, units = units)

def createUser(login_session):
	"""Create new user in database from login session, then return user ID"""
	newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).all()[0]
	return user.id

def getUserInfo(user_id):
	"""Pass in user ID, and function returns associated user object"""
	user = session.query(User).filter_by(id = user_id).one()
	return user

def getUserID(email):
	"""Pass in user email, and function returns user ID (if email exists in DB)"""
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None

def login_required(f):
	"""Add login required decorator to ensure appropriate security"""
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if login_session.get('gplus_id') is None:  #Is this right?!  Where can I get a global variable that represents a logged in user
			return redirect(url_for('showLogin', next=request.url))
		return f(*args, **kwargs)
	return decorated_function

"""================================================= Authentication Code"""

@app.route('/')
@app.route('/all/')
@app.route('/inventory/')
def showAllInv():
	"""See all units together.  Top Level."""
	floorplans = session.query(Floorplan).all()
	units = session.query(Unit).all()
	return render_template('index.html', floorplans = floorplans, units = units)

@app.route('/JSON/')
@app.route('/all/JSON/')
@app.route('/inventory/JSON/')
def allInvJSON():
	"""JSON that returns all units in inventory"""
	units = session.query(Unit).all()
	return jsonify (Unit=[unit.serialize for unit in units])

@app.route('/floorplan/<floorplan_id>/JSON/')
def floorplanJSON(floorplan_id):
	"""JSON that returns all units for a given floorplan"""
	units = session.query(Unit).filter_by(floorplan_id=floorplan_id).all()
	return jsonify (Unit=[unit.serialize for unit in units])

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/JSON/')
def unitJSON(floorplan_id, unit_id):
	"""JSON that returns information for a single unit"""
	units = session.query(Unit).filter_by(id=unit_id).all()
	return jsonify (Unit=[unit.serialize for unit in units])

@app.route('/floorplan/<floorplan_id>/') 
def showFloorplan(floorplan_id):
	"""See all units for a single floorplan."""
	floorplans = session.query(Floorplan).filter_by(id=floorplan_id).all()
	units = session.query(Unit).filter_by(floorplan_id=floorplan_id).all()
	return render_template('floorplan.html', floorplans = floorplans, units = units)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/')
def showUnit(floorplan_id, unit_id):
	"""See detail for a specific floorplan."""
	unit = session.query(Unit).filter_by(id=unit_id).one()
	return render_template('unit.html', unit = unit)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/edit/', methods=['GET','POST'])
@login_required
def editUnit(floorplan_id, unit_id):
	"""Change details for a specific unit"""
	editedUnit = session.query(Unit).filter_by(id=unit_id).one()
	if request.method == 'POST':
		if request.form['Description']:
			editedUnit.description = request.form['Description']
		if request.form['Status']:
			editedUnit.status = request.form['Status']
		session.add(editedUnit)
		session.commit()
		return redirect(url_for('showUnit', floorplan_id=floorplan_id, unit_id=unit_id))
	else:
		return render_template('editunit.html', unit = editedUnit, floorplan_id=floorplan_id, unit_id=unit_id)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/delete/', methods=['GET','POST'])
@login_required
def deleteUnit(floorplan_id, unit_id):
	"""Delete a unit"""
	deletedUnit = session.query(Unit).filter_by(id=unit_id).one()
	if request.method == 'POST':
		session.delete(deletedUnit)
		session.commit()
		return redirect(url_for('showAllInv'))
	else:
		return render_template('deleteunit.html', unit = deletedUnit, floorplan_id=floorplan_id, unit_id=unit_id)


@app.route('/newunit/', methods=['GET','POST'])
@login_required
def newUnit():
	"""Add a new unit, based on floorplans that are already available"""
	if request.method == 'POST':
		newUnit = Unit(
			name=request.form['Name'], 
			status=request.form['Status'], 
			description=request.form['Description'], 
			floorplan_id=request.form['Floorplan_ID'], 
			user_id=session_user)
		session.add(newUnit)
		session.commit()
		return redirect(url_for('showAllInv'))
	else:
		return render_template('newunit.html')					

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True #Note: turn this off for production version
	app.run(host = '0.0.0.0', port = 5000)