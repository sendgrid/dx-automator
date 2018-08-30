import React, { Component } from 'react';
import axios from 'axios';
import ContentClassTabs from "./components/ContentClassTabs";
import TasksList from "./components/TasksList";
import AddTask from "./components/AddTask";
import Header from "./components/Header";

class App extends Component {
  constructor() {
    super();
    this.state = {
      tasks: []
    };
  }

  componentDidMount() {
    this.getTasks();
  };

  // Adds a task to the db
  addTask = (creator, link) => {
    return axios.post(`${process.env.REACT_APP_TASKS_SERVICE_URL}/tasks`,
      {creator, link}).then((res) => {this.getTasks()})
      .catch((err) => { console.log(err); });
  };

  // Gets all the tasks in the db
  getTasks(){
    return axios.get(`${process.env.REACT_APP_TASKS_SERVICE_URL}/tasks`)
    .then((res) => {this.setState({tasks: res.data.data.tasks});})
    .catch((err) => { console.log(err); });
  };

  render() {
    return (
      <div className="App" id="app-maindiv">
        {/* Header with the title and settings button */}
        <div className="Header">
          <Header/>
        </div>

        {/* DX-automator's category tabs */}
        <div className="ContentClassTabs" id="tabs-container">
          <ContentClassTabs/>
          <div id="add-task-button-conatiner">
          {/* TODO: define dynamic input fields */}
            <AddTask call={this.addTask}/>
          </div>
        </div>

        {/* Body with all the content */}
        <div className="Body">
          <TasksList tasks={this.state.tasks}/>
        </div>
      </div>
    );
  }
}

export default App; 
