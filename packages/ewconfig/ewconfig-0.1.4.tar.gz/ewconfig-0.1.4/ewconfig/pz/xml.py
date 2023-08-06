from enum import Enum
from logging import getLogger
from re import sub

from .pz import PolesZeros

log = getLogger(__name__)


class Response(Enum):
    DISPLACEMENT = 1
    VELOCITY = 2
    ACCELERATION = 3


class UnsupportedResponseException(Exception): pass


PZ_FMT = '\t%+.6e\t%+.6e\n'
PZ_FMT_LO = '\t%+.5e \t%+.5e \n'


class XmlPolesZeros(PolesZeros):

    def __init__(self, net, sta, chan, lo_precision=False, default_response=None):
        super().__init__()
        self.__parse(net, sta, chan, lo_precision=lo_precision, default_response=default_response)

    def __parse(self, net, sta, chan, lo_precision=False, default_response=None):
        self.lat = chan.latitude
        self.lon = chan.longitude
        self.elev = chan.elevation
        self.net = net.code
        self.sta = sta.code
        self.chan = chan.code
        self.loc = chan.location_code if chan.location_code else '--'
        # the following is based on the implementation of Response.get_sacpz which gets the same data
        # that the original code used
        # https://github.com/obspy/obspy/blob/e7b9474573e15a586cb8ce73df9bbe677f0d7421/obspy/core/inventory/response.py#L1956
        # for some reason that doesn't correct to displacement (and mike doesn't think that's a problem)
        try:
            paz = chan.response.get_paz()  # may raise an exception if there is none
            self.constant = paz.normalization_factor * chan.response.instrument_sensitivity.value
            self.zeros_lines = [self.__format_pz(c, lo_precision) for c in paz.zeros]
            self.poles_lines = [self.__format_pz(c, lo_precision) for c in paz.poles]
            response = self.__response_from_input_units(chan, default_response=default_response)
            if self.zeros_lines or self.poles_lines:
                for _ in range(response.value-1):  # shift to displacement
                    # has to be at start to match original
                    self.zeros_lines.insert(0, self.__format_pz(0j, lo_precision))
        except UnsupportedResponseException:
            raise
        except Exception as e:
            log.debug(f'Discarding {e} ({type(e)})')
            log.info(f'No PAZ data in {self}')

    def __format_pz(self, imag, lo_precision):
        # the original code printed more precision than it actually had(!)
        if lo_precision:
            text = PZ_FMT_LO % (imag.real, imag.imag)
            return sub(r'e([-+]\d{2}) ', r'0e\1', text)
        else:
            return PZ_FMT % (imag.real, imag.imag)

    def __response_from_input_units(self, chan, default_response=None):
        try:
            instrument_sensitivity = chan.response.instrument_sensitivity
            units_map = {'m': Response.DISPLACEMENT,
                         'm/s': Response.VELOCITY,
                         'm/s**2': Response.ACCELERATION}
            input_units = instrument_sensitivity.input_units.lower()
            if input_units == 'pa':
                raise UnsupportedResponseException('Pressure sensitive detector')
            if input_units in units_map:
                response = units_map[input_units]
                log.debug(f'Input units {input_units} => {response}')
                return response
            log.warning(f'Could not parse input units {input_units} for {self}')
        except UnsupportedResponseException as e:
            raise
        except Exception as e:
            log.warning(f'Could not infer response for {self} ({e})')
        if default_response:
            log.info(f'Using default response for {self}: {default_response}')
            return default_response
        else:
            raise UnsupportedResponseException(f'Cannot infer response type for {self} '
                                               f'(use --velocity etc to override))')
