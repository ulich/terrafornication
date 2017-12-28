# terrafornication

Describe your infrastructure with terraform as python code.


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
aws.resource("instance", "app1", {
    "ami": "ami-aa2ea6d0",
    "instance_type": "t2.micro"
})

print tf.to_json()
```

This writes the following json to stdout:
```json
{
    "resource": {
        "aws_instance": {
            "app1": {
                "ami": "ami-aa2ea6d0",
                "instance_type": "t2.micro"
            }
        }
    },
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
