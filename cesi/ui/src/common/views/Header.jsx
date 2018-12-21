import React, { Component } from "react";
import { NavLink as RRNavLink } from "react-router-dom";
import {
  Nav,
  Navbar,
  NavbarBrand,
  NavbarToggler,
  NavItem,
  NavLink,
  Badge,
  Collapse,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from "reactstrap";

class HeaderSettings extends Component {
  state = { isOpen: false };

  toggle = () => {
    this.setState({
      isOpen: !this.state.isOpen
    });
  };

  render() {
    return (
      <React.Fragment>
        <NavbarToggler onClick={this.toggle} />
        <Collapse isOpen={this.state.isOpen} navbar>
          <Nav className="ml-auto" navbar>
            <UncontrolledDropdown nav inNavbar>
              <DropdownToggle nav caret>
                Settings
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem tag="div">
                  <NavLink to="/about" tag={RRNavLink}>
                    <strong>About</strong>
                  </NavLink>
                </DropdownItem>
                <DropdownItem tag="div">
                  <NavLink to="/profile/change_password" tag={RRNavLink}>
                    <strong>Change Password</strong>
                  </NavLink>
                </DropdownItem>
                <DropdownItem divider />
                <DropdownItem onClick={this.props.onLogOut}>
                  Logout
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          </Nav>
        </Collapse>
      </React.Fragment>
    );
  }
}

/**
 * https://stackoverflow.com/questions/42372179/reactstrap-and-react-router-4-0-0-beta-6-active-navlink
 *
 */
const Header = ({ onLogOut, isAdmin, version }) => {
  return (
    <Navbar color="light" light expand="md">
      <NavbarBrand exact to="/about" tag={RRNavLink}>
        Cesi <Badge color="success">{version}</Badge>
      </NavbarBrand>
      <Nav pills>
        <NavItem>
          <NavLink exact replace to="/dashboard" tag={RRNavLink}>
            Dashboard
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink exact replace to="/nodes" tag={RRNavLink}>
            Nodes
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink exact replace to="/environments" tag={RRNavLink}>
            Environments
          </NavLink>
        </NavItem>
        <NavItem>
          <NavLink exact replace to="/groups" tag={RRNavLink}>
            Groups
          </NavLink>
        </NavItem>
        {isAdmin && (
          <NavItem>
            <NavLink exact replace to="/users" tag={RRNavLink}>
              Users
            </NavLink>
          </NavItem>
        )}
      </Nav>
      <HeaderSettings onLogOut={onLogOut} />
    </Navbar>
  );
};

export default Header;
