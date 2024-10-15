import requests as r
import json

with open('/app/config.json') as f:
    credentials = json.load(f)['credentials']

CLOUDFLARE_EMAIL = credentials['CLOUDFLARE_EMAIL']
CLOUDFLARE_API_KEY = credentials['CLOUDFLARE_API_KEY']
CLOUDFLARE_API_ENDPOINT = 'https://api.cloudflare.com/client/v4'
HEADERS = {
    'X-Auth-Email': CLOUDFLARE_EMAIL,
    'X-Auth-Key': CLOUDFLARE_API_KEY
}


def get_zones():
    url = '%s/zones' % (
        CLOUDFLARE_API_ENDPOINT,
    )
    res = r.get(url, headers=HEADERS)
    return res.text


def get_dns_record(domain):
    url = '%s/zones/%s/dns_records?name=%s' % (
        CLOUDFLARE_API_ENDPOINT,
        domain['zone_id'],
        domain['name']
    )
    res = r.get(url, headers=HEADERS)
    result_list = res.json()['result']

    return result_list[0] if len(result_list) > 0 else None


def update_dns_record(domain_record, domain_config, ip):
    url = '%s/zones/%s/dns_records/%s' % (
        CLOUDFLARE_API_ENDPOINT,
        domain_record['zone_id'],
        domain_record['id']
    )
    data = {
        'type': 'A',
        'name': domain_record['name'],
        'content': ip,
        'ttl': 120,
        'proxied': domain_config.get('proxied', False)
    }

    res = r.put(url, headers=HEADERS, json=data)
    return res.text


def create_dns_record(domain_config, ip):
    url = '%s/zones/%s/dns_records' % (
        CLOUDFLARE_API_ENDPOINT,
        domain_config['zone_id']
    )
    data = {
        'type': 'A',
        'name': domain_config['name'],
        'content': ip,
        'ttl': 120,
        'proxied': domain_config.get('proxied', False)
    }

    res = r.post(url, headers=HEADERS, json=data)
    return res.text
