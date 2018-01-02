# terrafornication &middot; [![Build Status](https://travis-ci.org/ulich/terrafornication.svg?branch=master)](https://travis-ci.org/ulich/terrafornication)

Describe your infrastructure with terraform as python code (tested with python 2.6, 2.7, 3.3, 3.4, 3.5, 3.6).


## Why?

Terraform is a very nice tool, but the terraform configuration syntax is very limiting.
By writing code, you have full power of a programming language.


## How does it work?

Terraform supports JSON as an alternative template syntax, and terrafornication produces compatible JSON.

Terrafornication is a small library and doesn't include any specific definitions for each cloud provider,
therefore it shouldn't need to change very often in the future.


## Example

```python
from terrafornication import Terrafornication

tf = Terrafornication()
aws = tf.provider("aws", { "region": "us-east-1" })

primary_zone = aws.resource("route53_zone", "primary", {
    "name": "example.com"
})

aws.resource("route53_record", "dev", {
    "zone_id": primary_zone.ref("zone_id"),
    "name": "dev",
    "type": "A",
    "ttl": "60",
    "records": ["1.2.3.4"]
})

print tf.to_json()
```

This writes the following json to stdout:
```json
{
    "resource": {
        "aws_route53_zone": {
            "primary": {
                "name": "example.com"
            }
        },
        "aws_route53_record": {
            "dev": {
                "records": ["1.2.3.4"],
                "ttl": "60",
                "type": "A",
                "zone_id": "${aws_route53_zone.primary.zone_id}",
                "name": "dev"
            }
        }
    },
    "data": {},
    "provider": [
        {
            "aws": {
                "region": "us-east-1"
            }
        }
    ]
}
```

Now write the json to a file with a `.tf.json` extension and then run
```
terraform init
terraform apply
```
