# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from mw.tests.helpers import TestFixture
from mw.emql import emql

class TestNytimes_adapter(TestFixture):
    
    def setUp(self):
        super(TestNytimes_adapter, self).setUp()
        self.cache = emql.emql_cache()


    def run_query(self, q):
        api_key = self.mss.ctx.config['extensions.nytimes_articles']
        debug, cursors, results = self.mss.emqlread(None, q, {'debug': True, 'cache': False},
                                                    api_keys={'nytimes_articles': api_key}, 
                                                    cache=self.cache)
        return results

    def test_stephen_colbert(self):
        r = self.run_query({"id": "/en/stephen_colbert",
                            "/base/topics/news/nytimes": [{'limit': 4}]})
        assert r["/base/topics/news/nytimes"]
        self.assertEqual(len(r["/base/topics/news/nytimes"]), 4)

    def test_us_presidents(self):
        results = self.run_query([{"id": None,
                                   "/base/topics/news/nytimes": [{"limit": 1}],
                                   "limit": 3,
                                   "/people/person/date_of_birth": None,
                                   "sort": "-/people/person/date_of_birth",
                                   "type": "/government/us_president"}])
        for r in results:
            assert r["/base/topics/news/nytimes"]
            self.assertEqual(len(r["/base/topics/news/nytimes"]), 1)
        


