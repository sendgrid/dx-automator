import React, { Component } from 'react';
import axios from 'axios';
import {Button, StatefulTextInput, ButtonList} from "@sendgrid/ui-components";
import ContentClassTabs from "./components/ContentClassTabs";
import TasksList from "./components/TasksList";
import ExampleContainer from "./components/AddTaskPopup";
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

  getTasks(){
    return axios.get(`${process.env.REACT_APP_TASKS_SERVICE_URL}/tasks`)
    .then((res) => {this.setState({tasks: res.data.data.tasks});})
    .catch((err) => { console.log(err); });
  };

  render() {
    return (
      <div className="App" id="app-maindiv">
        <div className="Header">
          <Header/>
        </div>

        <div className="ContentClassTabs" id="tabs-container">
          <ContentClassTabs/>
          <div id="add-task-button-conatiner">
            <Button type="primary" icon="create" >
              Add task
            </Button>
          </div>
        </div>

        <div className="Body">
        <ExampleContainer
          renderHeader="Add Task"
          // renderFooter={close => (
          //   <ButtonList>
          //     <Button small type="secondary" onClick={close}>
          //       Cancel
          //     </Button>
          //     <Button small type="primary" onClick={close}>
          //       Add
          //     </Button>
          //   </ButtonList>
            // )}
          />
          <TasksList tasks={this.state.tasks}/>
        </div>
      </div>
    );
  }
}

export default App; 
