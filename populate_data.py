# From SQLalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Floorplan, Unit
engine = create_engine('sqlite:///apartment-inventory.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

studio1 = Floorplan(name='Cozy Studio', square_footage=550, bedrooms=1, bathrooms=1)
session.add(studio1)
session.commit()

studio2 = Floorplan(name='Spacious Studio', square_footage=750, bedrooms=1, bathrooms=1)
session.add(studio2)
session.commit()

one_bedroom = Floorplan(name='Standard', square_footage=775, bedrooms=1, bathrooms=1)
session.add(one_bedroom)
session.commit()

loft = Floorplan(name='Loft', square_footage=695, bedrooms=1, bathrooms=1)
session.add(loft)
session.commit()

two_bedroom1 = Floorplan(name='Cozy Two-Bedroom', square_footage=900, bedrooms=2, bathrooms=1)
session.add(two_bedroom1)
session.commit()

two_bedroom2 = Floorplan(name='Spacious Two-Bedroom', square_footage=1150, bedrooms=2, bathrooms=2)
session.add(two_bedroom2)
session.commit()

print "Floorplan data populated successfully!"

unit = Unit(name='5-101', floorplan_id=1)
session.add(unit)
session.commit()

unit = Unit(name='5-102', floorplan_id=2)
session.add(unit)
session.commit()

unit = Unit(name='5-103', floorplan_id=1)
session.add(unit)
session.commit()

unit = Unit(name='5-104', floorplan_id=2)
session.add(unit)
session.commit()

unit = Unit(name='5-105', floorplan_id=1)
session.add(unit)
session.commit()

unit = Unit(name='6-101', floorplan_id=3)
session.add(unit)
session.commit()

unit = Unit(name='6-102', floorplan_id=3)
session.add(unit)
session.commit()

unit = Unit(name='6-103', floorplan_id=3)
session.add(unit)
session.commit()

unit = Unit(name='6-104', floorplan_id=3)
session.add(unit)
session.commit()

unit = Unit(name='6-111', floorplan_id=4)
session.add(unit)
session.commit()

unit = Unit(name='6-112', floorplan_id=4)
session.add(unit)
session.commit()

unit = Unit(name='6-113', floorplan_id=4)
session.add(unit)
session.commit()

unit = Unit(name='6-114', floorplan_id=4)
session.add(unit)
session.commit()

print "Unit data populated successfully!"