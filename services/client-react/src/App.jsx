import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import axios from "axios";
import Header from "./components/Header";
import IssuesList from "./components/IssuesList";
import { Divider } from "@sendgrid/ui-components";

const all_repos = [
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

class App extends Component {
  constructor() {
    super();
    let unlabeled_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let bugs_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let bugs_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let follow_ups_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let follow_ups_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let code_reviews_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let security_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    let security_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    this.state = {
      unlabeled_issues: unlabeled_issues_dict,
      bugs_issues: bugs_issues_dict,
      bugs_prs: bugs_prs_dict,
      followups_issues: follow_ups_issues_dict,
      followups_prs: follow_ups_prs_dict,
      codereviews: code_reviews_dict,
      securityiss_issues: security_issues_dict,
      securityiss_prs: security_prs_dict,
    };
    this.Triage = this.Triage.bind(this);
  }

  componentWillMount() {
    this.getUnlabeledIssues();
    this.getFollowUps();
    this.getBugs();
    this.getCodeReviews();
    this.getSecurityIssues();
  };

  Home() {
    return <h2>Home</h2>;
  }

  Triage() {
    const items = [];
    let num_unlabeled = 0;
    let num_bugs = 0;
    let num_followups = 0;
    let num_codereviews = 0;
    let num_securityiss = 0;
    const unlabeled_repos = [];
    const bug_issue_repos = [];
    const bug_pr_repos = [];
    const followup_issue_repos = [];
    const followup_pr_repos = [];
    const code_review_repos = [];
    const securityiss_issue_repos = [];
    const securityiss_pr_repos = [];

    for (const [index, value] of all_repos.entries()) {
      num_unlabeled += this.state.unlabeled_issues[value].length;
      num_bugs += this.state.bugs_issues[value].length + this.state.bugs_prs[value].length;
      num_followups += this.state.followups_issues[value].length + this.state.followups_prs[value].length;
      num_codereviews += this.state.codereviews[value].length;
      num_securityiss += this.state.securityiss_issues[value].length + this.state.securityiss_prs[value].length;

      if (num_unlabeled !== 0) {
        let unlab = "unlabeled-".concat(value);
        if(this.state.unlabeled_issues[value].length !== 0){
          unlabeled_repos.push(
            <a key={index} className="link" href={"#".concat(unlab)}>
            {value}: {this.state.unlabeled_issues[value].length}
            <br></br>
            </a>
          );
          items.push(
            <div key={index}>
            <h2>Unlabeled Issues - {value}</h2>
            <div id={unlab} className="Body" key={index*index + index + 2*all_repos.length}>
              <IssuesList issues={this.state.unlabeled_issues[value]}/>
            </div>
            </div>
          );
        }
      }

      let bug_issue_id = "bugs-issues-".concat(value);
      if(this.state.bugs_issues[value].length !== 0){
        bug_issue_repos.push(
          <a key={index.toString().concat('-issue')} className="link" href={"#".concat(bug_issue_id)}>
          {value}: {this.state.bugs_issues[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 3*index + 4*all_repos.length).toString().concat('-issue')}>
          <h2>Bugs Issues - {value}</h2>
          <div id={bug_issue_id} className="Body" key={(index*index + 2*index + 3*all_repos.length).toString().concat('-issue')}>
            <IssuesList issues={this.state.bugs_issues[value]}/>
          </div>
          </div>
        );
      }

      let bug_pr_id = "bugs-prs-".concat(value);
      if(this.state.bugs_prs[value].length !== 0){
        bug_pr_repos.push(
          <a key={index.toString().concat('-pr')} className="link" href={"#".concat(bug_pr_id)}>
          {value}: {this.state.bugs_prs[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 3*index + 4*all_repos.length).toString().concat('-pr')}>
          <h2>Bugs PRs - {value}</h2>
          <div id={bug_pr_id} className="Body" key={index*index + 2*index + 3*all_repos.length}>
            <IssuesList issues={this.state.bugs_prs[value]}/>
          </div>
          </div>
        );
      }

      let follow_issue_id = "followup-issues-".concat(value);
      if(this.state.followups_issues[value].length !== 0){
        followup_issue_repos.push(
          <a key={index.toString().concat('-issue')} className="link" href={"#".concat(follow_issue_id)}>
          {value}: {this.state.followups_issues[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 4*index + 5*all_repos.length).toString().concat('-issue')}>
          <h2>Follow Ups Issues - {value}</h2>
          <div id={follow_issue_id} className="Body" key={(index*index + 3*index + 4*all_repos.length).toString().concat('-issue')}>
            <IssuesList issues={this.state.followups_issues[value]}/>
          </div>
          </div>
        );
      }

      let follow_pr_id = "followup-prs-".concat(value);
      if(this.state.followups_prs[value].length !== 0){
        followup_pr_repos.push(
          <a key={index.toString().concat('-pr')} className="link" href={"#".concat(follow_pr_id)}>
          {value}: {this.state.followups_prs[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 4*index + 5*all_repos.length).toString().concat('-pr')}>
          <h2>Follow Ups Prs - {value}</h2>
          <div id={follow_pr_id} className="Body" key={(index*index + 3*index + 4*all_repos.length).toString().concat('-pr')}>
            <IssuesList issues={this.state.followups_prs[value]}/>
          </div>
          </div>
        );
      }

      let code_review_id = "coderev-".concat(value);
      if(this.state.codereviews[value].length !== 0){
        code_review_repos.push(
          <a key={index} className="link" href={"#".concat(code_review_id)}>
          {value}: {this.state.codereviews[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={index*index + 5*index + 6*all_repos.length}>
          <h2>Code Review Needed - {value}</h2>
          <div id={code_review_id} className="Body" key={index*index + 4*index + 5*all_repos.length}>
            <IssuesList issues={this.state.codereviews[value]}/>
          </div>
          </div>
        );
      }

      let securityiss_issue_id = "securityiss-issues-".concat(value);
      if(this.state.securityiss_issues[value].length !== 0){
        securityiss_issue_repos.push(
          <a key={index.toString().concat('-issue')} className="link" href={"#".concat(securityiss_issue_id)}>
          {value}: {this.state.securityiss_issues[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 6*index + 7*all_repos.length).toString().concat('-issue')}>
          <h2>Security Issues - {value}</h2>
          <div id={securityiss_issue_id} className="Body" key={(index*index + 5*index + 6*all_repos.length).toString().concat('-issue')}>
            <IssuesList issues={this.state.securityiss_issues[value]}/>
          </div>
          </div>
        );
      }

      let securityiss_pr_id = "securityiss-prs-".concat(value);
      if(this.state.securityiss_prs[value].length !== 0){
        securityiss_pr_repos.push(
          <a key={index.toString().concat('-pr')} className="link" href={"#".concat(securityiss_pr_id)}>
          {value}: {this.state.securityiss_prs[value].length}
          <br></br>
          </a>
        );
        items.push(
          <div key={(index*index + 6*index + 7*all_repos.length).toString().concat('-pr')}>
          <h2>Security PRs - {value}</h2>
          <div id={securityiss_pr_id} className="Body" key={(index*index + 5*index + 6*all_repos.length).toString().concat('-pr')}>
            <IssuesList issues={this.state.securityiss_prs[value]}/>
          </div>
          </div>
        );
      }
    }

    return (<div>
              <h1>Triage</h1>
              <Divider/>
              <h1>Summary</h1>
              <div id="summary">
              <div id="bugs">
              <div>Open Bugs: {num_bugs}</div>
              <br></br>
              <p>Issues</p>
              {bug_issue_repos}
              <br></br>
              <p>PRs</p>
              {bug_pr_repos}
              </div>

              <div id="unlabeled-issues">
              <div>Unlabeled Issues: {num_unlabeled}</div>
              <br></br>
              {unlabeled_repos}
              <br></br>
              </div>

              <div id = "follow-ups">
              <div>Follow Ups: {num_followups}</div>
              <br></br>
              <p>Issues</p>
              {followup_issue_repos}
              <br></br>
              <p>PRs</p>
              {followup_pr_repos}
              </div>

              <div id = "code-reviews">
              <div>Code Reviews: {num_codereviews}</div>
              <br></br>
              {code_review_repos}
              </div>

              <div id = "security-issues">
              <div>Security Issues: {num_securityiss}</div>
              <br></br>
              <p>Issues</p>
              {securityiss_issue_repos}
              <br></br>
              <p>PRs</p>
              {securityiss_pr_repos}
              </div>

              </div>

              <Divider/>
              {items}
            </div>);
  }

  getUnlabeledIssues() {
    let unlabeledIssues = this.createDictofReposWithEmptyArrays(all_repos);

    for (const repo of all_repos) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'issues',
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        let i = res.data.length;
        while (i--) {
            if (res.data[i].labels.length !== 0) {
              res.data.splice(i, 1);
            }
        }
        unlabeledIssues[repo] = res.data;
        this.setState({unlabeled_issues: unlabeledIssues});
      })
      .catch((err) => {
          console.log(err);
      });
    }
  }

  getBugs() {
    let issueBugs = this.createDictofReposWithEmptyArrays(all_repos);
    let prBugs = this.createDictofReposWithEmptyArrays(all_repos);

    for (const repo of all_repos) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'issues',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        issueBugs[repo] = res.data;
        this.setState({bugs_issues: issueBugs});
      })
      .catch((err) => {
          console.log(err);
      });

      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        prBugs[repo] = res.data;
        this.setState({bugs_prs: prBugs});
      })
      .catch((err) => {
          console.log(err);
      });
    }
  }

  getFollowUps() {
    let followups_issues = this.createDictofReposWithEmptyArrays(all_repos);
    let followups_prs = this.createDictofReposWithEmptyArrays(all_repos);

    for (const repo of all_repos) {
      axios.get('http://192.168.99.100/github/items', {
        params: {
          repo: repo,
          item_type: 'issues',
          states: ['OPEN'],
          limit: ['first', '100']
      }})
      .then(res => {
        followups_issues[repo] = res.data.filter(item => item['follow_up_needed']);
        this.setState({followups_issues});
      })
      .catch(err => {
          console.log(err);
      });

      axios.get('http://192.168.99.100/github/items', {
        params: {
          repo: repo,
          item_type: 'pull_requests',
          states: ['OPEN'],
          limit: ['first', '100']
      }})
      .then(res => {
        followups_prs[repo] = res.data.filter(item => item['follow_up_needed']);
          this.setState({followups_prs});
      })
      .catch(err => {
          console.log(err);
      });
    }
  }

  getCodeReviews() {
    let codeReviews = this.createDictofReposWithEmptyArrays(all_repos);

    for (const repo of all_repos) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['status: code review request'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        codeReviews[repo] = res.data;
        this.setState({codereviews: codeReviews});
      })
      .catch((err) => {
          console.log(err);
      });
    }
  }

  getSecurityIssues() {
    let issueSecurity = this.createDictofReposWithEmptyArrays(all_repos);
    let prSecurity = this.createDictofReposWithEmptyArrays(all_repos);

    for (const repo of all_repos) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'issues',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        issueSecurity[repo] = res.data;
        this.setState({securityiss_issues: issueSecurity});
      })
      .catch((err) => {
          console.log(err);
      });

      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: repo,
          item_type: 'pull_requests',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        prSecurity[repo] = res.data;
        this.setState({securityiss_prs: prSecurity});
      })
      .catch((err) => {
          console.log(err);
      });
    }
  }

  createDictofReposWithEmptyArrays(all_repos){
    let dict_of_repos = {};
    all_repos.forEach(function(repo) {
      dict_of_repos[repo] = [];
    });
    return dict_of_repos;
  }

  render() {
    return (
      <Router>
        <div className="App" id="app-maindiv">
          <div className="Header">
            <Header />
          </div>

          <Route exact path="/" component={this.Home} />
          <Route exact path="/triage" component={this.Triage} />

        </div>
      </Router>
    );
  }
}

export default App;
