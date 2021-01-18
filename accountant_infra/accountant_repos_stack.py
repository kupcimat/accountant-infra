from aws_cdk import (
    aws_ecr as ecr,
    core as cdk,
)


class AccountantReposStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECR repositories
        self.repository_web = ecr.Repository(
            self, "accountant-web-repository", repository_name="accountant-web"
        )
        self.repository_worker = ecr.Repository(
            self, "accountant-worker-repository", repository_name="accountant-worker"
        )
