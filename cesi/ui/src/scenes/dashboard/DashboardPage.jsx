import React, { Component } from "react";
import { Container } from "reactstrap";

import { ActivityLogs, DashboardSummary } from "scenes/dashboard/components";

class DashboardPage extends Component {
  componentDidMount() {
    this.props.refreshActivityLogs();
    this.props.refreshEnvironments();
    this.props.refreshNodes();
  }
  render() {
    const {
      environments,
      nodes,
      logs,
      refreshActivityLogs,
      clearActivityLogs
    } = this.props;
    return (
      <Container>
        <DashboardSummary environments={environments} nodes={nodes} />
        <ActivityLogs
          logs={logs}
          refreshLogs={refreshActivityLogs}
          clearLogs={clearActivityLogs}
        />
      </Container>
    );
  }
}

export default DashboardPage;
