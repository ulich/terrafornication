from unittest import TestCase

import terrafornication
from terrafornication.provider import DuplicateResourceException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()

    def test_multiple_providers_with_aliases(self):
        aws = self.tf.provider("aws", {})
        aws2 = self.tf.provider("aws", { "alias": "provider2" })

        aws.resource('instance', 'app1', {})
        aws2.resource('instance', 'app2', {})

        self.assertEqual(self.tf.to_dict(), {
            "provider": [{
                "aws": {}
            }, {
                "aws": {
                    "alias": "provider2"
                }
            }],
            "resource": {
                "aws_instance": {
                    "app1": {},
                    "app2": {
                        "provider": "aws.provider2"
                    }
                }
            }
        })

    def test_duplicate_resources(self):
        aws = self.tf.provider("aws", {})
        aws.resource('instance', 'app1', {"foo": "bar"})

        with self.assertRaises(DuplicateResourceException):
            aws.resource('instance', 'app1', {"foo": "baz"})
