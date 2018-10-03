import React from 'react';
import {PageHeader, PageHeading, Divider, DropdownButton} from "@sendgrid/ui-components"

const Header = () => {
  return (

    <PageHeader>
        <PageHeading title="DX-automator">
            <DropdownButton label="Settings" type="secondary" icon="gear">
            <a>Work</a>
            <a>in</a>
            <a>Progress</a>
            </DropdownButton>
        </PageHeading>
        <Divider id="divider"/>
    </PageHeader> 
  )
};

export default Header