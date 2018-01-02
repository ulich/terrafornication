from unittest import TestCase

from terrafornication import Terrafornication, DuplicateResourceException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = Terrafornication()


    def test_duplicate_resources(self):
        self.tf.resource('aws_instance', 'app1', {"foo": "bar"})

        self.assertRaises(DuplicateResourceException, lambda: self.tf.resource('aws_instance', 'app1', {}))


    def test_resource_references(self):
        instance = self.tf.resource('aws_instance', 'app1', {})
        self.tf.resource('aws_route53_record', instance.name + '_dns', {
            "records": [instance.ref('public_ip')]
        })

        self.assertEqual(self.tf.to_dict(), {
            "resource": {
                "aws_instance": {
                    "app1": {},
                },
                "aws_route53_record": {
                    "app1_dns": {
                        "records": ["${aws_instance.app1.public_ip}"]
                    }
                }
            }
        })
    

    def test_resource_name_reuse_in_properties(self):
        self.tf.resource('aws_route53_record', 'dns', lambda resource: {
            "name": resource.name
        })

        self.assertEqual(self.tf.to_dict(), {
            "resource": {
                "aws_route53_record": {
                    "dns": {
                        "name": "dns"
                    }
                }
            }
        })
