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
