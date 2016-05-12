from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)



@app.route('/')
@app.route('/all/')
@app.route('/inventory/')
def showAllInv():
	# return "Here is the entire inventory, all floorplans and all units."
	return render_template('index.html')

@app.route('/floorplan/<floorplan_id>/')
def showFloorplanInv(floorplan_id):
	# return "Here are all units for the %s floorplan." % (floorplan_id,)
	return render_template('floorplan.html', floorplan_id = floorplan_id)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/')
def showUnitDetail(floorplan_id, unit_id):
	# return "Here are specific details for unit %s, which has the %s floorplan." % (unit_id, floorplan_id)
	return render_template('unit.html', floorplan_id = floorplan_id, unit_id = unit_id)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/edit/')
def editUnit(floorplan_id, unit_id):
	# return "This URL allows for EDITING details about unit %s." % (unit_id,)
	return render_template('editunit.html', floorplan_id = floorplan_id, unit_id = unit_id)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)