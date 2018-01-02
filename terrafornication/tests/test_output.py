from unittest import TestCase

from terrafornication import Terrafornication, DuplicateOutputException

class TestTerrafornication(TestCase):
    
    def setUp(self):
        self.tf = Terrafornication()


    def test_output(self):
        elastic_ip = self.tf.resource('aws_eip', 'elastic_ip', {})

        foo = self.tf.output("ip", {
            "value": elastic_ip.ref("public_ip")
        })

        self.assertEqual(self.tf.to_dict(), {
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
