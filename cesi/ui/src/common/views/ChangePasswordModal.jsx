import React from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  Form,
  FormGroup,
  Input,
  Label
} from "reactstrap";

import FormMessage from "common/helpers/FormMessage";
import api from "services/api";

class ChangePassword extends React.Component {
  state = {
    modal: false,
    oldPassword: "",
    newPassword: "",
    confirmPassword: "",
    formMessage: "",
    formStatus: ""
  };

  toggle = () => {
    this.setState({
      modal: !this.state.modal
    });
  };

  handleChangePassword = e => {
    e.preventDefault();
    const { oldPassword, newPassword, confirmPassword } = this.state;
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
          this.toggle();
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
  handleInputChange = event => {
    const { name, value } = event.target;
    this.setState({
      [name]: value
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
      <div>
        <span onClick={this.toggle}>Change Password</span>
        <Modal isOpen={this.state.modal} toggle={this.toggle}>
          <ModalHeader toggle={this.toggle}>Changing Your Password</ModalHeader>
          <ModalBody>
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
          </ModalBody>
        </Modal>
      </div>
    );
  }
}

export default ChangePassword;
