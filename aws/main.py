import os
from os import environ
from typing import cast

from aws_cdk.aws_iam import ServicePrincipal, Role, IPrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode, AssetImageCodeProps
from aws_cdk.core import Stack, Construct, App, Environment


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        role = Role(
            self,
            'LambdaRole',
            assumed_by=cast(IPrincipal, ServicePrincipal('lambda.amazonaws.com')),
            inline_policies={
                's3': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                's3:ListBucket',
                                's3:PutObject',
                                's3:GetObject',
                                's3:ListObjects'
                            ],
                            resources=[
                                'arn:aws:s3:::*'
                            ]
                        )
                    ]
                ),
                'lambda': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=['lambda:InvokeFunction'],
                            resources=['arn:aws:lambda:*:*:function:*']
                        )
                    ]
                ),
                'logs': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                'logs:CreateLogGroup',
                                'logs:CreateLogStream',
                                'logs:PutLogEvents'
                            ],
                            resources=['*']
                        )
                    ]
                )
            }
        )
        DockerImageFunction(
            self,
            'Function',
            code=DockerImageCode.from_image_asset(
                directory=os.getcwd(),
                file='Dockerfile',
                exclude=['cdk.out']
            ),
            role=role,
            environment={}
        )
        # CfnFunction(
        #     self,
        #     'Function',
        #     code_uri='.build',
        #     handler='src.main.lambda_handler',
        #     runtime='python3.8',
        #     role=role.role_arn,
        #     events={
        #         'Get': CfnFunction.EventSourceProperty(
        #             type='Api',
        #             properties=CfnFunction.ApiEventProperty(
        #                 method='get',
        #                 path='/{proxy+}'
        #             )
        #         ),
        #         'Post': CfnFunction.EventSourceProperty(
        #             type='Api',
        #             properties=CfnFunction.ApiEventProperty(
        #                 method='post',
        #                 path='/{proxy+}'
        #             )
        #         )
        #     }
        # )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'JqbxBotDataService', env=Environment(region=environ.get('AWS_DEFAULT_REGION')))
    app.synth()
