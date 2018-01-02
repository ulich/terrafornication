
from unittest import TestCase

import terrafornication

class TestTerrafornication(TestCase):
    
    def test_to_json(self):
        tf = terrafornication.Terrafornication()
        json = tf.to_json()
        self.assertTrue(isinstance(json, str))
        self.assertTrue('"resource":' in json)
