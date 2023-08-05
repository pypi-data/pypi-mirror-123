# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyzonevalidator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyzonevalidator',
    'version': '0.3.1',
    'description': 'Validate DNS Zones programmatically',
    'long_description': "# PyZoneValidator\n\nCode example:\n\n```python\n\nzv = zoneValidator()\nfrom pprint import pprint\npprint(zv.validate('dnssec-failed.org', fail_if_not_signed=False))\n\n# Output:\n#{'errors': [DNSSEC_DS_AND_DNSKEY_RECORD_DO_NOT_MATCH: DNSSEC: DS and DNSKEY key do not align for zone 'dnssec-failed.org'. [dns102.comcast.net.],\n#            DNSSEC_DS_AND_DNSKEY_RECORD_DO_NOT_MATCH: DNSSEC: DS and DNSKEY key do not align for zone 'dnssec-failed.org'. [dns101.comcast.net.],\n#            DNSSEC_DS_AND_DNSKEY_RECORD_DO_NOT_MATCH: DNSSEC: DS and DNSKEY key do not align for zone 'dnssec-failed.org'. [dns105.comcast.net.],\n#            DNSSEC_DS_AND_DNSKEY_RECORD_DO_NOT_MATCH: DNSSEC: DS and DNSKEY key do not align for zone 'dnssec-failed.org'. [dns103.comcast.net.],\n#            DNSSEC_DS_AND_DNSKEY_RECORD_DO_NOT_MATCH: DNSSEC: DS and DNSKEY key do not align for zone 'dnssec-failed.org'. [dns104.comcast.net.]],\n# 'warnings': []}\n\n```\n\n",
    'author': 'Teun Ouwehand',
    'author_email': 'teun@nextpertise.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
