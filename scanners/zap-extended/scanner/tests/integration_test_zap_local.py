#!/usr/bin/env python3

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import logging
from zapv2 import ZAPv2

from scbzapv2 import ZapConfiguration
from scbzapv2 import ZapConfigureContext
from scbzapv2 import ZapConfigureSpider
from scbzapv2 import ZapConfigureActiveScanner

#######################################
### BEGINNING OF CONFIGURATION AREA ###
#######################################
## The user only needs to change variable values bellow to make the script
## work according to his/her needs. MANDATORY parameters must not be empty

# MANDATORY. Define the API key generated by ZAP and used to verify actions.
apiKey = 'eor898q1luuq8054e0e5r9s3jh'

# MANDATORY. Define the listening address of ZAP instance
localProxy = {
    "http": "http://127.0.0.1:8010",
    "https": "http://127.0.0.1:8010"
}

#################################
### END OF CONFIGURATION AREA ###
#################################

# set up logging to file - see previous section for more details
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s: %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    filename='zap-extended.log',
    filemode='w')

logging.info('Configuring ZAP Instance with %s', localProxy)
# Connect ZAP API client to the listening address of ZAP instance
zap = ZAPv2(proxies=localProxy, apikey=apiKey)

test_yaml_1 = "./tests/mocks/empty-files/"
test_yaml_2 = "./tests/mocks/empty/"
test_yaml_3 = "./tests/mocks/context-with-overlay/"
test_yaml_4 = "./tests/mocks/context-with-overlay-secrets/"
test_yaml_5 = "./tests/mocks/scan-full-bodgeit/"
test_yaml_6 = "./tests/mocks/scan-full-secureCodeBox.io/"

config = ZapConfiguration(test_yaml_5)
target = "http://bodgeit:8080/"

logging.info("ZAP Configuration: %s with type %s", config.get_config(),
              type(config.get_config()))
logging.info("ZAP Configuration/Contexts: %s with type %s",
              config.get_contexts(), type(config.get_contexts()))
logging.info("ZAP Configuration/Contexts/0: %s with type %s",
              config.get_context_by_index(0),
              type(config.get_context_by_index(0)))

# Starting to configure the ZAP Instance based on the given Configuration
if config.has_configurations() and config.has_context_configurations:
    local_zap_context = ZapConfigureContext(zap, config)

# if a ZAP Configuration is defined start to configure the running ZAP instance (`zap`)
if config and config.has_spider_configurations:
    # Starting to configure the ZAP Instance based on the given Configuration
    zap_spider = ZapConfigureSpider(zap, config)
    spider_id = zap_spider.start_spider_by_url(target, False)
    zap_spider.wait_until_finished(spider_id)

# if a ZAP Configuration is defined start to configure the running ZAP instance (`zap`)
if config and config.has_scan_configurations:
    # Starting to configure the ZAP Instance based on the given Configuration
    zap_scan = ZapConfigureActiveScanner(zap, config)
    # Search for the corresponding context based on the given targetUrl which should correspond to defined the spider url
    scan_id = zap_scan.start_scan_by_url(target)
    zap_scan.wait_until_finished(scan_id)
