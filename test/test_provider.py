# vim: set fileencoding=utf-8 :
#
# Copyright (c) 2013 Daniel Truemper <truemped at googlemail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
from __future__ import absolute_import, division, print_function, with_statement

import sys
if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

from supercell.api.metatypes import ContentType
from supercell.api.provider import ProviderBase, JsonProvider


class MoreDetailedJsonProvider(JsonProvider):

    CONTENT_TYPE = ContentType('application/json', vendor='supercell')


class JsonProviderWithVendorAndVersion(JsonProvider):

    CONTENT_TYPE = ContentType('application/json', vendor='supercell',
                               version=1.0)


class TestBasicProvider(TestCase):

    def test_default_json_provider(self):
        provider = ProviderBase.map_provider('application/json')
        self.assertIs(provider, JsonProvider)

    def test_specific_json_provider(self):
        provider = ProviderBase.map_provider('application/vnd.supercell+json')
        self.assertIs(provider, MoreDetailedJsonProvider)

    def test_json_provider_with_version(self):
        provider = ProviderBase.map_provider(
                'application/vnd.supercell-v1.0+json')
        self.assertIs(provider, JsonProviderWithVendorAndVersion)