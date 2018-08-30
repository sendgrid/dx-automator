import React from 'react';
import {Tabs, Tab, Button} from "@sendgrid/ui-components"

const ContentClassTabs = () => {
  return (
    <Tabs id="tabs" zeroBorder centered>
        <Tab active>Tasks</Tab>
        <Tab>Coming</Tab>
        <Tab>Soon</Tab>
    </Tabs>
  )
};

export default ContentClassTabs