import time
import logging
from sdc11073 import wsdiscovery
from sdc11073.sdcclient import SdcClient
from sdc11073.mdib.clientmdib import ClientMdibContainer
from sdc11073.definitions_sdc import SDC_v1_Definitions
from sdc11073.loghelper import basic_logging_setup

wsd = wsdiscovery.WSDiscoverySingleAdapter('Ethernet')
wsd.start()

def find_spritzenpumpe():
    services = wsd.search_services(types=SDC_v1_Definitions.MedicalDeviceTypesFilter,
                                   timeout=10)

    for s in services:
        if 'arcomed' in s.epr:
            return s
    for s in services:
        print(s)


if __name__ == '__main__':
    basic_logging_setup()
    logging.getLogger('sdc.discover').setLevel(logging.WARNING)
    service = find_spritzenpumpe()
    if service is not None:
        client = SdcClient.from_wsd_service(service, ssl_context=None)
        client.start_all()
        mdib= ClientMdibContainer(client)
        mdib.init_mdib()
        while True:
            time.sleep(1)
    else:
        print('not found')


