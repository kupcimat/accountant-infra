from aws_cdk import aws_s3 as s3, core as cdk


class AccountantInfraStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket_uploads = s3.Bucket(
            self,
            "accountant-document-uploads",
            bucket_name="accountant-document-uploads",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            versioned=False,
        )
        bucket_results = s3.Bucket(
            self,
            "accountant-document-results",
            bucket_name="accountant-document-results",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            versioned=False,
        )
