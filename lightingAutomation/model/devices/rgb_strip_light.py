from ext.attribute_packer import CollectionPackerMixin
from .rgb_light import RGBLight


class RGBStripLight(CollectionPackerMixin):
    def __init__(self, size):
        self.lights = tuple(RGBLight() for i in range(size))
        CollectionPackerMixin.__init__(self, self.lights)
        self.reset()

    def _average_group_attr(self, attr):
        return sum(getattr(light, attr) for light in self.lights) / len(self.lights)
    def _set_group_attr(self, attr, value):
        for light in self.lights:
            setattr(light, attr, value)

    @property
    def red(self):
        return self._average_attr('red')
    @red.setter
    def red(self, value):
        self._set_group_attr('red', value)

    @property
    def green(self):
        return self._average_attr('green')
    @green.setter
    def green(self, value):
        self._set_group_attr('green', value)

    @property
    def blue(self):
        return self._average_attr('blue')
    @blue.setter
    def blue(self, value):
        self._set_group_attr('blue', value)

    @property
    def rgb(self):
        return (self.red, self.green, self.blue)
    @rgb.setter
    def rgb(self, rgb):
        self.red, self.green, self.blue = rgb

    def reset(self):
        for light in self.lights:
            light.reset()
