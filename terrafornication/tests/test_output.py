from unittest import TestCase

import terrafornication
from terrafornication import DuplicateOutputException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()


    def test_output(self):
        aws = self.tf.provider("aws", {})
        elastic_ip = aws.resource('eip', 'elastic_ip', {})

        foo = self.tf.output("ip", {
            "value": elastic_ip.ref("public_ip")
        })

        self.assertEqual(self.tf.to_dict(), {
            "provider": [{
                "aws": {}
            }],
            "resource": {
                "aws_eip": {
                    "elastic_ip": {}
                }
            },
            "output": {
                "ip": {
                    "value": "${aws_eip.elastic_ip.public_ip}"
                }
            }
        })
    

    def test_duplicate_output(self):
        self.tf.output('foo', {})

        self.assertRaises(DuplicateOutputException, lambda: self.tf.output('foo', {}))
