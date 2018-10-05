import React from "react";
import { Row, Col, Badge, Card, CardTitle, CardText } from "reactstrap";

import getConnectedAndNotConnectedNode from "util/index";

const DashboardSummary = ({ environments, nodes }) => {
  // Nodes and Processes Sections
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

  // Environments Section
  const environmentNodes = environments.reduce(
    (nodes, env) => nodes.concat(...env.members),
    []
  );

  const amountOfProcessesForEnvironment = environmentNodes.reduce(
    (total, node) => total + node.processes.length,
    0
  );

  return (
    <Row className="justify-content-md-center">
      <Col>
        <Card body>
          <CardTitle>
            Environments <Badge color="secondary">{environments.length}</Badge>
          </CardTitle>
          <CardText>
            {environmentNodes.length} Nodes | {amountOfProcessesForEnvironment}{" "}
            Processes
          </CardText>
        </Card>
      </Col>
      <Col>
        <Card body>
          <CardTitle>
            Nodes <Badge color="secondary">{nodes.length}</Badge>
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
