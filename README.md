# SDTKO-Audit

SDTKO Audit is an auditing SDK and Whitebox tool that can be used in conjunction with Cloudflare to audit for subdomain takeovers. To use the `audit.py`, you will need your domain's DNS to be managed by Cloudflare.

The SDK utilizes two tools:
- [Nuclei Scanner](https://github.com/projectdiscovery/nuclei)
- [Takemeon](https://github.com/MilindPurswani/takemeon)

Using these 2 tools, we can check for any potential dangling `nxdomain` subdomain takeovers as well as 3rd party HTTP subdomain takeover. 

As an example, we have implemented `audit.py` that checks for subdomain takeover, sends slack notifications and also generates report.

## Features

:white_check_mark:  Checks for Subdomain Takeovers using Nuclei Scanner and takemeon.

:white_check_mark:  Integration with Cloudflare API.

:white_check_mark:  Support for sending notifications via slack.

:white_check_mark:  Allows generating a report with custom template `Jinja2`


## Installation

1. Install [Golang](https://golang.org/doc/install)

2. Install [Nuclei Scanner](https://github.com/projectdiscovery/nuclei)

```bash
GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
```

3. Install [Takemeon](https://github.com/MilindPurswani/takemeon)

```bash
~# go get -u github.com/milindpurswani/takemeon
```

4. Git clone the project

```bash
~# git clone https://github.com/MilindPurswani/SDTKO-Audit.git
```

5. Install requirements.txt

```bash
~# pip3 install -r requirements.txt
```

5. Setup `CF_API_KEY` - This is the most important aspect of this project, one needs their Cloudflare API Key to get all the CNAME records from their zone file. Kindly follow [this](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys) guide to obtain the API KEY. The API needs to have atleast read-only permission for the DNS Zone for the domain supplied for auditing. If you attempt to supply an API_KEY without permission to the DNS Zone of the domain, the script will throw an error.

```bash
~# echo "export CF_API_KEY=\"your-cf-api-key\"" > ~/.bashrc
```

6. Setup `SLACK_WEBHOOK_URL` - Slack webhook url is needed to get slack notification for scanning updates. To get your slack webhook url, follow the [guide](https://api.slack.com/messaging/webhooks) here. 

```bash
echo "export SLACK_WEBHOOK_URL=\"https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXX\"" > ~/.bashrc
```

## Usage

To use the Whitebox SDTKO-Audit tool, simply run the following command:

```bash
python3 audit.py <your-domain-name.com>
```

If you have not created any environment variables, use the following command:

```bash
~# CF_API_KEY="your-cf-api-key" SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXX" python3 audit.py <your-domain-name.com>
```

For more information on documentation checkout [docs.md](docs.md)


## Automation

The `audit.py` can be automated by creating a service something like this: 


1. Create a service with user, group and relevant environment variables. We need to set the  `CF_API_KEY` and `SLACK_WEBHOOK_URL` env variables. Make sure to edit the `WorkingDirectory` and `ExecStart` attributes and point them to your cloned repo location.

```bash
~# cat <<EOF >> /lib/systemd/system/sdtko-audit.service
[Unit]
Description=Subdomain Takeover Auditing service
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
Type=simple
User=root
group=root
Environment="CF_API_KEY=<your-api-key>"
Environment="SLACK_WEBHOOK_URL=https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXX"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin:/root/go/bin:/usr/local/go/bin:/root/go/bin"
WorkingDirectory=/root/project/SDTKO-Audit/
ExecStart=/usr/bin/python3 /root/project/SDTKO-Audit/audit.py xve.io
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
EOF

```

2. Reload the daemon

```bash
~# systemctl daemon-reload
```

3. Enable the service

```bash
~# systemctl enable sdtko-audit.service
```

4. Start the service

```bash
~# systemctl start sdtko-audit.service
```

5. Add Daily schedule to crontab

```bash
~# crontab -e
```

6. Add the following entry to your crontab to run the task daily at 9:30 AM in the morning


```
30 9 * * * service sdtko-audit start
```