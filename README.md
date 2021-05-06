# SDTKO-Audit

SDTKO Audit is an auditing SDK and tool that can be used in conjunction with Cloudflare to audit for subdomain takeovers. 

The SDK utilizes two tools:
- [Nuclei Scanner](https://github.com/projectdiscovery/nuclei)
- [Takemeon](https://github.com/MilindPurswani/takemeon)

Using these 2 tools, we can check for any potential dangling `nxdomain` subdomain takeovers as well as 3rd party HTTP subdomain takeover. 

As an example, we have implemented `audit.py` that checks for subdomain takeover, sends slack notifications and also generates report.

## Features

:white_check_mark: Checks for Subdomain Takeovers using Nuclei Scanner and takemeon.

:white_check_mark: Integration with Cloudflare API.

:white_check_mark: Support for sending notifications via slack.

:white_check_mark: Allows generating a report with custom template `Jinja2`


## Installation

1. Install [Golang](https://golang.org/doc/install)

2. Install [Nuclei Scanner](https://github.com/projectdiscovery/nuclei)

```bash
GO111MODULE=on go get -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei
```

3. Install [Takemeon](https://github.com/MilindPurswani/takemeon)

```bash
go get -u github.com/milindpurswani/takemeon
```

4. Git clone the project

```bash
git clone https://github.com/MilindPurswani/SDTKO-Audit.git
```

5. Install requirements.txt

```bash
pip3 install -r requirements.txt
```

5. Setup `CF_API_KEY` - This is the most important aspect of this project, one needs their Cloudflare API Key to get all the CNAME records from their zone file. Kindly follow [this](https://support.cloudflare.com/hc/en-us/articles/200167836-Managing-API-Tokens-and-Keys) guide to obtain the API KEY. The API needs to have atleast read-only permission for the DNS Zone of target domain.

```bash
echo "export CF_API_KEY=\"your-cf-api-key\"" > ~/.bashrc
```

6. Setup `SLACK_WEBHOOK_URL` - Slack webhook url is needed to get slack notification for scanning updates. To get your slack webhook url, follow the [guide](https://api.slack.com/messaging/webhooks) here. 

```bash
echo "export SLACK_WEBHOOK_URL=\"https://hooks.slack.com/services/XXXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXX\"" > ~/.bashrc
```

