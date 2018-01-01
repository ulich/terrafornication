from unittest import TestCase

import terrafornication
from terrafornication import DuplicateVariableException, DuplicateOutputException

class TestVariable(TestCase):
    
    def setUp(self):
        self.tf = terrafornication.Terrafornication()
    

    def test_variable(self):
        foo = self.tf.variable('foo', {
            "default": "bar"
        })

        aws = self.tf.provider("aws", {})
        aws.resource('instance', 'app', {
            "ami": foo.ref()
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {
                "foo": {
                    "default": "bar"
                }
            },
            "provider": [{
                "aws": {}
            }],
            "data": {},
            "resource": {
                "aws_instance": {
                    "app": {
                        "ami": "${var.foo}"
                    }
                }
            },
            "output": {}
        })
    

    def test_duplicate_variable(self):
        self.tf.variable('foo', {})

        with self.assertRaises(DuplicateVariableException):
            self.tf.variable('foo', {})
