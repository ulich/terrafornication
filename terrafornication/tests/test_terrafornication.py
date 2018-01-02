
from unittest import TestCase

import terrafornication

class TestTerrafornication(TestCase):
    
    def test_to_json(self):
        tf = terrafornication.Terrafornication()
        tf.variable('foo', {})
        json = tf.to_json()

        self.assertTrue(isinstance(json, str))
        self.assertTrue('"variable":' in json)
