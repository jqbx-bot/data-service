import os
from os import environ
from typing import cast

from aws_cdk.aws_apigateway import LambdaRestApi, CorsOptions
from aws_cdk.aws_iam import ServicePrincipal, Role, IPrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import DockerImageFunction, DockerImageCode
from aws_cdk.aws_s3 import Bucket
from aws_cdk.core import Stack, Construct, App, Environment


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        bucket = Bucket(self, 'Bucket')
        LambdaRestApi(
            self,
            'Api',
            default_cors_preflight_options=CorsOptions(
                allow_origins=['*']
            ),
            handler=DockerImageFunction(
                self,
                'Function',
                code=DockerImageCode.from_image_asset(directory=os.getcwd(), file='Dockerfile', exclude=['cdk.out']),
                environment={
                    'S3_BUCKET': bucket.bucket_name
                },
                role=Role(
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
                                        's3:DeleteObject',
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
            )
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'JqbxBotDataService', env=Environment(region=environ.get('AWS_DEFAULT_REGION')))
    app.synth()
