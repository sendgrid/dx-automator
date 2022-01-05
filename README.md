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
