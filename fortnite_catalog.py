from flask import (
	Flask, render_template, request, redirect, url_for, flash, jsonify)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fortnite_database_setup import Base, User, Weapon, WeaponDetail


from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Fortnite Catalog"

engine = create_engine('sqlite:///fortniteweapondatabase.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token


@app.route('/login')
def showLogin():
	state = ''.join(random.choice(
		string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


#  Gconnect method for google sign-in


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
        return response

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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
        	'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it does not make a new one
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
    output += ' " style = "width: 300px; height: 300px;border-radius:'
    output += ' 150px;-webkit-border-radius:'
    output += ' 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


#  User Helper Functions


def createUser(login_session):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Route for GDisconnect to disconnect from login session.
# Revoke's user token and reset login_session.


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
        	'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/' +
    	'revoke?token=%s' % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('showWeapons'))
    else:
        response = make_response(
        	json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Route for root of site to show all weapon classes


@app.route('/')
@app.route('/fortnite')
def showWeapons():
	weapons = session.query(Weapon).all()
	if 'username' not in login_session:
		return render_template('publicfortnite.html', weapons=weapons)
	else:
		return render_template('fortnite.html', weapons=weapons)

# Route to add new weapon


@app.route('/fortnite/new', methods=['GET', 'POST'])
def newWeapon():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		if request.form['name']:
			newWeapon = Weapon(
				name=request.form['name'], user_id=login_session['user_id'])
			session.add(newWeapon)
			session.commit()
		return redirect(url_for('showWeapons'))
	return render_template('newWeapon.html')


# Route to edit existing weapon


@app.route('/fortnite/<string:weapon_name>/edit', methods=['GET', 'POST'])
def editWeapon(weapon_name):
	if 'username' not in login_session:
		return redirect('/login')
	editedWeapon = session.query(Weapon).filter_by(name=weapon_name).one()
	if editedWeapon.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this weapon.  Are you its creator?');}</script><body onload='myFunction()''>"  # noqa
	if request.method == 'POST':
		if request.form['name']:
			editedWeapon.name = request.form['name']
			session.add(editedWeapon)
			session.commit()
		return redirect(url_for('showWeapons'))
	return render_template('editWeapon.html', weapon=editedWeapon)


# Route to delete existing weapon


@app.route('/fortnite/<string:weapon_name>/delete', methods=['GET', 'POST'])
def deleteWeapon(weapon_name):
	if 'username' not in login_session:
		return redirect('/login')
	deletedWeapon = session.query(Weapon).filter_by(name=weapon_name).one()
	if deletedWeapon.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this weapon.  Are you its creator?);}</script><body onload='myFunction()''>"  # noqa
	if request.method == 'POST':
		session.delete(deletedWeapon)
		session.commit()
		return redirect(url_for('showWeapons'))
	return render_template('deleteWeapon.html', weapon=deletedWeapon)


# Route to show list of all types of a weapon


@app.route('/fortnite/<string:weapon_name>/list')
def showWeaponList(weapon_name):
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	items = session.query(WeaponDetail).filter_by(weapon_id=weapon.id)
	if 'username' not in login_session:
		return render_template('publicWeaponList.html', weapon=weapon, items=items)
	else:
		return render_template('weaponList.html', weapon=weapon, items=items)

# Route to show a specific weapon detail


@app.route('/fortnite/<string:weapon_name>/list/<string:weapon_detail_name>')
def showWeaponDetail(weapon_name, weapon_detail_name):
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	weapon_detail = session.query(
		WeaponDetail).filter_by(name=weapon_detail_name).one()
	if 'username' not in login_session:
		return render_template(
			'publicWeaponDetail.html', weapon=weapon, weapon_detail=weapon_detail)
	else:
		return render_template(
			'weaponDetail.html', weapon=weapon, weapon_detail=weapon_detail)


# Route to add weapon detail


@app.route('/fortnite/<string:weapon_name>/list/new', methods=['GET', 'POST'])
def newWeaponDetail(weapon_name):
	if 'username' not in login_session:
		return redirect('/login')
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	if request.method == 'POST':
		new_weapon_detail = WeaponDetail(
			name=request.form['name'],
			description=request.form['description'],
			color=request.form['color'],
			damage=request.form['damage'],
			weapon_id=weapon.id,
			user_id=login_session['user_id'])
		session.add(new_weapon_detail)
		session.commit()
		return redirect(url_for('showWeaponList', weapon_name=weapon.name))
	return render_template('newWeaponDetail.html', weapon_name=weapon_name)


# Route to edit weapon detail


@app.route('/fortnite/<string:weapon_name>/list/<string:weapon_detail_name>/edit', methods=['GET', 'POST'])  # noqa
def editWeaponDetail(weapon_name, weapon_detail_name):
	if 'username' not in login_session:
		return redirect('/login')
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	editedWeaponDetail = session.query(WeaponDetail).filter_by(
		name=weapon_detail_name).one()
	if editedWeaponDetail.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to edit this weapon.  Are you its creator?');}</script><body onload='myFunction()''>"  # noqa
	if request.method == 'POST':
		if request.form['name']:
			editedWeaponDetail.name = request.form['name']
		if request.form['description']:
			editedWeaponDetail.description = request.form['description']
		if request.form['color']:
			editedWeaponDetail.color = request.form['color']
		if request.form['damage']:
			editedWeaponDetail.damage = request.form['damage']
		session.add(editedWeaponDetail)
		session.commit()
		return redirect(url_for('showWeaponList', weapon_name=weapon.name))
	return render_template(
		'editWeaponDetail.html',
		weapon_detail=editedWeaponDetail,
		weapon_name=weapon.name)


# Route to delete weapon detail


@app.route('/fortnite/<string:weapon_name>/list/<string:weapon_detail_name>/delete', methods=['GET', 'POST'])  # noqa
def deleteWeaponDetail(weapon_name, weapon_detail_name):
	if 'username' not in login_session:
		return redirect('/login')
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	deletedWeaponDetail = session.query(WeaponDetail).filter_by(
		name=weapon_detail_name).one()
	if deletedWeaponDetail.user_id != login_session['user_id']:
		return "<script>function myFunction() {alert('You are not authorized to delete this weapon.  Are you its creator?');}</script><body onload='myFunction()''>"  # noqa
	if request.method == 'POST':
		session.delete(deletedWeaponDetail)
		session.commit()
		return redirect(url_for('showWeaponList', weapon_name=weapon.name))
	return render_template(
		'deleteWeaponDetail.html',
		weapon_detail=deletedWeaponDetail,
		weapon_name=weapon.name)


# Route to homepage JSON format


@app.route('/fortnite/JSON')
def weaponJSON():
	weapons = session.query(Weapon).all()
	return jsonify(Weapons=[weapon.serialize for weapon in weapons])


# Route to weapon list JSON format


@app.route('/fortnite/<string:weapon_name>/JSON')
def weaponListJSON(weapon_name):
	weapon = session.query(Weapon).filter_by(name=weapon_name).one()
	items = session.query(WeaponDetail).filter_by(weapon_id=weapon.id)
	return jsonify(Weapon_List=[i.serialize for i in items])


# Route to individual weapon detail JSON format


@app.route('/fortnite/<string:weapon_name>/list/<string:weapon_detail_name>/JSON')  # noqa
def weaponDetailJSON(weapon_name, weapon_detail_name):
	item = session.query(WeaponDetail).filter_by(name=weapon_detail_name).one()
	return jsonify(Weapon=item.serialize)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
