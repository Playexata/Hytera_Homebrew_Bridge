#!/usr/bin/env python3

import configparser

from hytera_ip_site_connect.dmr import DMRHyteraService
from hytera_common.hytera_service_interface import HyteraServiceInterface
from hytera_ip_site_connect.p2p import P2PHyteraService
from hytera_ip_site_connect.rdac import RDACHyteraService
from hytera_ip_site_connect.storage import Storage


class HyteraIPSiteConnect(HyteraServiceInterface):
    p2p_service: P2PHyteraService = P2PHyteraService()
    dmr_service: DMRHyteraService = DMRHyteraService()
    rdac_service: RDACHyteraService = RDACHyteraService()
    storage: Storage = Storage()

    def load_settings(self):
        config = configparser.ConfigParser()
        config.sections()
        config.read("settings.ini")
        if "ip-site-connect" in config:
            constants = config["ip-site-connect"]
            if "DEFAULT_SERVICE_PORT" in constants:
                self.storage.set_service_port(
                    P2PHyteraService.__name__, int(constants["default_service_port"])
                )
            if "DEFAULT_DMR_PORT" in constants:
                self.storage.set_service_port(
                    DMRHyteraService.__name__, int(constants["default_dmr_port"])
                )
            if "DEFAULT_RDAC_PORT" in constants:
                self.storage.set_service_port(
                    RDACHyteraService.__name__, int(constants["default_rdac_port"])
                )
            if "DEFAULT_SERVICE_IP" in constants:
                self.storage.set_service_ip(str(constants["default_service_ip"]))

    def start(self) -> None:
        self.load_settings()

        self.dmr_service.set_storage(self.storage).start()
        self.rdac_service.set_storage(self.storage).start()
        self.p2p_service.set_storage(self.storage).start()
