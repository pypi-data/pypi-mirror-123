# serverless-container-constructs

CDK patterns for modern application with serverless containers on AWS

# `AlbFargateServices`

Inspired by *Vijay Menon* from the [AWS blog post](https://aws.amazon.com/blogs/containers/how-to-use-multiple-load-balancer-target-group-support-for-amazon-ecs-to-access-internal-and-external-service-endpoint-using-the-same-dns-name/) introduced in 2019, `AlbFargateServices` allows you to create one or many fargate services with both internet-facing ALB and internal ALB associated with all services. With this pattern, fargate services will be allowed to intercommunicat via internal ALB while external inbound traffic will be spread across the same service tasks through internet-facing ALB.

The sample below will create 3 fargate services associated with both external and internal ALBs. The internal ALB will have an alias(`internal.svc.local`) auto-configured from Route 53 so services can communite through the private ALB endpoint.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from serverless_container_constructs import AlbFargateServices

AlbFargateServices(stack, "Service",
    spot=True, # FARGATE_SPOT only cluster
    tasks=[{
        "listener_port": 80,
        "task": order_task,
        "desired_count": 2,
        # customize the service autoscaling policy
        "scaling_policy": {
            "max_capacity": 20,
            "request_per_target": 1000,
            "target_cpu_utilization": 50
        }
    }, {"listener_port": 8080, "task": customer_task, "desired_count": 2}, {"listener_port": 9090, "task": product_task, "desired_count": 2}
    ],
    route53_ops={
        "zone_name": zone_name, # svc.local
        "external_alb_record_name": external_alb_record_name, # external.svc.local
        "internal_alb_record_name": internal_alb_record_name
    }
)
```

## Fargate Spot Support

By enabling the `spot` property, 100% fargate spot tasks will be provisioned to help you save up to 70%. Check more details about [Fargate Spot](https://aws.amazon.com/about-aws/whats-new/2019/12/aws-launches-fargate-spot-save-up-to-70-for-fault-tolerant-applications/?nc1=h_ls). This is a handy catch-all flag to force all tasks to be `FARGATE_SPOT` only.

To specify mixed strategy with partial `FARGATE` and partial `FARGATE_SPOT`, specify the `capacityProviderStrategy` for individual tasks like

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
AlbFargateServices(stack, "Service",
    tasks=[{
        "listener_port": 8080,
        "task": customer_task,
        "desired_count": 2,
        "capacity_provider_strategy": [{
            "capacity_provider": "FARGATE",
            "base": 1,
            "weight": 1
        }, {
            "capacity_provider": "FARGATE_SPOT",
            "base": 0,
            "weight": 3
        }
        ]
    }
    ]
)
```

The custom capacity provider strategy will be applied if `capacityProviderStretegy` is specified, otherwise, 100% spot will be used when `spot: true`. The default policy is 100% Fargate on-demand.

## ECS Exec

Simply turn on the `enableExecuteCommand` property to enable the [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html) support for all services.

## Internal or External Only

By default, all task(s) defined in the `AlbFargateServices` will be registered to both external and internal ALBs.
Set `accessibility` to make it internal only, external only, or both.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
AlbFargateServices(stack, "Service",
    tasks=[{"listener_port": 8080, "task": task1, "accessibility": LoadBalancerAccessibility.INTERNAL_ONLY}, {"listener_port": 8081, "task": task2, "accessibility": LoadBalancerAccessibility.EXTERNAL_ONLY}, {"listener_port": 8082, "task": task3}
    ]
)
```

Please note if all tasks are defined as `INTERNAL_ONLY`, no external ALB will be created. Similarly, no internal ALB
will be created if all defined as `EXTERNAL_ONLY`.

## VPC Subnets

By default, all tasks will be deployed in the private subnets. You will need the NAT gateway for the default route associated with the private subnets to ensure the task can successfully pull the container images.

However, you are allowed to specify `vpcSubnets` to customize the subnet selection.

To deploy all tasks in public subnets, one per AZ:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
AlbFargateServices(stack, "Service",
    vpc_subnets={
        "subnet_type": ec2.SubnetType.PUBLIC,
        "one_per_az": True
    }, ...
)
```

This will implicitly enable the `auto assign public IP` for each fargate task so the task can successfully pull the container images from external registry. However, the ingress traffic will still be balanced via the external ALB.

To deploy all tasks in specific subnets:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
AlbFargateServices(stack, "Service",
    vpc_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "sub-1a", "subnet-0e9460dbcfc4cf6ee"),
            ec2.Subnet.from_subnet_id(stack, "sub-1b", "subnet-0562f666bdf5c29af"),
            ec2.Subnet.from_subnet_id(stack, "sub-1c", "subnet-00ab15c0022872f06")
        ]
    }, ...
)
```

## Sample Application

This repository comes with a sample applicaiton with 3 services in Golang. On deployment, the `Order` service will be exposed externally on external ALB port `80` and all requests to the `Order` service will trigger sub-requests internally to another other two services(`product` and `customer`) through the internal ALB and eventually aggregate the response back to the client.

![](images/AlbFargateServices.svg)

## Deploy

To deploy the sample application in you default VPC:

```sh
// install first
yarn install
npx cdk diff -c use_default_vpc=1
npx cdk deploy -c use_default_vpc=1
```

On deployment complete, you will see the external ALB endpoint in the CDK output. `cURL` the external HTTP endpoint and you should be able to see the aggregated response.

```sh
$ curl http://demo-Servi-EH1OINYDWDU9-1397122594.ap-northeast-1.elb.amazonaws.com

{"service":"order", "version":"1.0"}
{"service":"product","version":"1.0"}
{"service":"customer","version":"1.0"}
```

## `cdk-nag` with `AwsSolutions` check

This construct follows the best practices from the [AWS Solutoins](https://github.com/cdklabs/cdk-nag/blob/main/RULES.md#awssolutions) with [cdk-nag](https://github.com/cdklabs/cdk-nag). Enable the `AWS_SOLUTIONS_CHECK` context variable to check aginst the cdk-nag rules.

```sh
npx cdk diff -c AWS_SOLUTIONS_CHECK=1
or
npx cdk synth -c AWS_SOLUTIONS_CHECK=1
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
