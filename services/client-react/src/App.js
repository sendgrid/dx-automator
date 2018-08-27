import React, { Component } from 'react';
import { PageHeader, PageHeading, Button, Divider } from "@sendgrid/ui-components";
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <PageHeader>
          <PageHeading title="DX-automator">
            <Button type="primary" id="stui-test-locator-abc">
              Primary
            </Button>
          </PageHeading>
        </PageHeader>
        <Divider/>
      </div>
    );
  }
}

export default App; 
