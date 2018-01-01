from unittest import TestCase

import terrafornication
from terrafornication.provider import DuplicateResourceException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()


    def test_duplicate_resources(self):
        aws = self.tf.provider("aws", {})
        aws.resource('instance', 'app1', {"foo": "bar"})

        with self.assertRaises(DuplicateResourceException):
            aws.resource('instance', 'app1', {"foo": "baz"})


    def test_resource_references(self):
        aws = self.tf.provider("aws", {})
        instance = aws.resource('instance', 'app1', {})
        aws.resource('route53_record', instance.name + '_dns', {
            "records": [instance.ref('public_ip')]
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }],
            "data": {},
            "resource": {
                "aws_instance": {
                    "app1": {},
                },
                "aws_route53_record": {
                    "app1_dns": {
                        "records": ["${aws_instance.app1.public_ip}"]
                    }
                }
            },
            "output": {}
        })
    

    def test_resource_name_reuse_in_properties(self):
        aws = self.tf.provider("aws", {})
        aws.resource('route53_record', 'dns', lambda resource: {
            "name": resource.name
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }],
            "data": {},
            "resource": {
                "aws_route53_record": {
                    "dns": {
                        "name": "dns"
                    }
                }
            },
            "output": {}
        })
