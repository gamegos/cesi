import React, { Component } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  Form,
  FormGroup,
  Label,
  Input
} from "reactstrap";

import api from "services/api";
import FormMessage from "common/helpers/FormMessage";

class AddNewUserModal extends Component {
  state = {
    modal: false,
    username: "",
    password: "",
    confirmPassword: "",
    usertype: "0",
    formMessage: "",
    formStatus: ""
  };

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };
  handleInputChange = event => {
    const { name, value } = event.target;
    this.setState({
      [name]: value
    });
  };

  submitForm = e => {
    e.preventDefault();
    const { username, password, confirmPassword, usertype } = this.state;
    if (password !== confirmPassword) {
      this.setState({
        formStatus: "danger",
        formMessage: "Password and Confirm Password didn't match"
      });
      return;
    }
    api.users
      .add(username, password, usertype)
      .then(json => {
        this.setState({
          formStatus: "success",
          formMessage: `'${username}' successfully added`
        });
        setTimeout(() => {
          this.toggle();
          this.props.refreshUsers();
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
      username,
      password,
      confirmPassword,
      formMessage,
      formStatus
    } = this.state;
    return (
      <div>
        <Button outline color="success" onClick={this.toggle}>
          Add New User
        </Button>
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>New User</ModalHeader>
          <ModalBody>
            <Form onSubmit={this.submitForm}>
              <FormMessage message={formMessage} status={formStatus} />
              <FormGroup>
                <Label>Username</Label>
                <Input
                  type="username"
                  name="username"
                  id="exampleUsername"
                  placeholder="myusername"
                  value={username}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <FormGroup>
                <Label for="password">Password</Label>
                <Input
                  type="password"
                  name="password"
                  id="password"
                  placeholder="********"
                  value={password}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <FormGroup>
                <Label for="confirmPassword">Confirm Password</Label>
                <Input
                  type="password"
                  name="confirmPassword"
                  id="confirmPassword"
                  placeholder="********"
                  value={confirmPassword}
                  onChange={this.handleInputChange}
                />
              </FormGroup>
              <FormGroup>
                <Label for="usertype">Usertype</Label>
                <Input
                  type="select"
                  name="usertype"
                  id="usertype"
                  onChange={this.handleInputChange}
                >
                  <option value="0">Admin</option>
                  <option value="1">Normal User</option>
                </Input>
              </FormGroup>
              <Button color="success">Add</Button>{" "}
              <Button color="secondary" onClick={this.toggle}>
                Cancel
              </Button>
            </Form>
          </ModalBody>
        </Modal>
      </div>
    );
  }
}

export default AddNewUserModal;
