# The Developer Experience (DX) Automator

This tool is intended to help make managing multiple GitHub repositories much easier for DX, DevRel, and Open Source Engineering teams.

## Contributing

Everyone who participates in our repo is expected to comply with our [Code of Conduct](CODE_OF_CONDUCT.md).

We welcome [contributions](CONTRIBUTING.md) in the form of issues, pull requests and code reviews.

## Usage - Standalone Scripts

### Environment Setup

Update the development environment with your [GITHUB_TOKEN](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line), for example:

1. Copy the sample environment file to a new file: `cp .env_sample .env`
1. Edit the new `.env` to add your GitHub Personal Access Token
1. Source the `.env` file to set the variable in the current session: `source .env`

Install the python dependencies and activate the environment:

```bash
make install
source venv/bin/activate
```

### Running Scripts

```bash
python ./examples/action_items.py
python ./examples/metrics.py daily
python ./examples/metrics.py weekly
```
## Usage - Updating DataDog Monitors through Terraform
1. Open a PR that includes any relevant changes to `terraform_datadog_monitors.tf` located in the `terraform` directory
2. After your changes are approved, merge the PR to Main
3. Use the team's credentials to login to the Terraform-DI service account
4. Navigate to the [workspaces](app.terraform.io/app) tab.
5. Click on the [runs](https://app.terraform.io/app/Twilio-Developer-Interfaces/workspaces/dx-automator/runs) tab to verify that the changes to the monitors are made successful.
