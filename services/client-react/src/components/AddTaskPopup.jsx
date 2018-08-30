import {React, Component} from 'react';
import {Button, CenterModal} from "@sendgrid/ui-components"

class ExampleContainer extends Component {
    constructor() {
      super(...arguments);
      this.state = { isOpen: true };
      this.open = e => {
        this.setState({ isOpen: true });
      };
      this.close = e => {
        this.setState({ isOpen: false });
      };
    }
    render() {
      return (
        <div>
          <Button type="primary" onClick={this.open}>
            Open Modal
          </Button>
          {/* <CenterModal
            padding={this.props.padding}
            large={this.props.large}
            hasX={this.props.hasX}
            onClose={this.close}
            open={this.state.isOpen}
            renderBody={this.props.renderBody}
            renderFooter={
              this.props.renderFooter
                ? () => this.props.renderFooter(this.close)
                : null
            }
            renderHeader={this.props.renderHeader}
            data-role="example"
          /> */}
        </div>
      );
    }
  }

  export default ExampleContainer
    // <ExampleContainer
    //   renderHeader="Add Task"
    //   renderBody={() => (
    //     <form>
    //     <div className="field">
    //         <StatefulTextInput
    //             type="text"
    //             label="Creator"
    //             isRequired={true}
    //             id="test-input-simple"
    //             onChange={action("Input Changed")}
    //             onBlur={action("onBlur Called")}
    //         />
    //     </div>
    //     <div className="field">
    //         <StatefulTextInput
    //             type="text"
    //             label="Link"
    //             isRequired={true}
    //             id="test-input-simple"
    //             onChange={action("Input Changed")}
    //             onBlur={action("onBlur Called")}
    //         />
    //     </div>
    //     <input
    //       type="submit"
    //       className="button is-primary is-large is-fullwidth"
    //       value="Submit"
    //     />
    //   </form>
    //   )}
    //   renderFooter={close => (
    //     <ButtonList>
    //       <Button small type="secondary" onClick={close}>
    //         Cancel
    //       </Button>
    //       <Button small type="primary" onClick={close}>
    //         Add
    //       </Button>
    //     </ButtonList>
    //   )}
    // />