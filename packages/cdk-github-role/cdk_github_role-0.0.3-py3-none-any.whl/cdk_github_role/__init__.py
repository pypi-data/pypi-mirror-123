'''
# GitHub IAM Role

> An AWS CDK construct which defines an IAM Role that can be assumed by a GitHub
> Workflow.

## Usage

### GitHub OIDC Provider

In order to define the IAM Role, you'll first need to create an OIDC provider
for GitHub in your account.

These are the settings for the GitHub OIDC provider. You can create the provider
through the AWS IAM console or using the `GitHubOidcProvider` construct as
demonstrated below:

Settings:

* URL: `https://token.actions.githubusercontent.com`
* Client IDs: `sigstore`
* Thumbprints: `a031c46782e6e6c662c2c87c76da9aa62ccabd8e`

Or via CDK:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_github_role import GitHubOidcProvider
from aws_cdk.core import App, Stack

app = App()
stack = Stack(app, "GitHubOidcProviderStack")
GitHubOidcProvider(stack, "GitHubOidcProvider")

app.synth()
```

### IAM Roles for Repositories

Then, you can create an IAM role that grants a specific GitHub repository
certain permissions in the account. Use `GitHubOidcProvider.forAccount()` to
obtain a reference to the singleton provider.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_github_role import GithubRole

# must exist in advance.
provider = GitHubOidcProvider.for_account()

bar_role = GitHubRole(self, "GitHubFooBarRole",
    provider=provider,
    repository="foo/bar",
    role_name="FooBarGitHubRole"
)

goo_role = GitHubRole(self, "GitHubFooGooRole",
    provider=provider,
    repository="foo/goo",
    role_name="GitHubFooGooRole"
)

# now we can grant it permissions. for example:
bucket.grant_read(bar_role)
bucket.grant_write(goo_role)
```

To assume this role from a GitHub Workflow, add the
[aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
GitHub action step to your workflow:

```yaml
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@9aaa1daa91b40ce855e24cd45fb39b2ca18aeaf1
        with:
          aws-region: us-east-2
          role-to-assume: arn:aws:iam::123456789100:role/FooBarGitHubRole
          role-session-name: MySessionName
```

This step will obtain temporary credentials for this role in your AWS account.

## Security

See [Security Issues](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This project is licensed under the Apache-2.0 License.
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

import aws_cdk.aws_iam
import aws_cdk.core


class GitHubRole(
    aws_cdk.aws_iam.Role,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github-role.GitHubRole",
):
    '''Creates an IAM role that can be assumed by GitHub workflows.

    Use the ``aws-actions/configure-aws-credentials`` GitHub action and specify
    only ``role-to-assume`` in order to assume this role from a GitHub workflow.

    :see: https://github.com/aws-actions/configure-aws-credentials#assuming-a-role
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        provider: "IGitHubOidcProvider",
        repository: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param provider: The singleton instance of the GitHub OIDC provider deployed to this account. You will need to separately provision a single instance of ``GitHubOidcProvider`` to the account and then use ``GitHubOidcProvider.forAccount(this)`` to retrieve a reference to this provider.
        :param repository: The full name of the GitHub repository (e.g. ``myaccount/myrepo``).
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        props = GitHubRoleProps(
            provider=provider,
            repository=repository,
            description=description,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-github-role.GitHubRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "provider": "provider",
        "repository": "repository",
        "description": "description",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class GitHubRoleProps:
    def __init__(
        self,
        *,
        provider: "IGitHubOidcProvider",
        repository: builtins.str,
        description: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[aws_cdk.aws_iam.IManagedPolicy]] = None,
        max_session_duration: typing.Optional[aws_cdk.core.Duration] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[aws_cdk.aws_iam.IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Props for ``GitHubRole``.

        :param provider: The singleton instance of the GitHub OIDC provider deployed to this account. You will need to separately provision a single instance of ``GitHubOidcProvider`` to the account and then use ``GitHubOidcProvider.forAccount(this)`` to retrieve a reference to this provider.
        :param repository: The full name of the GitHub repository (e.g. ``myaccount/myrepo``).
        :param description: A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_ids: List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "provider": provider,
            "repository": repository,
        }
        if description is not None:
            self._values["description"] = description
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def provider(self) -> "IGitHubOidcProvider":
        '''The singleton instance of the GitHub OIDC provider deployed to this account.

        You will need to separately provision a single instance of
        ``GitHubOidcProvider`` to the account and then use
        ``GitHubOidcProvider.forAccount(this)`` to retrieve a reference to this
        provider.

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            GitHubOidcProvider.for_account(self)
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast("IGitHubOidcProvider", result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The full name of the GitHub repository (e.g. ``myaccount/myrepo``).'''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]]:
        '''A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, aws_cdk.aws_iam.PolicyDocument]], result)

    @builtins.property
    def managed_policies(
        self,
    ) -> typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]]:
        '''A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[aws_cdk.aws_iam.IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[aws_cdk.aws_iam.IManagedPolicy]:
        '''AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-github-role.IGitHubOidcProvider")
class IGitHubOidcProvider(typing_extensions.Protocol):
    '''Represents a GitHub OIDC provider.'''

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''The ARN of the OIDC provider.'''
        ...


class _IGitHubOidcProviderProxy:
    '''Represents a GitHub OIDC provider.'''

    __jsii_type__: typing.ClassVar[str] = "cdk-github-role.IGitHubOidcProvider"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''The ARN of the OIDC provider.'''
        return typing.cast(builtins.str, jsii.get(self, "providerArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitHubOidcProvider).__jsii_proxy_class__ = lambda : _IGitHubOidcProviderProxy


@jsii.implements(IGitHubOidcProvider)
class GitHubOidcProvider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-github-role.GitHubOidcProvider",
):
    '''Defines an OIDC provider for GitHub workflows.

    This provider can be
    '''

    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="forAccount") # type: ignore[misc]
    @builtins.classmethod
    def for_account(
        cls,
        account: typing.Optional[builtins.str] = None,
    ) -> IGitHubOidcProvider:
        '''
        :param account: The AWS account for which you want to obtain the OIDC provider. If not specified, we will use the current account.

        :return: The singleton GitHub OIDC provider for an account.
        '''
        return typing.cast(IGitHubOidcProvider, jsii.sinvoke(cls, "forAccount", [account]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="DOMAIN")
    def DOMAIN(cls) -> builtins.str:
        '''The OIDC domain for GitHub.'''
        return typing.cast(builtins.str, jsii.sget(cls, "DOMAIN"))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="THUMBPRINT")
    def THUMBPRINT(cls) -> builtins.str:
        '''The OIDC domain thumbprint for GitHub.'''
        return typing.cast(builtins.str, jsii.sget(cls, "THUMBPRINT"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="providerArn")
    def provider_arn(self) -> builtins.str:
        '''The ARN of the OIDC provider.'''
        return typing.cast(builtins.str, jsii.get(self, "providerArn"))


__all__ = [
    "GitHubOidcProvider",
    "GitHubRole",
    "GitHubRoleProps",
    "IGitHubOidcProvider",
]

publication.publish()
