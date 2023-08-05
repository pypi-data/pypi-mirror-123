import time
from threading import Timer
import atexit

from modular_client import ModularClient

try:
    from pkg_resources import get_distribution, DistributionNotFound
    import os
    _dist = get_distribution('lickport_array_interface_interface')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'lickport_array_interface_interface')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except (ImportError,DistributionNotFound):
    __version__ = None
else:
    __version__ = _dist.version


DEBUG = False

class LickportArrayInterface():
    '''
    '''
    _CHECK_DATA_PERIOD = 1.0
    def __init__(self,*args,**kwargs):
        if 'debug' in kwargs:
            self.debug = kwargs['debug']
        else:
            kwargs.update({'debug': DEBUG})
            self.debug = DEBUG
        atexit.register(self._exit)
        self.controller = ModularClient()
        self.controller.set_time(int(time.time()))
        self.data = []

    def start_check_data_timer(self):
        self._check_data_timer = Timer(self._CHECK_DATA_PERIOD,self._check_data)
        self._check_data_timer.start()

    def _check_data(self):
        self.start_check_data_timer()
        data = self.controller.get_and_clear_lick_data()
        if len(data) > 0:
            for datum in data:
                print(datum)
            self.data.extend(data)

    def _exit(self):
        try:
            self._check_data_timer.cancel()
        except AttributeError:
            pass

def main(args=None):
    debug = False
    lai = LickportArrayInterface(debug=debug)
    lai.start_check_data_timer()

# -----------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
