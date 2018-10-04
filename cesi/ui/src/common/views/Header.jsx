import React, { Component } from "react";
import { NavLink as RRNavLink } from "react-router-dom";
import {
  Navbar,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  NavbarToggler,
  Collapse,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem
} from "reactstrap";

import ChangePasswordModal from "common/views/ChangePasswordModal";

class HeaderProfileSettings extends Component {
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
                <DropdownItem>
                  <ChangePasswordModal />
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
const Header = ({ onLogOut, isAdmin }) => {
  return (
    <Navbar color="light" light expand="md">
      <NavbarBrand exact to="/" tag={RRNavLink}>
        Cesi
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
      <HeaderProfileSettings onLogOut={onLogOut} />
    </Navbar>
  );
};

export default Header;
