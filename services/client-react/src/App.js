import React, { Component } from 'react';
import { PageHeader, PageHeading, Divider,
  DropdownButton, Card, Tab, Tabs} from "@sendgrid/ui-components";
import './App.css';

class App extends Component {
  getTasks(){
    // return axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
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
            <div className="col-8" id="tasks-card">
              <Card
              // body={this.getTasks}
              />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App; 
