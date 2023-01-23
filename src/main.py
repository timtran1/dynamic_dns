import requests as r
import json
import time
from cloudflare import get_dns_record, update_dns_record, create_dns_record
from datetime import datetime

with open('/app/config.json') as f:
    domains = json.load(f)['domains']
    
def timestamp():
    return datetime.now().strftime('%d/%m/%Y %H:%M:%S')

print(timestamp() + ' - Dynamic DNS started for %s' % ','.join(
    [domain['name'] for domain in domains]))

current_ip = r.get('https://api.ipify.org').content.decode('utf8')
print(timestamp() + ' - Current IP is ' + current_ip)

for domain in domains:
    domain_record = get_dns_record(domain)

    if not domain_record or domain_record['content'] != current_ip or domain_record['proxied'] != domain.get('proxied', False):
        print(timestamp() + ' - Updating DNS data')

        if domain_record:
            print(timestamp() + ' - Existing DNS record found for %s, updating...' % domain[
                'name'])
            result = update_dns_record(domain_record, current_ip)
            print(result)

        else:
            print(
                timestamp() + ' - No DNS record found for %s, creating...' % domain['name'])
            result = create_dns_record(domain, current_ip)
            print(result)