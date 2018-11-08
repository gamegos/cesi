import React from "react";

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
import { withRouter } from "react-router-dom";

import FormMessage from "common/helpers/FormMessage";
import api from "services/api";

class ChangePassword extends React.Component {
  state = {
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
    formMessage: "",
    formStatus: ""
  };

  handleInputChange = event => {
    const { name, value } = event.target;
    this.setState({
      [name]: value
    });
  };

  handleChangePassword = e => {
    e.preventDefault();
    const { oldPassword, newPassword, confirmPassword } = this.state;
    if (!oldPassword) {
      this.setState({
        formStatus: "danger",
        formMessage: "Please enter valid value old password"
      });
      return;
    }
    if (newPassword !== confirmPassword) {
      this.setState({
        formStatus: "danger",
        formMessage: "New Password and Confirm Password didn't match"
      });
      return;
    }
    api.profile
      .changePassword(oldPassword, newPassword)
      .then(json => {
        this.setState({
          formStatus: "success",
          formMessage: "Success! Your Password has been changed!"
        });
        setTimeout(() => {
          // Redirect home page
          this.props.history.push("/");
        }, 1000);
      })
      .catch(error => {
        console.log(error);
        this.setState({
          formStatus: "danger",
          formMessage: error.message
        });
      });
  };
  render() {
    const {
      oldPassword,
      newPassword,
      confirmPassword,
      formMessage,
      formStatus
    } = this.state;
    return (
      <Container className="App">
        <Row>
          <Col>
            <h2>Change Password</h2>
            <Form onSubmit={this.handleChangePassword}>
              <FormMessage message={formMessage} status={formStatus} />
              <FormGroup>
                <Label>Old Password</Label>
                <Input
                  type="password"
                  name="oldPassword"
                  placeholder="******"
                  value={oldPassword}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <FormGroup>
                <Label>New Password</Label>
                <Input
                  type="password"
                  name="newPassword"
                  placeholder="******"
                  value={newPassword}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <FormGroup>
                <Label>Confirm Password</Label>
                <Input
                  type="password"
                  name="confirmPassword"
                  placeholder="******"
                  value={confirmPassword}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <Button color="primary">Change</Button>{" "}
              <Button color="secondary" onClick={this.toggle}>
                Cancel
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    );
  }
}

export default withRouter(ChangePassword);
