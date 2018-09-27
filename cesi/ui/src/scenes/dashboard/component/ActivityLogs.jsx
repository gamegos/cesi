import React from "react";
import { Row, Col, Button } from "reactstrap";

import { ActivityLogList } from "scenes/dashboard/component";

const ActivityLogs = ({ logs, refreshLogs, clearLogs }) => {
  return (
    <React.Fragment>
      <br />
      <Row>
        <Col sm="10">
          <h2>Activity Logs</h2>
        </Col>
        <Col>
          <Button outline color="info" onClick={refreshLogs}>
            Refresh
          </Button>
          <Button outline color="danger" onClick={clearLogs}>
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
};

export default ActivityLogs;
