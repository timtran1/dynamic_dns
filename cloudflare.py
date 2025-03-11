import requests
from schemas import DomainConfig
import os
from dotenv import load_dotenv

load_dotenv()

CLOUDFLARE_EMAIL = os.environ.get('CLOUDFLARE_EMAIL', None)
CLOUDFLARE_API_KEY = os.environ.get('CLOUDFLARE_API_KEY', None)
CLOUDFLARE_API_ENDPOINT = 'https://api.cloudflare.com/client/v4'
HEADERS = {
    'X-Auth-Email': CLOUDFLARE_EMAIL,
    'X-Auth-Key': CLOUDFLARE_API_KEY
}


def get_zones():
    url = f'{CLOUDFLARE_API_ENDPOINT}/zones'
    res = requests.get(url, headers=HEADERS)
    return res.text


def get_dns_record(domain: DomainConfig) -> dict | None:
    url = f"{CLOUDFLARE_API_ENDPOINT}/zones/{domain.zone_id}/dns_records?name={domain.name}"
    res = requests.get(url, headers=HEADERS)
    response = res.json()
    result_list = response.get('result', None)

    if not result_list:
        return None

    data = result_list[0]
    data['zone_id'] = domain.zone_id

    return data


def update_dns_record(domain_record: dict, domain_config: DomainConfig, ip: str) -> str:
    url = f"{CLOUDFLARE_API_ENDPOINT}/zones/{domain_record['zone_id']}/dns_records/{domain_record['id']}"
    data = {
        'type': 'A',
        'name': domain_record['name'],
        'content': ip,
        'ttl': 120,
        'proxied': domain_config.proxied
    }

    res = requests.put(url, headers=HEADERS, json=data)
    return res.text


def create_dns_record(domain_config: DomainConfig, ip: str) -> str:
    url = f"{CLOUDFLARE_API_ENDPOINT}/zones/{domain_config.zone_id}/dns_records"
    data = {
        'type': 'A',
        'name': domain_config.name,
        'content': ip,
        'ttl': 120,
        'proxied': domain_config.proxied
    }

    res = requests.post(url, headers=HEADERS, json=data)
    return res.text
