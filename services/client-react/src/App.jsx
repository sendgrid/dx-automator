import React, {Component} from "react";
import axios from "axios";
import Header from "./components/Header";
import IssuesList from "./components/IssuesList";
import {Divider} from "@sendgrid/ui-components";

const ALL_REPOS = [
  'sendgrid-nodejs',
  'sendgrid-csharp',
  'sendgrid-php',
  'sendgrid-python',
  'sendgrid-java',
  'sendgrid-go',
  'sendgrid-ruby',
  'smtpapi-nodejs',
  'smtpapi-go',
  'smtpapi-python',
  'smtpapi-php',
  'smtpapi-csharp',
  'smtpapi-java',
  'smtpapi-ruby',
  'sendgrid-oai',
  'open-source-library-data-collector',
  'python-http-client',
  'php-http-client',
  'csharp-http-client',
  'java-http-client',
  'ruby-http-client',
  'rest',
  'nodejs-http-client',
  'dx-automator'
];

const GITHUB_URL = 'http://192.168.99.100/github/items';

class App extends Component {
  constructor() {
    super();

    this.state = {
      unlabeled_issues: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      bugs_issues: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      bugs_prs: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      followups_issues: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      followups_prs: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      code_reviews: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      security_issues: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
      security_prs: this.createDictOfReposWithEmptyArrays(ALL_REPOS),
    };
  }

  componentWillMount() {
    this.getFollowUps();
    this.getUnlabeledIssues();
    this.getBugs();
    this.getCodeReviews();
    this.getSecurityIssues();
  };

  triage() {
    const items = [];
    let num_unlabeled = 0;
    let num_bugs = 0;
    let num_followups = 0;
    let num_code_reviews = 0;
    let num_security = 0;
    const unlabeled_repos = [];
    const bug_issue_repos = [];
    const bug_pr_repos = [];
    const followup_issue_repos = [];
    const followup_pr_repos = [];
    const code_review_repos = [];
    const security_issue_repos = [];
    const security_pr_repos = [];

    for (const repo of ALL_REPOS) {
      num_unlabeled += this.state.unlabeled_issues[repo].length;
      num_bugs += this.state.bugs_issues[repo].length + this.state.bugs_prs[repo].length;
      num_followups += this.state.followups_issues[repo].length + this.state.followups_prs[repo].length;
      num_code_reviews += this.state.code_reviews[repo].length;
      num_security += this.state.security_issues[repo].length + this.state.security_prs[repo].length;

      if (this.state.unlabeled_issues[repo].length > 0) {
        const unlabeled = "unlabeled-".concat(repo);
        unlabeled_repos.push(
          <a key={unlabeled} className="link" href={"#".concat(unlabeled)}>
            {repo}: {this.state.unlabeled_issues[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={unlabeled} key={unlabeled}>
            <h2>Unlabeled Issues - {repo}</h2>
            <IssuesList id={unlabeled} issues={this.state.unlabeled_issues[repo]}/>
          </div>
        );
      }

      if (this.state.bugs_issues[repo].length > 0) {
        const bug_issue_id = "bugs-issues-".concat(repo);
        bug_issue_repos.push(
          <a key={bug_issue_id} className="link" href={"#".concat(bug_issue_id)}>
            {repo}: {this.state.bugs_issues[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={bug_issue_id} key={bug_issue_id}>
            <h2>Bugs Issues - {repo}</h2>
            <IssuesList id={bug_issue_id} issues={this.state.bugs_issues[repo]}/>
          </div>
        );
      }

      if (this.state.bugs_prs[repo].length > 0) {
        const bug_pr_id = "bugs-prs-".concat(repo);
        bug_pr_repos.push(
          <a key={bug_pr_id} className="link" href={"#".concat(bug_pr_id)}>
            {repo}: {this.state.bugs_prs[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={bug_pr_id} key={bug_pr_id}>
            <h2>Bugs PRs - {repo}</h2>
            <IssuesList id={bug_pr_id} issues={this.state.bugs_prs[repo]}/>
          </div>
        );
      }

      if (this.state.followups_issues[repo].length > 0) {
        const follow_issue_id = "followup-issues-".concat(repo);
        followup_issue_repos.push(
          <a key={follow_issue_id} className="link" href={"#".concat(follow_issue_id)}>
            {repo}: {this.state.followups_issues[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={follow_issue_id} key={follow_issue_id}>
            <h2>Follow Ups Issues - {repo}</h2>
            <IssuesList id={follow_issue_id} issues={this.state.followups_issues[repo]}/>
          </div>
        );
      }

      if (this.state.followups_prs[repo].length > 0) {
        const follow_pr_id = "followup-prs-".concat(repo);
        followup_pr_repos.push(
          <a key={follow_pr_id} className="link" href={"#".concat(follow_pr_id)}>
            {repo}: {this.state.followups_prs[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={follow_pr_id} key={follow_pr_id}>
            <h2>Follow Ups Prs - {repo}</h2>
            <IssuesList id={follow_pr_id} issues={this.state.followups_prs[repo]}/>
          </div>
        );
      }

      if (this.state.code_reviews[repo].length > 0) {
        const code_review_id = "coderev-".concat(repo);
        code_review_repos.push(
          <a key={code_review_id} className="link" href={"#".concat(code_review_id)}>
            {repo}: {this.state.code_reviews[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={code_review_id} key={code_review_id}>
            <h2>Code Review Needed - {repo}</h2>
            <IssuesList id={code_review_id} issues={this.state.code_reviews[repo]}/>
          </div>
        );
      }

      if (this.state.security_issues[repo].length > 0) {
        const security_issue_id = "security-issues-".concat(repo);
        security_issue_repos.push(
          <a key={security_issue_id} className="link" href={"#".concat(security_issue_id)}>
            {repo}: {this.state.security_issues[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={security_issue_id} key={security_issue_id}>
            <h2>Security Issues - {repo}</h2>
            <IssuesList id={security_issue_id} issues={this.state.security_issues[repo]}/>
          </div>
        );
      }

      if (this.state.security_prs[repo].length > 0) {
        const security_pr_id = "security-prs-".concat(repo);
        security_pr_repos.push(
          <a key={security_pr_id} className="link" href={"#".concat(security_pr_id)}>
            {repo}: {this.state.security_prs[repo].length}
            <br/>
          </a>
        );
        items.push(
          <div id={security_pr_id} key={security_pr_id}>
            <h2>Security PRs - {repo}</h2>
            <IssuesList id={security_pr_id} issues={this.state.security_prs[repo]}/>
          </div>
        );
      }
    }

    return (
      <div>
        <h1>Triage</h1>
        <Divider/>
        <h1>Summary</h1>
        <div id="summary">

          <div id="bugs">
            <div>Open Bugs: {num_bugs}</div>
            <br/>
            <p>Issues</p>
            {bug_issue_repos}
            <br/>
            <p>PRs</p>
            {bug_pr_repos}
          </div>

          <div id="unlabeled-issues">
            <div>Unlabeled Issues: {num_unlabeled}</div>
            <br/>
            {unlabeled_repos}
            <br/>
          </div>

          <div id="follow-ups">
            <div>Follow Ups: {num_followups}</div>
            <br/>
            <p>Issues</p>
            {followup_issue_repos}
            <br/>
            <p>PRs</p>
            {followup_pr_repos}
          </div>

          <div id="code-reviews">
            <div>Code Reviews: {num_code_reviews}</div>
            <br/>
            {code_review_repos}
          </div>

          <div id="security">
            <div>Security Issues: {num_security}</div>
            <br/>
            <p>Issues</p>
            {security_issue_repos}
            <br/>
            <p>PRs</p>
            {security_pr_repos}
          </div>

        </div>

        <Divider/>
        {items}
      </div>
    );
  }

  getUnlabeledIssues() {
    const unlabeled_issues = this.createDictOfReposWithEmptyArrays(ALL_REPOS);

    for (const repo of ALL_REPOS) {
      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'issues',
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          unlabeled_issues[repo] = res.data.filter(item => item.labels.length === 0);
          this.setState({ unlabeled_issues });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  getBugs() {
    const bugs_issues = this.createDictOfReposWithEmptyArrays(ALL_REPOS);
    const bugs_prs = this.createDictOfReposWithEmptyArrays(ALL_REPOS);

    for (const repo of ALL_REPOS) {
      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'issues',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          bugs_issues[repo] = res.data;
          this.setState({ bugs_issues });
        })
        .catch(err => {
          console.log(err);
        });

      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          bugs_prs[repo] = res.data;
          this.setState({ bugs_prs });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  getFollowUps() {
    const followups_issues = this.createDictOfReposWithEmptyArrays(ALL_REPOS);
    const followups_prs = this.createDictOfReposWithEmptyArrays(ALL_REPOS);

    for (const repo of ALL_REPOS) {
      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'issues',
          states: ['OPEN'],
          limit: ['first', '100']
        }
      })
        .then(res => {
          followups_issues[repo] = res.data.filter(item => item['follow_up_needed']);
          this.setState({ followups_issues });
        })
        .catch(err => {
          console.log(err);
        });

      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'pull_requests',
          states: ['OPEN'],
          limit: ['first', '100']
        }
      })
        .then(res => {
          followups_prs[repo] = res.data.filter(item => item['follow_up_needed']);
          this.setState({ followups_prs });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  getCodeReviews() {
    const code_reviews = this.createDictOfReposWithEmptyArrays(ALL_REPOS);

    for (const repo of ALL_REPOS) {
      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['status: code review request'],
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          code_reviews[repo] = res.data;
          this.setState({ code_reviews });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  getSecurityIssues() {
    const security_issues = this.createDictOfReposWithEmptyArrays(ALL_REPOS);
    const security_prs = this.createDictOfReposWithEmptyArrays(ALL_REPOS);

    for (const repo of ALL_REPOS) {
      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'issues',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          security_issues[repo] = res.data;
          this.setState({ security_issues });
        })
        .catch(err => {
          console.log(err);
        });

      axios.get(GITHUB_URL, {
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
        }
      })
        .then(res => {
          security_prs[repo] = res.data;
          this.setState({ security_prs });
        })
        .catch(err => {
          console.log(err);
        });
    }
  }

  createDictOfReposWithEmptyArrays(all_repos) {
    const dict_of_repos = {};
    all_repos.forEach(function (repo) {
      dict_of_repos[repo] = [];
    });
    return dict_of_repos;
  }

  render() {
    return (
      <div id="app-maindiv">
        <div>
          <Header/>
        </div>
        {this.triage()}
      </div>
    );
  }
}

export default App;
