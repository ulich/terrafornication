from unittest import TestCase

import terrafornication
from terrafornication.provider import DuplicateDataSourceException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()


    def test_data_sources(self):
        aws = self.tf.provider("aws", {})
        instance = aws.data('instance', 'app1', { "filter": [{ "name": "image-id", "values": ["ami-xxxxxxx"] }] })
        aws.resource('route53_record', instance.name + '_dns', {
            "records": [instance.ref('public_ip')]
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }],
            "data": {
                "aws_instance": {
                    "app1": {
                        "filter": [{
                            "name": "image-id",
                            "values": ["ami-xxxxxxx"]
                        }]
                    }
                }
            },
            "resource": {
                "aws_route53_record": {
                    "app1_dns": {
                        "records": ["${data.aws_instance.app1.public_ip}"]
                    }
                }
            },
            "output": {}
        })


    def test_data_source_name_reuse_in_properties(self):
        aws = self.tf.provider("aws", {})
        aws.data('instance', 'app1', lambda data_source: { "name": data_source.name })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }],
            "data": {
                "aws_instance": {
                    "app1": {
                        "name": "app1"
                    }
                }
            },
            "resource": {},
            "output": {}
        })


    def test_duplicate_data_sources(self):
        aws = self.tf.provider("aws", {})
        aws.data('instance', 'app1', {})

        self.assertRaises(DuplicateDataSourceException, lambda: aws.data('instance', 'app1', {}))
