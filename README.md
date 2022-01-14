# dynamic_dns

Keep your domains pointed at a machine IP even as your IP changes over time. 

Good for running home servers. Currently supports Cloudflare domains. You will need your [Cloudflare API key](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys#12345682).

Domains will be pointed at the machine that runs the project.

## Preqs

* Cloudflare email
* Cloudflare API key (instruction above)
* `zone_id` for each domain

How to get `zone_id`: On the Cloudflare dashboard, click on the website domain you want to use, click Overview tab, scroll down, and on the right side bar, you should see Zone ID under the API section.

All subdomains of the same site can use the same `zone_id`.

## Installation
Clone the repo and fill in above information at the `config.json` file
```
{
  "credentials": {
    "CLOUDFLARE_EMAIL": "tim@example.com",
    "CLOUDFLARE_API_KEY": "somevalue"
  },
  "domains": [
    {
      "name": "example.com",
      "zone_id": "someothervalue"
    },
    {
      "name": "subdomain.example.com",
      "zone_id": "someothervalue"
    }
  ]
}
```

`cd` into the folder and run

**With Docker**
```shell
docker-compose up -d
```

**Barebone**
```shell
pip3 install -r requirements.txt
python3 main.py
```

## Adding or removing domains

Edit `config.json` and run `docker restart dynamic_dns`
