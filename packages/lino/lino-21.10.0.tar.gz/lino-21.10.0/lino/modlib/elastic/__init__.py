# Copyright 2008-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Intelligent search functionality.

Requires Elasticsearch to be installed.
"""

import os
import subprocess
from lino.api import ad
from lino.core.utils import get_models


class Plugin(ad.Plugin):

    ES_url = 'localhost:9200' # running a docker instance locally
    """URL to the elasticsearch instance"""

    debian_dev_server = False

    def on_site_startup(self, site):
        if self.debian_dev_server:
            p = subprocess.Popen('docker -v'.split(), stdout=subprocess.PIPE)
            _, err = p.communicate()
            if err is not None:
                pass

        ds = site.django_settings

        indexes = {}
        for m in get_models():
            if hasattr(m, 'ES_index') and m.ES_index is not None:
                indexes[m.ES_index]['models'].append(m)

        ds['SEARCH_SETTINGS'] = {
            'connections': {
                'defaults': self.ES_url,
            },
            'indexes': indexes,
            'settings': {
                'auto_sync': True,
            },
        }

    def get_required_plugins(self):
        yield 'about'

    def get_requirements(self):
        yield 'elasticsearch-django'
