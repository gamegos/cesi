import React, { Component } from "react";
import { Card, CardTitle, Badge, Button, Table } from "reactstrap";
import PropTypes from "prop-types";

import api from "services/api";

class Processes extends Component {
  static propTypes = {
    node: PropTypes.object.isRequired,
    filterFunc: PropTypes.func
  };
  static defaultProps = {
    filterFunc: () => true
  };

  handleAllProcess = action => {
    const nodeName = this.props.node.general.name;
    api.nodes.allProcess[action](nodeName).then(() => {
      console.log("Updating nodes for single node action.");
      this.props.refresh();
    });
  };
  handleProcess = (action, processName) => {
    const nodeName = this.props.node.general.name;
    api.processes.process[action](nodeName, processName).then(() => {
      console.log("Updating nodes for single process action.");
      this.props.refresh();
    });
  };
  render() {
    const { node, filterFunc } = this.props;
    return (
      <React.Fragment>
        <Card body>
          <CardTitle>
            Processes for {node.general.name}{" "}
            <Badge color="secondary">{node.processes.length}</Badge>{" "}
            <Button
              color="success"
              onClick={() => this.handleAllProcess("start")}
            >
              Start All
            </Button>{" "}
            <Button
              color="danger"
              onClick={() => this.handleAllProcess("stop")}
            >
              Stop All
            </Button>{" "}
            <Button
              color="warning"
              onClick={() => this.handleAllProcess("restart")}
            >
              Restart All
            </Button>{" "}
          </CardTitle>
          {node.processes.length !== 0 ? (
            <Table hover>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Group</th>
                  <th>Pid</th>
                  <th>Uptime</th>
                  <th>State</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {node.processes.filter(filterFunc).map(process => (
                  <tr key={process.name}>
                    <td>{process.name}</td>
                    <td>{process.group}</td>
                    <td>{process.pid}</td>
                    <td>{process.uptime}</td>
                    <td>{process.statename}</td>
                    <td>
                      <Button
                        color="success"
                        onClick={() =>
                          this.handleProcess("start", process.name)
                        }
                      >
                        Start
                      </Button>{" "}
                      <Button
                        color="danger"
                        onClick={() => this.handleProcess("stop", process.name)}
                      >
                        Stop
                      </Button>{" "}
                      <Button
                        color="warning"
                        onClick={() =>
                          this.handleProcess("restart", process.name)
                        }
                      >
                        Restart
                      </Button>{" "}
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          ) : (
            <p>No processes configured.</p>
          )}
        </Card>
        <br />
      </React.Fragment>
    );
  }
}

export default Processes;
