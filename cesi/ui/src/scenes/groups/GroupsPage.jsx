import React, { Component } from "react";
import { Card, CardTitle, Row, Col, Container, Badge } from "reactstrap";

import Processes from "common/helpers/Processes";
import FilterOfGroups from "scenes/groups/components/FilterOfGroups";

class GroupsPage extends Component {
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

  componentWillMount() {
    this.props.refreshGroups();
  }

  render() {
    const { checks } = this.state;
    const { groups, nodes, refreshNodes } = this.props;
    const filterFunc = process => {
      return checks.includes(process.group);
    };
    return (
      <Container fluid>
        <Row>
          <Col sm={{ size: "auto" }}>
            <Card body>
              <CardTitle>
                {"Groups "} <Badge color="secondary">{groups.length}</Badge>
              </CardTitle>
              <FilterOfGroups
                groups={groups}
                checks={checks}
                onInputChange={this.handleInputChange}
              />
            </Card>
          </Col>
          <Col>
            {checks.length > 0 &&
              nodes.map(node => (
                <Processes
                  key={node.general.name}
                  node={node}
                  filterFunc={filterFunc}
                  refresh={refreshNodes}
                />
              ))}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default GroupsPage;
