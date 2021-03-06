import logging
import yaml
from itertools import groupby

from pysistence import make_dict

from .device_collection import DeviceCollection

from .devices.rgb_light import RGBLight
from .devices.rgb_strip_light import RGBStripLight
from .devices.effect_light import EffectRGBLight
from .devices.smoke import Smoke
from .devices.dmx_passthrough import DMXPassthru

log = logging.getLogger(__name__)

DEVICE_TYPES = make_dict({
    device_class.__name__: device_class
    for device_class in (RGBLight, RGBStripLight, EffectRGBLight, Smoke, DMXPassthru)
})


def device_collection_loader(path=None, data=None):
    if not path and not data:
        log.warning('device_collection_loader passed no path or data')
        return DeviceCollection()
    assert bool(path) ^ bool(data), 'Provide either a path or data'
    if path:
        log.debug(f'Loading device_collection: {path}')
        with open(path, 'rt') as filehandle:
            data = yaml.safe_load(filehandle)
    data = make_dict(data)

    def create_device(device_spec):
        if isinstance(device_spec, str):
            device_type = device_spec
            device_spec = {}
        else:
            device_type = device_spec.pop('device')
        assert device_type in DEVICE_TYPES, f'{device_type} is not a supported device. The valid options are {DEVICE_TYPES.keys()}'
        return DEVICE_TYPES[device_type](**device_spec)
    device_collection = DeviceCollection(make_dict({
        device_name: create_device(device_spec)
        for device_name, device_spec in data['devices'].items()
    }))

    # TODO: Possible bug?
    #   If yaml does not return ordered dict's this may fail.
    #   If pysistence does not support ordered dicts this may fail
    #   We may have to change the data structure to accommodate repeatable item order or build dependency order ourselfs
    #   The order appears to be preserved. So this may be fine
    for group_name, device_names in data.get('groups', {}).items():
        device_collection.add_group(group_name, device_names)

    # Display summary of devices loaded
    log.info('Loaded device_collection: {}'.format(
        tuple(
            f'{name}: {len(tuple(group_iterator))}'
            for name, group_iterator in groupby(
                type(device).__name__ for device in device_collection._devices.values()
            )
        )
    ))
    return device_collection
