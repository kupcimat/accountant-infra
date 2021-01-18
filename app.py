#!/usr/bin/env python3

from aws_cdk import core

from accountant_infra.accountant_infra_stack import AccountantInfraStack
from accountant_infra.accountant_repos_stack import AccountantReposStack


app = core.App()
accountant_repos = AccountantReposStack(app, "accountant-repos")
accountant_infra = AccountantInfraStack(
    app,
    "accountant-infra",
    repository_web=accountant_repos.repository_web,
    repository_worker=accountant_repos.repository_worker,
)

app.synth()
