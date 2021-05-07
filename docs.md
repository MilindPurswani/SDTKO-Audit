# Documentation

This project has many components that can be used to develop tools based on the requirements. Currently, the `audit.py` implements all these components in certain way to perform a single WhiteBox Test.

## Cloudflare.py 

Allows you to call cloudflare API if you have valid `CF_API_KEY` environmental variable set.

```python
>>> from Cloudflare import *
>>> c = Cloudflare()
>>> c.get_cname_domains('xve.io')
[{'sub': 'takeover1.xve.io', 'resolution': 'non-existing-domain.github.io'}, {'sub': 'takeover2.xve.io', 'resolution': 'non-existing-bucket.s3.amazonaws.com'}, {'sub': 'takeover3.xve.io', 'resolution': 'totallynonexistingdomain.com'}, {'sub': 'takeover4.xve.io', 'resolution': 'totallynonexistingdomain2.com'}, {'sub': 'takeover5.xve.io', 'resolution': 'takeover4.xve.io'}, {'sub': 'www.xve.io', 'resolution': 'xve.io'}]
```

## NucleiWrapper.py

Checks if Nuclei is installed on current system when the object of class is created.

```python
>>> from NucleiWrapper import *
>>> n = NucleiWrapper()
>>> n.check_takeover([{'sub': 'takeover1.xve.io', 'resolution': 'non-existing-domain.github.io'}, {'sub': 'takeover2.xve.io', 'resolution': 'non-existing-bucket.s3.amazonaws.com'}])
[{'sub': 'takeover1.xve.io', 'name': 'github takeover detection', 'tko': True, 'resolution': 'non-existing-domain.github.io'}, {'sub': 'takeover2.xve.io', 'name': 'AWS Bucket Takeover Detection', 'tko': True, 'resolution': 'non-existing-bucket.s3.amazonaws.com'}]
>>> 
```

The `check_takeover()` function takes a list of domain names and their resolution as input and outputs a list of domains that are vulnerable to subdomain takeovers

## TMOWrapper.py

Checks if takemeon is installed in a system or not. If yes, the `check_takeover()` function will check if there is any nxdomain based subdomain takeover.

```python
>>> from TMOWrapper import * 
>>> t = TMOWrapper()
>>> t.check_takeover([{'sub': 'takeover3.xve.io', 'resolution': 'totallynonexistingdomain.com'}, {'sub': 'takeover4.xve.io', 'resolution': 'totallynonexistingdomain2.com'}, {'sub': 'takeover5.xve.io', 'resolution': 'takeover4.xve.io'}, {'sub': 'www.xve.io', 'resolution': 'xve.io'}])
[{'resolution': 'totallynonexistingdomain.com', 'tko': True, 'name': 'Dangling CNAME', 'sub': 'takeover3.xve.io'}, {'resolution': 'totallynonexistingdomain2.com', 'tko': True, 'name': 'Dangling CNAME', 'sub': 'takeover4.xve.io'}, {'resolution': 'takeover4.xve.io', 'tko': True, 'name': 'Dangling CNAME', 'sub': 'takeover5.xve.io'}]
>>> 
```

