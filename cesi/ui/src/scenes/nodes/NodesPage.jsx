import React, { Component } from "react";
import { Row, Col, Container } from "reactstrap";

import Processes from "common/helpers/Processes";
import FilterOfNodes from "scenes/nodes/components/FilterOfNodes";

class NodesPage extends Component {
  state = {
    checks: []
  };

  handleInputChange = event => {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    if (value) {
      this.setState(prevState => ({
        checks: prevState.checks.concat([name])
      }));
    } else {
      this.setState(prevState => ({
        checks: prevState.checks.filter(element => element !== name)
      }));
    }
  };

  componentDidMount() {
    this.props.refreshNodes();
  }

  render() {
    const { checks } = this.state;
    const { nodes, refreshNodes } = this.props;

    return (
      <Container fluid>
        <Row>
          <Col sm={{ size: "auto" }}>
            <FilterOfNodes
              nodes={this.props.nodes}
              checks={checks}
              onInputChange={this.handleInputChange}
            />
          </Col>
          <Col>
            {nodes
              .filter(node => checks.indexOf(node.general.name) >= 0)
              .map(node => (
                <Processes
                  key={node.general.name}
                  node={node}
                  refreshNodes={refreshNodes}
                />
              ))}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default NodesPage;
