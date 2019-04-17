import React, { Component } from "react";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import axios from "axios";
import ContentClassTabs from "./components/ContentClassTabs";
import TasksList from "./components/TasksList";
import AddTask from "./components/AddTask";
import Header from "./components/Header";
import UnlabeledIssueList from "./components/UnlabeledIssueList"
import BugsList from "./components/BugsList"
import { timingSafeEqual } from "crypto";
import update from 'immutability-helper';

class App extends Component {
  constructor() {
    super();
    this.state = {
      tasks: [],
      unlabeled_issues: //[],
      {
      'sendgrid-nodejs':[],
      'sendgrid-csharp':[],
      'sendgrid-php':[],
      'sendgrid-python':[],
      'sendgrid-java':[],
      'sendgrid-go':[],
      'sendgrid-ruby':[],
      'smtpapi-nodejs':[],
      'smtpapi-go':[],
      'smtpapi-python':[],
      'smtpapi-php':[],
      'smtpapi-csharp':[],
      'smtpapi-java':[],
      'smtpapi-ruby':[],
      'sendgrid-oai':[],
      'open-source-library-data-collector':[],
      'python-http-client':[],
      'php-http-client':[],
      'csharp-http-client':[],
      'java-http-client':[],
      'ruby-http-client':[],
      'rest':[],
      'nodejs-http-client':[],
      'dx-automator':[]},
      bugs: //[]
      {
        'sendgrid-nodejs':[],
        'sendgrid-csharp':[],
        'sendgrid-php':[],
        'sendgrid-python':[],
        'sendgrid-java':[],
        'sendgrid-go':[],
        'sendgrid-ruby':[],
        'smtpapi-nodejs':[],
        'smtpapi-go':[],
        'smtpapi-python':[],
        'smtpapi-php':[],
        'smtpapi-csharp':[],
        'smtpapi-java':[],
        'smtpapi-ruby':[],
        'sendgrid-oai':[],
        'open-source-library-data-collector':[],
        'python-http-client':[],
        'php-http-client':[],
        'csharp-http-client':[],
        'java-http-client':[],
        'ruby-http-client':[],
        'rest':[],
        'nodejs-http-client':[],
        'dx-automator':[]
      },
    };
    this.Triage = this.Triage.bind(this)
  }

  componentWillMount() {
    this.getTasks();
    this.getUnlabeledIssues();
    this.getBugs();
  };

  Home() {
    return <h2>Home</h2>
  }
  
  Triage() {
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
    const items = [];
    for (const [index, value] of all_repos.entries()) {
      // console.log(this.state.unlabeled_issues[value])
      items.push(
        <div key={index}>
        <h2>Unlabeled Issues - {value}</h2>
        <div className="Body" key={index*index + index + 2*all_repos.length}>
          <UnlabeledIssueList unlabeled_issues={this.state.unlabeled_issues[value]}/>
          {/* <UnlabeledIssueList unlabeled_issues={this.state.unlabeled_issues}/> */}
        </div>
        <h2>Bugs - {value}</h2>
        <div className="Body" key={index*index + 2*index + 3*all_repos.length}>
          <BugsList bugs={this.state.bugs[value]}/>
          {/* <BugsList bugs={this.state.bugs}/> */}
        </div>
        </div>
      )
    }

    return (<div>
              <h1>Triage</h1>
              {items}
            </div>)
  }

  
  // Adds a task to the db
  addTask = (creator, link) => {
    return axios.post(`${process.env.REACT_APP_TASKS_SERVICE_URL}`,
      {creator, link}).then((res) => {this.getTasks()})
      .catch((err) => { console.log(err); });
  };

  // Gets all the tasks in the db
  getTasks(){
    return axios.get(`${process.env.REACT_APP_TASKS_SERVICE_URL}`)
    .then((res) => {this.setState({tasks: res.data.data.tasks});})
    .catch((err) => { console.log(err); });
  };

  getUnlabeledIssues(){
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
      'dx-automator']
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value
      }})
      .then((res) => {
        // var newIssues = this.state.unlabeled_issues[value]
        // newIssues = res.data
        // var newIssues = this.state.unlabeled_issues[value]
          this.setState({unlabeled_issues: update(this.state.unlabeled_issues, {value: {$set: res.data}})});
          // this.setState({unlabeled_issues: res.data});
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
  }

  getBugs(){
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
      'dx-automator']
    for (const [index, value] of all_repos.entries()) {
      axios.get('http://192.168.99.100/github/issues',{
        params: {
          repo: value,
          labels: 'type: bug'
      }})
      .then((res) => {
        var newBugs = this.state.bugs
        console.log("before update: ")
        console.log(newBugs[value])
        newBugs[value] = res.data
        // this.setState({bugs: update(this.state.bugs, {value: {$set: newBugs}})});
        this.setState({bugs: newBugs})
        console.log("after update: ")
        console.log(this.state.bugs[value])
        // this.setState({unlabeled_issues: res.data});
      })
      .catch((err) => { 
          console.log(err); 
      });
    }
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
