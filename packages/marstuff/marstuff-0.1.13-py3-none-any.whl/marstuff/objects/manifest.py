from datetime import date

from marstuff.bases import Object
from marstuff.utils import convert, Extras


class Manifest(Object):
    def __init__(self, id=None, name=None, landing_date=None, launch_date=None, status=None, **extras):
        self.id = convert(id, int)
        self.name = convert(name, str)
        self.landing_date = convert(landing_date, date)
        self.launch_date = convert(launch_date, date)
        self.status = convert(status, str)
        self.extras: dict = convert(extras, Extras)
