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
	floorplans = session.query(Floorplan).all()
	units = session.query(Unit).all()
	return render_template('index.html', floorplans = floorplans, units = units)

@app.route('/floorplan/<floorplan_id>/')
def showFloorplan(floorplan_id):
	floorplans = session.query(Floorplan).filter_by(id=floorplan_id).all()
	units = session.query(Unit).filter_by(floorplan_id=floorplan_id).all()
	return render_template('floorplan.html', floorplans = floorplans, units = units)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/')
def showUnit(floorplan_id, unit_id):
	unit = session.query(Unit).filter_by(id=unit_id).one()
	return render_template('unit.html', unit = unit)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/edit/')
def editUnit(floorplan_id, unit_id):
	unit = session.query(Unit).filter_by(id=unit_id).one()
	return render_template('editunit.html', unit = unit)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)