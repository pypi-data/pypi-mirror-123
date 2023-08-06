from typing import *
from twopilabs.utils.scpi import ScpiResource
from .x1000_base import SenseX1000Base
from .x1000_scpi import SenseX1000ScpiDevice


class SenseX1000(SenseX1000Base):
    RESOURCE_DEVICE_MAP: Dict[Type[ScpiResource], Type[SenseX1000ScpiDevice]] = {
        ScpiResource: SenseX1000ScpiDevice
    }

    @classmethod
    def open_device(cls, resource: Union[ScpiResource], **kwargs) -> Union[SenseX1000ScpiDevice]:
        """Open the connection to a 2πSENSE X1000 series device and return a device object

        :param resource: A resource object to be opened
        :return: The device control object
        """
        if type(resource) not in cls.RESOURCE_DEVICE_MAP:
            raise TypeError(f'{type(resource)} is not a supported resource type')

        return cls.RESOURCE_DEVICE_MAP[type(resource)](resource, **kwargs)

    @classmethod
    def find_devices(cls, **kwargs) -> List[Union[ScpiResource]]:
        """Find 2πSENSE X1000 series devices connected to this computer and return a list of resources objects

        :param kwargs: Keyword arguments used by resource transports to control the discovery process
        :return: A list of resource objects
        """
        devices = []

        for device_type in cls.RESOURCE_DEVICE_MAP.values():
            devices += device_type.find_devices(**kwargs)

        return devices
