from unittest import TestCase

from terrafornication import Terrafornication, DuplicateVariableException, DuplicateOutputException

class TestVariable(TestCase):
    
    def setUp(self):
        self.tf = Terrafornication()
    

    def test_variable(self):
        foo = self.tf.variable('foo', {
            "default": "bar"
        })

        self.tf.resource('aws_instance', 'app', {
            "ami": foo.ref()
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {
                "foo": {
                    "default": "bar"
                }
            },
            "resource": {
                "aws_instance": {
                    "app": {
                        "ami": "${var.foo}"
                    }
                }
            }
        })
    

    def test_duplicate_variable(self):
        self.tf.variable('foo', {})

        self.assertRaises(DuplicateVariableException, lambda: self.tf.variable('foo', {}))
