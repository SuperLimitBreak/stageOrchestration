from ext.attribute_packer import AttributePackerMixin

from .rgb_light import RGBLight


class EffectRGBLight(RGBLight):
    def __init__(self, *args, x=0, y=0, globo=None, globo_rotation=0, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.globo = globo
        self.globo_rotation = globo_rotation
        AttributePackerMixin.__init__(self, (
            AttributePackerMixin.Attribute('x', 'onebyte'),
            AttributePackerMixin.Attribute('y', 'onebyte'),
            AttributePackerMixin.Attribute('globo', 'byte'),
            AttributePackerMixin.Attribute('globo_rotation', 'plusminusonebyte'),
        ))