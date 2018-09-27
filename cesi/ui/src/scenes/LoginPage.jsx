import React, { Component } from "react";
import {
  Container,
  Col,
  Form,
  FormGroup,
  Label,
  Input,
  Button,
  Row
} from "reactstrap";
import FormMessage from "common/helpers/FormMessage";

class LoginPage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      formMessage: "",
      formStatus: ""
    };
  }

  handleChange = event => {
    const { name, value } = event.target;
    this.setState({
      [name]: value
    });
  };

  submitForm = e => {
    e.preventDefault();
    const { username, password } = this.state;
    this.props.onLogIn(username, password);
    this.setState({
      formStatus: "danger",
      formMessage: "Invalid username or password"
    });
  };

  render() {
    const { username, password, formMessage, formStatus } = this.state;
    return (
      <Container className="App">
        <Row>
          <Col>
            <h2>Log In</h2>
            <Form className="form-signin" onSubmit={this.submitForm}>
              <FormMessage message={formMessage} status={formStatus} />
              <FormGroup>
                <Label>Username</Label>
                <Input
                  type="username"
                  name="username"
                  id="exampleUsername"
                  placeholder="myusername"
                  value={username}
                  onChange={this.handleChange}
                />
              </FormGroup>
              <FormGroup>
                <Label for="examplePassword">Password</Label>
                <Input
                  type="password"
                  name="password"
                  id="examplePassword"
                  placeholder="********"
                  value={password}
                  onChange={this.handleChange}
                />
              </FormGroup>
              <Button block color="primary" size="lg">
                Submit
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default LoginPage;
