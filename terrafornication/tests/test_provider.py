from unittest import TestCase

from terrafornication import Terrafornication

class TestProvider(TestCase):
    
    def setUp(self):
        self.tf = Terrafornication()
    

    def test_no_provider(self):
        self.assertEqual(self.tf.to_dict(), {})

    
    def test_provider_resource(self):
        aws = self.tf.provider("aws", {})
        aws.resource('instance', 'app1', {})

        self.assertEqual(self.tf.to_dict(), {
            "provider": [{
                "aws": {}
            }],
            "resource": {
                "aws_instance": {
                    "app1": {}
                }
            }
        })
    

    def test_provider_data_source(self):
        aws = self.tf.provider("aws", {})
        aws.data('instance', 'app1', {})

        self.assertEqual(self.tf.to_dict(), {
            "provider": [{
                "aws": {}
            }],
            "data": {
                "aws_instance": {
                    "app1": {}
                }
            }
        })


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
