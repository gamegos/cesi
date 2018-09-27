import React, { Component } from "react";
import { Card, CardTitle, Row, Col, Badge, Container } from "reactstrap";

import Processes from "common/helpers/Processes";
import FilterOfEnvironments from "scenes/environments/component/FilterOfEnvironments";

class EnvironmentsPage extends Component {
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
    this.props.refreshEnvironments();
  }

  render() {
    const { checks } = this.state;
    const { environments, refreshEnvironments } = this.props;
    return (
      <Container fluid>
        <Row>
          <Col sm={{ size: "auto" }}>
            <Card body>
              <CardTitle>Environments</CardTitle>
              <FilterOfEnvironments
                environments={this.props.environments}
                checks={this.state.checks}
                onInputChange={this.handleInputChange}
              />
            </Card>
          </Col>
          <Col>
            {checks.map(environmentName =>
              environments
                .filter(environment => environment.name === environmentName)
                .map(environment => (
                  <div key={environment.name}>
                    <h1>
                      Environment:
                      <Badge color="info">{environment.name}</Badge>
                    </h1>
                    {environment.members.map(member => (
                      <Processes
                        key={member.general.name}
                        node={member}
                        refresh={refreshEnvironments}
                      />
                    ))}
                  </div>
                ))
            )}
          </Col>
        </Row>
      </Container>
    );
  }
}

export default EnvironmentsPage;
