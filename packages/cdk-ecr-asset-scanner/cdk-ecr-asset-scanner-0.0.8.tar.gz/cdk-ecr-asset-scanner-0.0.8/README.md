# CDK ECR Asset Scanner

The CDK ECR Asset Scanner is a custom L3 `ScannedDockerImageAsset` construct that builds and uploads your container image assets to ECR. After pushing, it will return the vulnerability report status in a Stack Output. In that way, it gives crucial and important security related information directly back to the engineer working with the stack. It aims to improve security insight while working with AWS CDK.

As stated before, `ScannedDockerImageAsset` is a custom L3 construct in the AWS Construct Library that combines the following L2 Constructs:

* DockerImageAsset
* A Custom Resource backed by a Lambda function
* Stack outputs

Because it just combines existing Constructs, this means the `ScannedDockerImageAsset` is a very stable L3 construct, not deemed experimental.

![Terminal](./docs/assets/terminal_output.png)

## USAGE

Run `npm i cdk-ecr-asset-scanner`.

Just add the `ScannedDockerImageAsset` to your imports, and use it exactly like you would a normal `DockerImageAsset`. It will do all the heavy lifting under the hood by itself. Make sure cdk peer dependencies are correct as usual, but npm will point those out (> 1.118.0 cdk versions)

Example (ts):

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_ecr_asset_scanner import ScannedDockerImageAsset
import path as path

env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

app = cdk.App()

class TestStack(cdk.Stack):
    def __init__(self, scope, id, props=None):
        super().__init__(scope, id, props)

        # Image without scan
        # const image3 = new DockerImageAsset(this, "zzz", {
        #   directory: path.join(__dirname, "../src/"),
        # });

        # Image with scan
        image = ScannedDockerImageAsset(self, "zzz",
            directory=path.join(__dirname, "../src/")
        )
        image3 = ecs.ContainerImage.from_docker_image_asset(image)

        task_definition = ecs.FargateTaskDefinition(self, "test-task-definition",
            memory_limit_mi_b=2048,
            cpu=1024
        )
        task_definition.add_container("container_example_three",
            image=image3,
            environment={
                "TEST_VAR": "THREE"
            },
            logging=ecs.AwsLogDriver(
                stream_prefix="three"
            )
        )
TestStack(app, "hh-stack", env=env)
```

## Availability

* Typescript / JS
* Python
