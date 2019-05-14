import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import axios from "axios";
// import ContentClassTabs from "./components/ContentClassTabs";
// import TasksList from "./components/TasksList";
// import AddTask from "./components/AddTask";
import Header from "./components/Header";
import IssuesList from "./components/IssuesList"
// import { timingSafeEqual } from "crypto";
// import update from 'immutability-helper';
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
]

class App extends Component {
  constructor() {
    super();
    // this.main = React.createRef();
    var unlabeled_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var bugs_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var bugs_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var follow_ups_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var follow_ups_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var code_reviews_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var security_issues_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var security_prs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    this.state = {
      // tasks: [],
      unlabeled_issues: unlabeled_issues_dict,
      bugs_issues: bugs_issues_dict,
      bugs_prs: bugs_prs_dict,
      followups_issues: follow_ups_issues_dict,
      followups_prs: follow_ups_prs_dict,
      codereviews: code_reviews_dict,
      securityiss_issues: security_issues_dict,
      securityiss_prs: security_prs_dict,
    };
    this.Triage = this.Triage.bind(this)
  }

  componentWillMount() {
    // this.getTasks();
    this.getUnlabeledIssues();
    this.getBugs();
    this.getFollowUps();
    this.getCodeReviews();
    this.getSecurityIssues();
  };

  Home() {
    return <h2>Home</h2>
  }

  Triage() {
    const items = [];
    var num_unlabeled = 0
    var num_bugs = 0
    var num_followups = 0
    var num_codereviews = 0
    var num_securityiss = 0
    const unlabeled_repos = []
    const bug_issue_repos = []
    const bug_pr_repos = []
    const followup_issue_repos = []
    const followup_pr_repos = []
    const code_review_repos = []
    const securityiss_issue_repos = []
    const securityiss_pr_repos = []

    for (const [index, value] of all_repos.entries()) {
      num_unlabeled += this.state.unlabeled_issues[value].length
      num_bugs += this.state.bugs_issues[value].length + this.state.bugs_prs[value].length
      num_followups += this.state.followups_issues[value].length + this.state.followups_prs[value].length
      num_codereviews += this.state.codereviews[value].length
      num_securityiss += this.state.securityiss_issues[value].length + this.state.securityiss_prs[value].length

      if (num_unlabeled !== 0) {
        var unlab = "unlabeled-".concat(value)
        if(this.state.unlabeled_issues[value].length !== 0){
          unlabeled_repos.push(
            <a key={index} className="link" href={"#".concat(unlab)}>
            {value}: {this.state.unlabeled_issues[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={index}>
            <h2>Unlabeled Issues - {value}</h2>
            <div id={unlab}className="Body" key={index*index + index + 2*all_repos.length}>
              <IssuesList issues={this.state.unlabeled_issues[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_bugs !== 0) {
        var bug_issue_id = "bugs-issues-".concat(value)
        if(this.state.bugs_issues[value].length !== 0){
          bug_issue_repos.push(
            <a key={index.toString().concat('-issue')} className="link" href={"#".concat(bug_issue_id)}>
            {value}: {this.state.bugs_issues[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 3*index + 4*all_repos.length).toString().concat('-issue')}>
            <h2>Bugs Issues - {value}</h2>
            <div id={bug_issue_id} className="Body" key={(index*index + 2*index + 3*all_repos.length).toString().concat('-issue')}>
              <IssuesList issues={this.state.bugs_issues[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_bugs !== 0) {
        var bug_pr_id = "bugs-prs-".concat(value)
        if(this.state.bugs_prs[value].length !== 0){
          bug_pr_repos.push(
            <a key={index.toString().concat('-pr')} className="link" href={"#".concat(bug_pr_id)}>
            {value}: {this.state.bugs_prs[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 3*index + 4*all_repos.length).toString().concat('-pr')}>
            <h2>Bugs PRs - {value}</h2>
            <div id={bug_pr_id} className="Body" key={index*index + 2*index + 3*all_repos.length}>
              <IssuesList issues={this.state.bugs_prs[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_followups !== 0) {
        var follow_issue_id = "followup-issues-".concat(value)
        if(this.state.followups_issues[value].length !== 0){
          followup_issue_repos.push(
            <a key={index.toString().concat('-issue')} className="link" href={"#".concat(follow_issue_id)}>
            {value}: {this.state.followups_issues[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 4*index + 5*all_repos.length).toString().concat('-issue')}>
            <h2>Follow Ups Issues - {value}</h2>
            <div id={follow_issue_id} className="Body" key={(index*index + 3*index + 4*all_repos.length).toString().concat('-issue')}>
              <IssuesList issues={this.state.followups_issues[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_followups !== 0) {
        var follow_pr_id = "followup-prs-".concat(value)
        if(this.state.followups_prs[value].length !== 0){
          followup_pr_repos.push(
            <a key={index.toString().concat('-pr')} className="link" href={"#".concat(follow_pr_id)}>
            {value}: {this.state.followups_prs[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 4*index + 5*all_repos.length).toString().concat('-pr')}>
            <h2>Follow Ups Prs - {value}</h2>
            <div id={follow_pr_id} className="Body" key={(index*index + 3*index + 4*all_repos.length).toString().concat('-pr')}>
              <IssuesList issues={this.state.followups_prs[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_codereviews !== 0) {
        var code_review_id = "coderev-".concat(value)
        if(this.state.codereviews[value].length !== 0){
          code_review_repos.push(
            <a key={index} className="link" href={"#".concat(code_review_id)}>
            {value}: {this.state.codereviews[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={index*index + 5*index + 6*all_repos.length}>
            <h2>Code Review Needed - {value}</h2>
            <div id={code_review_id} className="Body" key={index*index + 4*index + 5*all_repos.length}>
              <IssuesList issues={this.state.codereviews[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_securityiss !== 0) {
        var securityiss_issue_id = "securityiss-issues-".concat(value)
        if(this.state.securityiss_issues[value].length !== 0){
          securityiss_issue_repos.push(
            <a key={index.toString().concat('-issue')} className="link" href={"#".concat(securityiss_issue_id)}>
            {value}: {this.state.securityiss_issues[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 6*index + 7*all_repos.length).toString().concat('-issue')}>
            <h2>Security Issues - {value}</h2>
            <div id={securityiss_issue_id} className="Body" key={(index*index + 5*index + 6*all_repos.length).toString().concat('-issue')}>
              <IssuesList issues={this.state.securityiss_issues[value]}/>
            </div>
            </div>
          )
        }
      }

      if (num_securityiss !== 0) {
        var securityiss_pr_id = "securityiss-prs-".concat(value)
        if(this.state.securityiss_prs[value].length !== 0){
          securityiss_pr_repos.push(
            <a key={index.toString().concat('-pr')} className="link" href={"#".concat(securityiss_pr_id)}>
            {value}: {this.state.securityiss_prs[value].length}
            <br></br>
            </a>
          )
          items.push(
            <div key={(index*index + 6*index + 7*all_repos.length).toString().concat('-pr')}>
            <h2>Security PRs - {value}</h2>
            <div id={securityiss_pr_id} className="Body" key={(index*index + 5*index + 6*all_repos.length).toString().concat('-pr')}>
              <IssuesList issues={this.state.securityiss_prs[value]}/>
            </div>
            </div>
          )
        }
      }

    }

    return (<div>
              <h1>Triage</h1>
              <Divider></Divider>
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

              <Divider></Divider>
              {items}
            </div>)
  }

  
  // // Adds a task to the db
  // addTask = (creator, link) => {
  //   return axios.post(`${process.env.REACT_APP_TASKS_SERVICE_URL}`,
  //     {creator, link}).then((res) => {this.getTasks()})
  //     .catch((err) => { console.log(err); });
  // };

  // // Gets all the tasks in the db
  // getTasks(){
  //   return axios.get(`${process.env.REACT_APP_TASKS_SERVICE_URL}`)
  //   .then((res) => {this.setState({tasks: res.data.data.tasks});})
  //   .catch((err) => { console.log(err); });
  // };

  getUnlabeledIssues(){
    var unlabeledIssues = this.createDictofReposWithEmptyArrays(all_repos);
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'issues',
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        var i = res.data.length
        while (i--) {
            if (res.data[i].labels.length !== 0) { 
              res.data.splice(i, 1);
            } 
        }
        unlabeledIssues[value] = res.data
        this.setState({unlabeled_issues: unlabeledIssues})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getBugs(){
    var issueBugs = this.createDictofReposWithEmptyArrays(all_repos);
    var prBugs = this.createDictofReposWithEmptyArrays(all_repos);
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'issues',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        issueBugs[value] = res.data
        this.setState({bugs_issues: issueBugs})
      })
      .catch((err) => { 
          console.log(err); 
      });

      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'pull_requests',
          labels: ['type: bug'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        prBugs[value] = res.data
        this.setState({bugs_prs: prBugs})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getFollowUps() {
    var issueFollowUps = this.createDictofReposWithEmptyArrays(all_repos);
    var prFollowUps = this.createDictofReposWithEmptyArrays(all_repos);
    const list_of_maintainers = [
      'aroach',
      'thinkingserious',
      'kylearoberts',
      'childish-sambino',
      'SendGridDX',
      'codecov'
    ]
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'issues',
          states: ['OPEN'],
          filter: "all",
          limit: ['first', '100']
      }})
      .then((res) => {
        var temp1 = {0: []}
        temp1[0] = res.data
        var temp = []
        for (const [index2, value2] of temp1[0].entries()){
          if (value2['last_comment_author'] && !list_of_maintainers.includes(value2['last_comment_author'])){
            temp.push(value2)
          }
        }
        issueFollowUps[value] = temp
        this.setState({followups_issues: issueFollowUps})
      })
      .catch((err) => { 
          console.log(err); 
      });

      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'pull_requests',
          states: ['OPEN'],
          limit: ['first', '100']
      }})
      .then((res) => {
        var temp1 = {0: []}
        temp1[0] = res.data
        var temp = []
        for (const [index2, value2] of temp1[0].entries()){
          if (value2['last_comment_author'] && !list_of_maintainers.includes(value2['last_comment_author'])){
            temp.push(value2)
          }
        }
        prFollowUps[value] = temp
        this.setState({followups_prs: prFollowUps})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getCodeReviews() {
    var codeReviews = this.createDictofReposWithEmptyArrays(all_repos);
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'pull_requests',
          labels: ['status: code review request'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        codeReviews[value] = res.data
        this.setState({codereviews: codeReviews})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getSecurityIssues() {
    var issueSecurity = this.createDictofReposWithEmptyArrays(all_repos);
    var prSecurity = this.createDictofReposWithEmptyArrays(all_repos);
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'issues',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        issueSecurity[value] = res.data
        this.setState({securityiss_issues: issueSecurity})
      })
      .catch((err) => { 
          console.log(err); 
      });

      axios.get('http://192.168.99.100/github/items',{
        params: {
          repo: value,
          item_type: 'pull_requests',
          labels: ['type: security'],
          states: ['OPEN'],
          limit: ['first', '100'],
      }})
      .then((res) => {
        prSecurity[value] = res.data
        this.setState({securityiss_prs: prSecurity})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  createDictofReposWithEmptyArrays(all_repos){
    var dict_of_repos = {}
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
      // <div className="App" id="app-maindiv">
      //   {/* Header with the title and settings button */}
      //   <div className="Header">
      //     <Header/>
      //   </div>

      //   {/* DX-automator's category tabs */}
      //   <div className="ContentClassTabs" id="tabs-container">
      //     <ContentClassTabs/>
      //     <div id="add-task-button-conatiner">
      //     {/* TODO: define dynamic input fields */}
      //       <AddTask call={this.addTask}/>
      //     </div>
      //   </div>

      //   {/* Body with all the content */}
      //   <div className="Body">
      //     <TasksList tasks={this.state.tasks}/>
      //   </div>
      // </div>
    );
  }
}

export default App; 
