# Actions

## GitHubRelease

A GitHub action to create or update a Release in GitHub.

### Usage

```yml
      - name: Create a release
        uses: sendgrid/dx-automator/actions/release@main
        with:
          changelog-filename: CHANGES.md
          footer: This is a custom footer
          assets: sendgrid-java.jar
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Action Inputs

| Name                 | Description                                                | Default                        |
|----------------------|------------------------------------------------------------|--------------------------------|
| `changelog-filename` | Filename of the changelog file                             | `CHANGES.md` or `CHANGELOG.md` |
| `footer`             | Custom release notes footer                                |                                |
| `assets`             | Space-separated list of assets to include with the release |                                |

The env var `GITHUB_TOKEN` must also be given which can be either `GITHUB_TOKEN` or a `repo`
-scoped [PAT](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token).

The `footer` input supports limited string parameter expansion. The table below lists the string literals and what they
will expand into.

| Literal      | Value                                                  |
|--------------|--------------------------------------------------------|
| `${version}` | The version of the release (i.e., the name of the tag) |

# Developing

## Requirements

* Node.js 12

## Contributing

Before submitting a pull request, run `npm run all` to build, format, lint, test the actions. This will also compile
each action into a single file which is required in order to run them in GitHub workflows. Failure to do so will result
in pull request check failures.
