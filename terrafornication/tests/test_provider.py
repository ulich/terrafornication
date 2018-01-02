from unittest import TestCase

import terrafornication

class TestProvider(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()
    

    def test_no_provider(self):
        self.assertEqual(self.tf.to_dict(), {})


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
