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
'''Helpers for dealing with HTTP level caching.'''
from __future__ import absolute_import, division, print_function, with_statement

from collections import namedtuple
from functools import wraps


__all__ = []


CacheConfigT = namedtuple('CacheConfigT', ['max_age', 's_max_age', 'public',
                                           'private', 'no_cache', 'no_store',
                                           'must_revalidate',
                                           'proxy_revalidate'])

def CacheConfig(max_age, s_max_age=None, public=False, private=False,
                no_cache=False, no_store=False, must_revalidate=True,
                proxy_revalidate=False):
    '''Create a :class:`CacheConfigT` with default values.'''
    return CacheConfigT(max_age, s_max_age=s_max_age, public=public,
                        private=private, no_cache=no_cache, no_store=no_store,
                        must_revalidate=must_revalidate,
                        proxy_revalidate=proxy_revalidate)


def cache(max_age, s_max_age=None, public=False, private=False, no_cache=False,
          no_store=False, must_revalidate=True, proxy_revalidate=False):
    '''Set the `Cache-Control` HTTP header to allow for fine grained caching
    controls.

    For detailed information read http://www.mnot.net/cache_docs/ and
    http://www.ietf.org/rfc/rfc2616.txt

    Usage::

        @cache(timedelta(minutes=10))
        def get(self):
            self.finish({'ok': True})

    This would allow public caches to store the result for 10 minutes.

    :param max_age: Number of seconds the response can be cached
    :type max_age: datetime.timedelta

    :param s_max_age: Like `max_age` but only applies to shared caches
    :type s_max_age: datetime.timedelta

    :param public: Marks responses as cachable even if they contain
                   authentication information
    :type public: bool

    :param private: Allows the browser to cache the result but not shared
                    caches
    :type private: bool

    :param no_cache: If *True* caches will revalidate the request before
                     delivering the cached copy
    :type no_cache: bool

    :param no_store: Caches should not store any cached copy.
    :type no_store: bool

    :param must_revalidate: Tells the cache to not serve stale copies of the
                            response
    :type must_revalidate: bool

    :param proxy_revalidate: Like `must_revalidate` except it only applies to
                             public caches
    :type proxy_revalidate: bool
    '''

    def wrapper(fn):

        @wraps(fn)
        def _func(self, *args, **kwargs):
            '''Inner method setting the HTTP header according to the params.'''
            cache_config = CacheConfig(max_age, s_max_age=s_max_age,
                                       public=public, private=private,
                                       no_cache=no_cache, no_store=no_store,
                                       must_revalidate=must_revalidate,
                                       proxy_revalidate=proxy_revalidate)

            self.set_header('Cache-Control',
                            compute_cache_header(cache_config))
            return fn(self, *args, **kwargs)

        return _func
    return wrapper


def compute_cache_header(cache_config):
    '''Compute the cache header for a given :class:`CacheConfigT`.

    :param cache_config: The :class:`CacheConfigT` defining the cache params
    :type cache_config: :class:`supercell.api.cache.CacheConfigT`
    :return: The computed `Cache-Control` header
    :rtype: str
    '''
    params = []
    params.append('max-age=%s' % cache_config.max_age.seconds)
    if cache_config.s_max_age:
        params.append('s-max-age=%s' % cache_config.s_max_age.seconds)
    if cache_config.public:
        params.append('public')
    if cache_config.private:
        params.append('private')
    if cache_config.no_cache:
        params.append('no-cache')
    if cache_config.no_store:
        params.append('no-store')
    if cache_config.must_revalidate:
        params.append('must-revalidate')
    if cache_config.proxy_revalidate:
        params.append('proxy-revalidate')

    return ', '.join(params)
