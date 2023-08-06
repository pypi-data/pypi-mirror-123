[![NPM version](https://badge.fury.io/js/cdk-demo-construct.svg)](https://badge.fury.io/js/cdk-demo-construct)
[![PyPI version](https://badge.fury.io/py/cdk-demo-construct.svg)](https://badge.fury.io/py/cdk-demo-construct)
![Release](https://github.com/neilkuan/cdk-demo-construct/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-demo-construct?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-demo-construct?label=pypi&color=blue)

# Welcome to `cdk-demo-construct`

The Constructs for the CDK Demo.

## To Use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_ec2 as ec2
import aws_cdk.core as cdk
from cdk_demo_construct import AlarmInstance
app = cdk.App()
stack = cdk.Stack(app, "integ-default")
vpc = ec2.Vpc(stack, "VPC")
AlarmInstance(stack, "AlarmInstance", vpc=vpc, notify_mail=["mail@example.com"])
```
