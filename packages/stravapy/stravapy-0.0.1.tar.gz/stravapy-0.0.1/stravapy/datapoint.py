import datetime


class DataPoint:
    def __init__(self, lat, long, elevation, timestamp):
        self.lat = lat
        self.long = long
        self.elevation = elevation
        self.timestamp = timestamp
        self.datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    def get_dict(self):
        return{
            'lat': self.lat,
            'long': self.long,
            'elevation': self.elevation,
            'timestamp': self.timestamp,
            'datetime': self.datetime
        }
