from unittest import TestCase

import terrafornication
from terrafornication import DuplicateVariableException, DuplicateOutputException
from terrafornication.provider import DuplicateResourceException, DuplicateDataSourceException

class TestTerrafornication(TestCase):
    
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


    def test_multiple_providers_with_aliases(self):
        aws = self.tf.provider("aws", {})
        aws2 = self.tf.provider("aws", { "alias": "provider2" })

        aws.resource('instance', 'app1', {})
        aws2.resource('instance', 'app2', {})

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }, {
                "aws": {
                    "alias": "provider2"
                }
            }],
            "data": {},
            "resource": {
                "aws_instance": {
                    "app1": {},
                    "app2": {
                        "provider": "aws.provider2"
                    }
                }
            },
            "output": {}
        })


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

        with self.assertRaises(DuplicateDataSourceException):
            aws.data('instance', 'app1', {})


    def test_output(self):
        aws = self.tf.provider("aws", {})
        elastic_ip = aws.resource('eip', 'elastic_ip', {})

        foo = self.tf.output("ip", {
            "value": elastic_ip.ref("public_ip")
        })

        self.assertEqual(self.tf.to_dict(), {
            "variable": {},
            "provider": [{
                "aws": {}
            }],
            "data": {},
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

        with self.assertRaises(DuplicateOutputException):
            self.tf.output('foo', {})