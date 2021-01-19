from aws_cdk import (
    aws_ecr as ecr,
    core as cdk,
)


class AccountantReposStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECR repositories
        remove_old_images = ecr.LifecycleRule(
            description="Expire old images, keep 2 latest",
            rule_priority=1,
            max_image_count=2,
            tag_status=ecr.TagStatus.ANY,
        )
        self.repository_web = ecr.Repository(
            self,
            "accountant-web-repository",
            repository_name="accountant-web",
            lifecycle_rules=[remove_old_images],
        )
        self.repository_worker = ecr.Repository(
            self,
            "accountant-worker-repository",
            repository_name="accountant-worker",
            lifecycle_rules=[remove_old_images],
        )
