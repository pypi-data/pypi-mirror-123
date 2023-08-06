'''
# AWS Lambda function with Flyway

## Flyway --> Migrate/Evolve your database schema

Flyway is an opensource tool to easily evolve your db : https://flywaydb.org/

## Flyway Migration Construct

This AWS CDK construct allows you to scale your db schema with a lambda function.

The lambda function code is upload on S3 bucket "flywaymigrationconstruct". The construct retrieves the code on it according
to the version of the construct.

You must pass arguments, most of which are optional and are parameters of your lambda function except two of them,
which are environment variables.

warning: vpc, subnet and securitygroups are optional, but if one of them is provided, others must be too.

## Migration DB SecretManager

Migration DB SecretManager is the Secret of the DB you want to manage with Flyway.
It has to have 6 arguments :

username : the username of your DB

password : the password of your DB

engine : the type of your db (Redshift, Aurora MySQL, ...)

host: the host of your DB

port: the port of your DB

dbname: the name of your DB

## Bucket Migration SQL

Bucket Migration SQL is the S3 Bucket where you will put your SQL files
(warning : you have to comply with the naming pattern of Flyway).

## Enable in Python and TS (maybe more soon):

PyPI: https://pypi.org/project/flywaymigrationconstruct/

npmjs: https://www.npmjs.com/package/flywaymigrationconstruct

## NB :

Flyway Migration Construct manages the lambda function permissions for the secret and the bucket.

Warning : Version 0.3.0 only allows DB on Amazon Redshift, MySQL, PostgreSQL and SAP HANA.
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

import aws_cdk.aws_ec2
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class FlywayConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="flywaymigrationconstruct.FlywayConstruct",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket_migration_sql: aws_cdk.aws_s3.IBucket,
        migration_db_secret_manager: aws_cdk.aws_secretsmanager.ISecret,
        memory_size: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
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
    def flyway_lambda_migration(self) -> aws_cdk.aws_lambda.Function:
        return typing.cast(aws_cdk.aws_lambda.Function, jsii.get(self, "flywayLambdaMigration"))

    @flyway_lambda_migration.setter
    def flyway_lambda_migration(self, value: aws_cdk.aws_lambda.Function) -> None:
        jsii.set(self, "flywayLambdaMigration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="objectCodeKey")
    def object_code_key(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "objectCodeKey"))

    @object_code_key.setter
    def object_code_key(self, value: typing.Any) -> None:
        jsii.set(self, "objectCodeKey", value)


@jsii.data_type(
    jsii_type="flywaymigrationconstruct.FlywayConstructParams",
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
        bucket_migration_sql: aws_cdk.aws_s3.IBucket,
        migration_db_secret_manager: aws_cdk.aws_secretsmanager.ISecret,
        memory_size: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[aws_cdk.aws_ec2.ISecurityGroup]] = None,
        subnet: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
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
            subnet = aws_cdk.aws_ec2.SubnetSelection(**subnet)
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
    def bucket_migration_sql(self) -> aws_cdk.aws_s3.IBucket:
        result = self._values.get("bucket_migration_sql")
        assert result is not None, "Required property 'bucket_migration_sql' is missing"
        return typing.cast(aws_cdk.aws_s3.IBucket, result)

    @builtins.property
    def migration_db_secret_manager(self) -> aws_cdk.aws_secretsmanager.ISecret:
        result = self._values.get("migration_db_secret_manager")
        assert result is not None, "Required property 'migration_db_secret_manager' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]]:
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_ec2.ISecurityGroup]], result)

    @builtins.property
    def subnet(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

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
