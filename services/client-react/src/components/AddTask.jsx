import React, {Component} from 'react';
import {Button, CenterModal, ButtonList} from "@sendgrid/ui-components"
import { TextInput} from "@sendgrid/ui-components/text-input"

class AddTask extends Component {
    constructor() {
      super(...arguments);
      this.state = { 
        isOpen: false,
        creatorValue: "",
        linkValue: ""  
      };
      this.open = e => {
        this.setState({ isOpen: true });
      };
      this.close = e => {
        this.setState({ isOpen: false });
      };
      this.addCreator = e => {
        this.setState({ creatorValue: e.target.value});
      };
      this.addLink = e => {
        this.setState({ linkValue: e.target.value});
      };
      this.resetblanks = e => {
        this.setState({ creatorValue: "", linkValue: ""})
      };
    }

    renderBody() {
      // Create function for dynamic input boxes based off of custom table fields
      return (
        <form>
          <div className="field">
              <TextInput
                  type="text"
                  label="Creator"
                  isRequired={true}
                  id="test-input-simple"
                  value={this.state.creatorValue}
                  onChange={this.addCreator}
                  // onBlur={action("onBlur Called")}
              />
          </div>
          <div className="field">
              <TextInput
                  type="text"
                  label="Link"
                  isRequired={true}
                  id="test-input-simple"
                  value={this.state.linkValue}
                  onChange={this.addLink}
                  // onBlur={action("onBlur Called")}
              />
          </div>
        </form>
      )
    }

    render() {
      return (
        <div>
          <Button type="primary" icon="create" onClick={() => {
            this.resetblanks()
            this.open()
            }}>
            Add task
          </Button>
          <CenterModal
            padding={this.props.padding}
            large={this.props.large}
            hasX={this.props.hasX}
            onClose={this.close}
            open={this.state.isOpen}
            renderBody={this.renderBody(this.addCreator, this.addLink)}
            renderFooter={
              close => (
                <ButtonList>
                  <Button small type="secondary" onClick={this.close}>
                    Cancel
                  </Button>
                  <Button small type="primary" onClick={
                    () => {
                      this.props.call(this.state.creatorValue, this.state.linkValue);
                      this.close();
                    }
                  }>
                    Add
                  </Button>
                </ButtonList>
                )
            }
            renderHeader= "Add Task"
            data-role="example"
          />
        </div>
      );
    }
  }

  export default AddTask
