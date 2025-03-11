import requests as r
import json
from cloudflare import get_dns_record, update_dns_record, create_dns_record
import logging
from schemas import DomainConfig
import logging_config

logger = logging.getLogger(__name__)

with open('config.json') as f:
    domains = json.load(f)['domains']

logger.info(f"Dynamic DNS started for {', '.join([domain['name'] for domain in domains])}")
current_ip = r.get('https://api.ipify.org').content.decode('utf8')
logger.info(f'Current IP is {current_ip}')

for config in domains:
    domain_config = DomainConfig(**config)
    domain_record = get_dns_record(domain_config)

    if (
            not domain_record or
            domain_record['content'] != current_ip or
            domain_record['proxied'] != domain_config.get('proxied', False)
    ):
        logger.info(f'Updating DNS data for {domain_config.name}')

        if domain_record:
            logger.info(f"Existing DNS record found for {domain_config.name}, updating...")
            result = update_dns_record(domain_record, domain_config, current_ip)
            logger.info(result)

        else:
            logger.info(f"No DNS record found for {domain_config.name}, creating...")
            result = create_dns_record(domain_config, current_ip)
            logger.info(result)
