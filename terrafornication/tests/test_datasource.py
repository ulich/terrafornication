from unittest import TestCase

from terrafornication import Terrafornication, DuplicateDataSourceException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = Terrafornication()


    def test_data_sources(self):
        instance = self.tf.data('aws_instance', 'app1', { "filter": [{ "name": "image-id", "values": ["ami-xxxxxxx"] }] })
        self.tf.resource('aws_route53_record', instance.name + '_dns', {
            "records": [instance.ref('public_ip')]
        })

        self.assertEqual(self.tf.to_dict(), {
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
            }
        })


    def test_data_source_name_reuse_in_properties(self):
        self.tf.data('aws_instance', 'app1', lambda data_source: { "name": data_source.name })

        self.assertEqual(self.tf.to_dict(), {
            "data": {
                "aws_instance": {
                    "app1": {
                        "name": "app1"
                    }
                }
            }
        })


    def test_duplicate_data_sources(self):
        self.tf.data('aws_instance', 'app1', {})

        self.assertRaises(DuplicateDataSourceException, lambda: self.tf.data('aws_instance', 'app1', {}))
