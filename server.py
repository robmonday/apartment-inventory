# Flask configuration
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)


# From SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Floorplan, Unit
engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


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

@app.route('/unit/<unit_id>/JSON/')
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
def newUnit():
	"""Add a new unit, based on floorplans that are already available"""
	if request.method == 'POST':
		newUnit = Unit(name=request.form['Name'], status=request.form['Status'], description=request.form['Description'], floorplan_id=request.form['Floorplan_ID'])
		session.add(newUnit)
		session.commit()
		return redirect(url_for('showAllInv'))
	else:
		return render_template('newunit.html')					

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)