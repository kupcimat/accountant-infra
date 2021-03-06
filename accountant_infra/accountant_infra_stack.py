from aws_cdk import (
    aws_ec2 as ec2,
    aws_ecr as ecr,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications,
    aws_sqs as sqs,
    core as cdk,
)


class AccountantInfraStack(cdk.Stack):
    def __init__(
        self,
        scope: cdk.Construct,
        construct_id: str,
        repository_web: ecr.Repository,
        repository_worker: ecr.Repository,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SQS Queue
        queue = sqs.Queue(
            self,
            "accountant-worker-queue",
            queue_name="accountant-worker-queue",
            # TODO https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html#grant-destinations-permissions-to-s3
            # encryption=sqs.QueueEncryption.KMS_MANAGED,
            receive_message_wait_time=cdk.Duration.seconds(10),
            visibility_timeout=cdk.Duration.seconds(30),
        )

        # S3 buckets
        bucket_uploads = s3.Bucket(
            self,
            "accountant-document-uploads",
            bucket_name="accountant-document-uploads",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=cdk.RemovalPolicy.DESTROY,
            versioned=False,
        )
        bucket_uploads.add_object_created_notification(
            dest=s3_notifications.SqsDestination(queue)
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

        # Fargate services
        vpc = ec2.Vpc(self, "accountant-vpc", max_azs=3)

        cluster = ecs.Cluster(
            self, "accountant-cluster", cluster_name="accountant-cluster", vpc=vpc
        )

        service_web = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "accountant-web-service",
            service_name="accountant-web-service",
            cluster=cluster,
            desired_count=1,
            cpu=256,
            memory_limit_mib=512,
            public_load_balancer=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                family="accountant-web-task",
                image=ecs.ContainerImage.from_ecr_repository(repository_web),
                container_name="accountant-web-container",
                container_port=80,
                enable_logging=True,
            ),
        )
        # web permissions
        service_web_role = service_web.task_definition.task_role
        bucket_uploads.grant_put(service_web_role)
        bucket_uploads.grant_read(service_web_role)
        bucket_results.grant_read(service_web_role)

        service_worker = ecs_patterns.QueueProcessingFargateService(
            self,
            "accountant-worker-service",
            service_name="accountant-worker-service",
            cluster=cluster,
            desired_task_count=1,
            cpu=256,
            memory_limit_mib=512,
            queue=queue,
            family="accountant-worker-task",
            image=ecs.ContainerImage.from_ecr_repository(repository_worker),
            container_name="accountant-worker-container",
            enable_logging=True,
        )
        # worker permissions
        service_worker_role = service_worker.task_definition.task_role
        bucket_uploads.grant_read(service_worker_role)
        bucket_results.grant_put(service_worker_role)
