
from unittest import TestCase

from terrafornication import Terrafornication

class TestTerrafornication(TestCase):
    
    def test_to_json(self):
        tf = Terrafornication()
        tf.variable('foo', {})
        json = tf.to_json()

        self.assertTrue(isinstance(json, str))
        self.assertTrue('"variable":' in json)
