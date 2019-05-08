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
    var bugs_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var follow_ups_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var code_reviews_dict = this.createDictofReposWithEmptyArrays(all_repos);
    var security_dict = this.createDictofReposWithEmptyArrays(all_repos);
    this.state = {
      // tasks: [],
      unlabeled_issues: unlabeled_issues_dict,
      bugs: bugs_dict,
      followups: follow_ups_dict,
      codereviews: code_reviews_dict,
      securityiss: security_dict,
    };
    this.Triage = this.Triage.bind(this)
  }

  componentWillMount() {
    // this.getTasks();
    this.getUnlabeledIssues();
    this.getBugs();
    this.getFollowUps();
    this.getCodeReviewed();
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
    const bug_repos = []
    const followup_repos = []
    const code_review_repos = []
    const securityiss_repos = []

    for (const [index, value] of all_repos.entries()) {
      num_unlabeled += this.state.unlabeled_issues[value].length
      num_bugs += this.state.bugs[value].length
      num_followups += this.state.followups[value].length
      num_codereviews += this.state.codereviews[value].length
      num_securityiss += this.state.securityiss[value].length

      if (this.state.unlabeled_issues[value].length !== 0) {
        var unlab = "unlabeled-".concat(value)
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

      if (this.state.bugs[value].length !== 0) {
        var bugid = "bugs-".concat(value)
        bug_repos.push(
          <a key={index} className="link" href={"#".concat(bugid)}>
          {value}: {this.state.bugs[value].length}
          <br></br>
          </a>
        )
        items.push(
          <div key={index*index + 3*index + 4*all_repos.length}>
          <h2>Bugs - {value}</h2>
          <div id={bugid} className="Body" key={index*index + 2*index + 3*all_repos.length}>
            <IssuesList issues={this.state.bugs[value]}/>
          </div>
          </div>
        )
      }

      if (this.state.followups[value].length !== 0) {
        var follow = "followup-".concat(value)
        followup_repos.push(
          <a key={index} className="link" href={"#".concat(follow)}>
          {value}: {this.state.followups[value].length}
          <br></br>
          </a>
        )
        items.push(
          <div key={index*index + 4*index + 5*all_repos.length}>
          <h2>Follow Ups - {value}</h2>
          <div id={follow} className="Body" key={index*index + 3*index + 4*all_repos.length}>
            <IssuesList issues={this.state.followups[value]}/>
          </div>
          </div>
        )
      }

      if (this.state.codereviews[value].length !== 0) {
        var follow = "coderev-".concat(value)
        code_review_repos.push(
          <a key={index} className="link" href={"#".concat(follow)}>
          {value}: {this.state.codereviews[value].length}
          <br></br>
          </a>
        )
        items.push(
          <div key={index*index + 5*index + 6*all_repos.length}>
          <h2>Code Review Needed - {value}</h2>
          <div id={follow} className="Body" key={index*index + 4*index + 5*all_repos.length}>
            <IssuesList issues={this.state.codereviews[value]}/>
          </div>
          </div>
        )
      }

      if (this.state.securityiss[value].length !== 0) {
        var follow = "securityiss-".concat(value)
        securityiss_repos.push(
          <a key={index} className="link" href={"#".concat(follow)}>
          {value}: {this.state.securityiss[value].length}
          <br></br>
          </a>
        )
        items.push(
          <div key={index*index + 6*index + 7*all_repos.length}>
          <h2>Security Issues - {value}</h2>
          <div id={follow} className="Body" key={index*index + 5*index + 6*all_repos.length}>
            <IssuesList issues={this.state.securityiss[value]}/>
          </div>
          </div>
        )
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
              {bug_repos}
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
              {followup_repos}
              </div>

              <div id = "code-reviews">
              <div>Code Reviews: {num_codereviews}</div>
              <br></br>
              {code_review_repos}
              </div>
              
              <div id = "security-issues">
              <div>Security Issues: {num_securityiss}</div>
              <br></br>
              {securityiss_repos}
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
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value
      }})
      .then((res) => {
        var newIssues = this.state.unlabeled_issues
        newIssues[value] = res.data
        this.setState({unlabeled_issues: newIssues})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getBugs(){
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value,
          labels: 'type: bug'
      }})
      .then((res) => {
        var newBugs = this.state.bugs
        newBugs[value] = res.data
        this.setState({bugs: newBugs})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getFollowUps(){
    const list_of_maintainers = [
      'aroach',
      'thinkingserious',
      'kylearoberts',
      'childish-sambino'
    ]
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value,
          labels: "status: waiting for feedback",
          states: "OPEN"
      }})
      .then((res) => {
        var newFollowUps = this.state.followups
        newFollowUps[value] = res.data
        var temp = []
        for (const [index2, value2] of newFollowUps[value].entries()){
          if (!list_of_maintainers.includes(value2['last_comment_author'])){
            temp.push(value2)
          }
        }
        newFollowUps[value] = temp
        this.setState({followups: newFollowUps})
      })
      .catch((err) => { 
          console.log(err); 
      });

      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value,
          labels: "status: waiting for feedback",
      }})
      .then((res) => {
        var newFollowUps = this.state.followups
        var temp1 = {0: []}
        temp1[0] = res.data
        var temp = []
        for (const [index2, value2] of temp1[0].entries()){
          if (!list_of_maintainers.includes(value2['last_comment_author'])){
            temp.push(value2)
          }
        }
        newFollowUps[value].concat(temp)
        this.setState({followups: newFollowUps})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getCodeReviewed() {
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/prs',{
        params: {
          repo: value,
          labels: "status: code review request",
          states:"OPEN"
      }})
      .then((res) => {
        var newIssues = this.state.codereviews
        newIssues[value] = res.data
        this.setState({codereviews: newIssues})
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getSecurityIssues() {
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value,
          labels: "type: security",
      }})
      .then((res) => {
        var newIssues = this.state.securityiss
        newIssues[value] = res.data
        this.setState({securityiss: newIssues})
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
