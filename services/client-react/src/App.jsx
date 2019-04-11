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

class App extends Component {
  constructor() {
    super();
    this.state = {
      tasks: [],
      unlabeled_issues: [],
      bugs: [],
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
    return (<div>
              <h1>Triage</h1>
              <h2>Unlabled Issues - PHP</h2>
              <div className="Body">
                <UnlabeledIssueList unlabeled_issues={this.state.unlabeled_issues}/>
              </div>
              <h2>Bugs - PHP</h2>
              <div className="Body">
                <BugsList bugs={this.state.bugs}/>
              </div>
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
    axios.get('http://192.168.99.100/github/issues',{
      params: {
        repo: 'sendgrid-php'
    }})
    .then((res) => {
        this.setState({unlabeled_issues: res.data});
    })
    .catch((err) => { 
        console.log(err); 
    });
  }

  getBugs(){
    axios.get('http://192.168.99.100/github/issues',{
      params: {
        repo: 'sendgrid-php',
        labels: 'type: bug'
    }})
    .then((res) => {
        this.setState({bugs: res.data});
    })
    .catch((err) => { 
        console.log(err); 
    });
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
