[![npm version](https://badge.fury.io/js/@pahud%2Fcdktf-aws-eks.svg)](https://badge.fury.io/js/@pahud%2Fcdktf-aws-eks)
[![PyPI version](https://badge.fury.io/py/pahud-cdktf-aws-eks.svg)](https://badge.fury.io/py/pahud-cdktf-aws-eks)
[![release](https://github.com/pahud/cdktf-aws-eks/actions/workflows/release.yml/badge.svg)](https://github.com/pahud/cdktf-aws-eks/actions/workflows/release.yml)
[![construct hub](https://img.shields.io/badge/Construct%20Hub-available-blue)](https://constructs.dev/packages/@pahud/cdktf-aws-eks)

# cdktf-aws-eks

CDKTF construct library for Amazon EKS.

## Usage

The following sample creates:

1. A new VPC
2. Amazon EKS cluster(control plane)
3. The default nodegroup with the cluster
4. The 2nd nodegroup with spot instances

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from pahud.cdktf_aws_eks import Cluster

# create the cluster and the default nodegroup
cluster = Cluster(stack, "demo-cluster",
    version=KubernetesVersion.V1_21,
    scaling_config={"min_capacity": 1}
)

# create the optional 2nd nodegroup
cluster.add_node_group("NG2",
    scaling_config={
        "min_capacity": 1,
        "max_capacity": 10,
        "desired_capacity": 5
    },
    capacity_type=CapacityType.SPOT,
    instance_types=["t3.large", "c5.large", "m5.large"]
)
```

## Existing VPC subnets

To deploy in any existing VPC, specify the `privateSubnets` and `publicSubnets`(if any).

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Cluster(stack, "demo-cluster",
    private_subnets=["subnet-111", "subnet-222", "subnet-333"],
    public_subnets=["subnet-444", "subnet-555", "subnet-666"],
    version=KubernetesVersion.V1_21
)
```
