from mongoengine import Document, StringField, PointField, DateTimeField
from datetime import datetime


def db_drop_and_create_all(app, db):
    with app.app_context():
        # Drop all collections (similar to tables in SQL databases)
        db.connection.drop_database(db.get_db())

        # Create collections (automatically happens when you save a document)
        # Initial sample data:
        insert_sample_locations(app)


def insert_sample_locations(app):
    with app.app_context():
        loc1 = Location(
            description='Brandenburger Tor',
            geom=Location.point_representation(
                latitude=52.516247,
                longitude=13.377711
        )
        )
        loc1.save()

        loc2 = Location(
            description='Schloss Charlottenburg',
            geom=Location.point_representation(
                    latitude=52.520608,
                    longitude=13.295581
            )
        )
        loc2.save()

        loc3 = Location(
            description='Tempelhofer Feld',
            geom=Location.point_representation(
                latitude=52.473580,
                longitude=13.405252
            )
        )
        loc3.save()


class SpatialConstants:
    SRID = 4326

class Location(Document):
    description = StringField(max_length=80)
    geom = PointField()

    @staticmethod
    def point_representation(latitude, longitude):
        return [longitude, latitude]

    @staticmethod
    def get_items_within_radius(lat, lng, radius):
        results = Location.objects(geom__near=[lng, lat], geom__max_distance=radius)
        return [l.to_dict() for l in results]
   
    def get_location_latitude(self):
        return self.geom['coordinates'][1]

    def get_location_longitude(self):
        return self.geom['coordinates'][0]

    def to_dict(self):
        return {
            'id': str(self.id),
            'description': self.description,
            'location': {
                'lng': self.get_location_longitude(),
                'lat': self.get_location_latitude()
            }
        }
    
    def insert(self):
        self.save()

    def delete(self):
        self.delete()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()


class Post(Document):
    title = StringField(max_length=100, required=True)
    date_posted = DateTimeField(default=datetime.utcnow(), required=True)
    content = StringField(required=True)
