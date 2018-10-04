import React from "react";
import { Row, Col, Badge, Card, CardTitle, CardText } from "reactstrap";

import getConnectedAndNotConnectedNode from "util/index";

const DashboardSummary = ({ environments, nodes }) => {
  // Nodes and Processes
  console.log("DashboardSummary: Nodes:", nodes);
  const { connectedNodes, notConnectedNodes } = getConnectedAndNotConnectedNode(
    nodes
  );
  const processes = {
    running: [],
    stopped: []
  };
  for (const node of connectedNodes) {
    for (const process of node.processes) {
      if (process.statename === "STOPPED") {
        processes.stopped.push(process);
      } else if (process.statename === "RUNNING") {
        processes.running.push(process);
      }
    }
  }
  // Environments
  const NotDefaultEnvironmentNodes = [];
  for (const environment of environments) {
    if (environment.name !== "default") {
      NotDefaultEnvironmentNodes.push(...environment.members);
    }
  }

  return (
    <Row className="justify-content-md-center">
      <Col>
        <Card body>
          <CardTitle>
            Environments{" "}
            <Badge color="secondary">{environments.length - 1}</Badge>
          </CardTitle>
          <CardText>
            {NotDefaultEnvironmentNodes.length} Nodes | 0 Processes
          </CardText>
        </Card>
      </Col>
      <Col>
        <Card body>
          <CardTitle>
            Nodes <Badge color="secondary">3</Badge>
          </CardTitle>
          <CardText>
            {connectedNodes.length} Connected | {notConnectedNodes.length}{" "}
            Not-Connected
          </CardText>
        </Card>
      </Col>
      <Col>
        <Card body>
          <CardTitle>
            Processes{" "}
            <Badge color="secondary">
              {processes.running.length + processes.stopped.length}
            </Badge>
          </CardTitle>
          <CardText>
            {processes.running.length} Running | {processes.stopped.length}{" "}
            Stopped
          </CardText>
        </Card>
      </Col>
    </Row>
  );
};

export default DashboardSummary;
