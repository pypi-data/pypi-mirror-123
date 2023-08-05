from cloudrail.knowledge.context.aws.resources_builders.terraform.aws_terraform_builder import AwsTerraformBuilder
from cloudrail.knowledge.context.aws.resources_builders.terraform.terraform_resource_builder_helper import build_kinesis_firehose_stream
from cloudrail.knowledge.context.aws.resources.service_name import AwsServiceName


class KinesisFirehoseStreamBuilder(AwsTerraformBuilder):
    def do_build(self, attributes):
        return build_kinesis_firehose_stream(attributes)

    def get_service_name(self) -> AwsServiceName:
        return AwsServiceName.AWS_KINESIS_FIREHOSE_DELIVERY_STREAM
