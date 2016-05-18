# From SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Floorplan, Unit, User
engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

import json # import to enable reading JSON for unit info


user1 = User(name='Unknown', email='Unknown')
session.add(user1)
session.commit()

user2 = User(name='Rob Monday', email='rob.monday@gmail.com')
session.add(user2)
session.commit()

studio1 = Floorplan(name='Cozy Studio', square_footage=550, bedrooms=1, bathrooms=1, user_id=0)
session.add(studio1)
session.commit()

studio2 = Floorplan(name='Spacious Studio', square_footage=750, bedrooms=1, bathrooms=1, user_id=0)
session.add(studio2)
session.commit()

one_bedroom = Floorplan(name='Standard', square_footage=775, bedrooms=1, bathrooms=1, user_id=0)
session.add(one_bedroom)
session.commit()

loft = Floorplan(name='Loft', square_footage=695, bedrooms=1, bathrooms=1, user_id=0)
session.add(loft)
session.commit()

two_bedroom1 = Floorplan(name='Cozy Two-Bed', square_footage=900, bedrooms=2, bathrooms=1, user_id=0)
session.add(two_bedroom1)
session.commit()

two_bedroom2 = Floorplan(name='Large Two-Bed', square_footage=1150, bedrooms=2, bathrooms=2, user_id=0)
session.add(two_bedroom2)
session.commit()

print "Floorplan data populated successfully!"

try:
	with open('sample_data.json') as json_data:  # to see much more data, try:  sample_data_extended.json
	    dataload = json.load(json_data)
	    units = dataload['Unit']
	    # print units
	    iteration_num = 0
	    for unit in units:
	    	iteration_num += 1
	    	print 'Add unit # '+str(iteration_num)
	    	entry = Unit(name=unit['name'], floorplan_id=unit['floorplan_id'], user_id=unit['user_id'])
	    	session.add(entry)
	    	session.commit()
	print "Unit data populated successfully!"
except:
	print "JSON did not load"

