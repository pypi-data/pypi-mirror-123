'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import monocdk
import monocdk.aws_ec2
import monocdk.aws_lambda
import monocdk.aws_s3
import monocdk.aws_secretsmanager


class FlywayConstruct(
    monocdk.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="flywaymigrationconstructmonocdk.FlywayConstruct",
):
    def __init__(
        self,
        scope: monocdk.Construct,
        id: builtins.str,
        *,
        bucket_migration_sql: monocdk.aws_s3.IBucket,
        migration_db_secret_manager: monocdk.aws_secretsmanager.ISecret,
        memory_size: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[monocdk.aws_ec2.ISecurityGroup]] = None,
        subnet: typing.Optional[monocdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[monocdk.Duration] = None,
        vpc: typing.Optional[monocdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_migration_sql: 
        :param migration_db_secret_manager: 
        :param memory_size: 
        :param security_groups: 
        :param subnet: 
        :param timeout: 
        :param vpc: 
        '''
        params = FlywayConstructParams(
            bucket_migration_sql=bucket_migration_sql,
            migration_db_secret_manager=migration_db_secret_manager,
            memory_size=memory_size,
            security_groups=security_groups,
            subnet=subnet,
            timeout=timeout,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, params])

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="BUCKET_CODE_ARN")
    def BUCKET_CODE_ARN(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "BUCKET_CODE_ARN"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="HANDLER")
    def HANDLER(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "HANDLER"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="ID_LAMBDA_CODE")
    def ID_LAMBDA_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ID_LAMBDA_CODE"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="flywayLambdaMigration")
    def flyway_lambda_migration(self) -> monocdk.aws_lambda.Function:
        return typing.cast(monocdk.aws_lambda.Function, jsii.get(self, "flywayLambdaMigration"))

    @flyway_lambda_migration.setter
    def flyway_lambda_migration(self, value: monocdk.aws_lambda.Function) -> None:
        jsii.set(self, "flywayLambdaMigration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="objectCodeKey")
    def object_code_key(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "objectCodeKey"))

    @object_code_key.setter
    def object_code_key(self, value: typing.Any) -> None:
        jsii.set(self, "objectCodeKey", value)


@jsii.data_type(
    jsii_type="flywaymigrationconstructmonocdk.FlywayConstructParams",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_migration_sql": "bucketMigrationSQL",
        "migration_db_secret_manager": "migrationDBSecretManager",
        "memory_size": "memorySize",
        "security_groups": "securityGroups",
        "subnet": "subnet",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class FlywayConstructParams:
    def __init__(
        self,
        *,
        bucket_migration_sql: monocdk.aws_s3.IBucket,
        migration_db_secret_manager: monocdk.aws_secretsmanager.ISecret,
        memory_size: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[monocdk.aws_ec2.ISecurityGroup]] = None,
        subnet: typing.Optional[monocdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[monocdk.Duration] = None,
        vpc: typing.Optional[monocdk.aws_ec2.IVpc] = None,
    ) -> None:
        '''
        :param bucket_migration_sql: 
        :param migration_db_secret_manager: 
        :param memory_size: 
        :param security_groups: 
        :param subnet: 
        :param timeout: 
        :param vpc: 
        '''
        if isinstance(subnet, dict):
            subnet = monocdk.aws_ec2.SubnetSelection(**subnet)
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_migration_sql": bucket_migration_sql,
            "migration_db_secret_manager": migration_db_secret_manager,
        }
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet is not None:
            self._values["subnet"] = subnet
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def bucket_migration_sql(self) -> monocdk.aws_s3.IBucket:
        result = self._values.get("bucket_migration_sql")
        assert result is not None, "Required property 'bucket_migration_sql' is missing"
        return typing.cast(monocdk.aws_s3.IBucket, result)

    @builtins.property
    def migration_db_secret_manager(self) -> monocdk.aws_secretsmanager.ISecret:
        result = self._values.get("migration_db_secret_manager")
        assert result is not None, "Required property 'migration_db_secret_manager' is missing"
        return typing.cast(monocdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[monocdk.aws_ec2.ISecurityGroup]]:
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[monocdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnet(self) -> typing.Optional[monocdk.aws_ec2.SubnetSelection]:
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[monocdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def timeout(self) -> typing.Optional[monocdk.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[monocdk.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[monocdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[monocdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FlywayConstructParams(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FlywayConstruct",
    "FlywayConstructParams",
]

publication.publish()
