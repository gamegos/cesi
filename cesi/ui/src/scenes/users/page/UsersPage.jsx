import React, { Component } from "react";
import { Row, Col, Table, Container, Button } from "reactstrap";

import AddNewUserModal from "scenes/users/component/AddNewUserModal";

class UsersPage extends Component {
  componentDidMount() {
    this.props.refreshUsers();
  }
  render() {
    const UserTypes = ["Admin", "Normal User"];
    const { users, refreshUsers, removeUser } = this.props;
    return (
      <Container>
        <Row>
          <Col>
            <h2>Users</h2>
          </Col>
          <Col>
            <AddNewUserModal refreshUsers={refreshUsers} />
          </Col>
        </Row>
        <Row>
          <Table hover>
            <thead>
              <tr>
                <th>#</th>
                <th>Username</th>
                <th>Usertype</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u, index) => (
                <tr key={u.name}>
                  <th scope="row">{index}</th>
                  <td>{u.name}</td>
                  <td>{UserTypes[u.type]}</td>
                  <td>
                    <Button
                      color="danger"
                      disabled={u.name === "admin"}
                      onClick={() => removeUser(u.name)}
                    >
                      Remove
                    </Button>{" "}
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Row>
      </Container>
    );
  }
}

export default UsersPage;
