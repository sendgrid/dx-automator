import React, { Component } from 'react';
import { PageHeader, PageHeading, Divider,
  DropdownButton, Card, Tab, Tabs} from "@sendgrid/ui-components";
import axios from 'axios';


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
          <PageHeader>
            <PageHeading title="DX-automator">
              <DropdownButton label="Settings" type="secondary" icon="gear">
                <a>Work</a>
                <a>in</a>
                <a>Progress</a>
              </DropdownButton>
            </PageHeading>
          </PageHeader>
          <Divider id="divider"/>
        </div>

        <div className="Body">
          <Tabs id="Tabs" zeroBorder centered>
            <Tab active>Tasks</Tab>
            <Tab>Coming</Tab>
            <Tab>Soon</Tab>
          </Tabs>
          <div className="list">
            <div className="col-8" >
              { this.state.tasks.map((task) => {
                return(<Card id="tasks-card" key={task.id} body={task.link}/>)
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App; 
