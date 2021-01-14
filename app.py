#!/usr/bin/env python3

from aws_cdk import core

from accountant_infra.accountant_infra_stack import AccountantInfraStack


app = core.App()
AccountantInfraStack(app, "accountant-infra")

app.synth()
