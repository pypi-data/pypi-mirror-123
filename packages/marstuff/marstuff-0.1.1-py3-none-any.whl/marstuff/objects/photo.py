from __future__ import annotations

from datetime import date

from marstuff.bases import Object
from marstuff.objects.manifest import Manifest
from marstuff.utils import convert, Extras


class Photo(Object):
    def __init__(self, id=None, sol=None, camera=None, img_src=None, earth_date=None, rover=None, **extras):
        self.id = convert(id, int)
        self.sol = convert(sol, int)
        self.camera = convert(camera, Camera)
        self.img_src = convert(img_src, str)
        self.earth_date = convert(earth_date, date)
        self.rover = convert(rover, Manifest)
        self.extras: dict = convert(extras, Extras)


from marstuff.objects.camera import Camera
