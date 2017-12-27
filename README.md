# terrafornication

Describe your infrastructure with terraform as python code.


## Why?

Terraform is a very nice tool, but the terraform configuration syntax is very limiting.
By writing code, you have full power of a programing language.


## How does it work?

Terraform supports JSON as an alternative template syntax, and terrafornication produces compatible JSON.

Terrafornication is a very small library and doesn't include any specific definitions for each cloud provider,
therefore it shouldn't need to change very often in the future.
