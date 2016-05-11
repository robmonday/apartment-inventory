from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/all/')
@app.route('/inventory/')
def showAllInv():
	return "Here is the entire inventory, all floorplans and all units."

@app.route('/floorplan/<floorplan_id>')
def showFloorplanInv(floorplan_id):
	return "Here are all units for the %s floorplan." % (floorplan_id,)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>')
def showUnitDetail(floorplan_id, unit_id):
	return "Here are specific details for unit %s, which has the %s floorplan." % (unit_id, floorplan_id)

@app.route('/floorplan/<floorplan_id>/unit/<unit_id>/edit')
def showUnitDetail(floorplan_id, unit_id):
	return "This URL allows for editing details about unit %s." % (unit_id)


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)