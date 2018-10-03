import React, { Component } from "react";
import { Row, Col, Button } from "reactstrap";

import { ActivityLogList } from "scenes/dashboard/components";

class ActivityLogs extends Component {
  state = {
    isReverse: false
  };

  reverse = () => {
    this.setState((prevstate, _) => ({
      isReverse: !prevstate.isReverse
    }));
  };
  render() {
    let logs = this.props.logs;
    if (this.state.isReverse) {
      logs = logs.reverse();
    }

    return (
      <React.Fragment>
        <br />
        <Row>
          <Col sm="9">
            <h2>Activity Logs</h2>
          </Col>
          <Col>
            <Button outline color="warning" onClick={this.reverse}>
              Reverse
            </Button>{" "}
            <Button outline color="info" onClick={this.props.refreshLogs}>
              Refresh
            </Button>{" "}
            <Button outline color="danger" onClick={this.props.clearLogs}>
              Clear
            </Button>
          </Col>
        </Row>
        <Row>
          <Col>
            <ActivityLogList logs={logs} />
          </Col>
        </Row>
      </React.Fragment>
    );
  }
}

export default ActivityLogs;
