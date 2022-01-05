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

### Action inputs

| Name                 | Description                                                                                                                          | Default      |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------|--------------|
| `changelog-filename` | Filename of the changelog file                                                                                                       | `CHANGES.md` |
| `footer`             | Custom release notes footer                                                                                                          |              |
| `assets`             | Space-separated list of assets to include with the release                                                                           |              |
| `token`              | `GITHUB_TOKEN` or a `repo` scoped [PAT](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) |              |
