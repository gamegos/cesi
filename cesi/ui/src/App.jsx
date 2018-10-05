import React, { Component } from "react";
import { HashRouter, Route, Switch } from "react-router-dom";

import "./App.css";
import api from "services/api";
import {
  LoginPage,
  DashboardPage,
  ErrorPage,
  GroupsPage,
  NodesPage,
  EnvironmentsPage,
  UsersPage,
  HomePage
} from "scenes/index";

import Header from "common/views/Header";

class App extends Component {
  state = {
    profile: null,
    logs: [],
    nodes: [],
    environments: [],
    users: [],
    groups: []
  };

  handleRefreshActivityLogs = async () => {
    const logs = await api.activitylogs.get();
    this.setState({ logs });
  };

  handleClearActivityLogs = async () => {
    await api.activitylogs.clear();
    this.setState({ logs: [] });
  };

  handleRefreshGroups = async () => {
    const groups = await api.groups.get();
    this.setState({ groups });
  };

  handleRefreshNodes = async () => {
    const nodes = await api.nodes.get();
    this.setState({ nodes });
  };

  handleRefreshEnvironments = async () => {
    const environments = await api.environments.get();
    this.setState({ environments });
  };

  handleRefreshDashboardSummary = async () => {
    await this.handleRefreshEnvironments();
    await this.handleRefreshNodes();
  };

  handleRefreshUsers = async () => {
    const users = await api.users.get();
    this.setState({ users });
  };

  handleRemoveUser = username => {
    api.users
      .remove(username)
      .then(() => this.handleRefreshUsers())
      .catch(error => console.log(error));
  };

  handleLogIn = (username, password) => {
    return new Promise(async (resolve, reject) => {
      try {
        await api.auth.logIn(username, password);
        resolve("okey");
        this.handleRefreshProfile();
      } catch (error) {
        console.log(error);
        reject(error);
      }
    });
  };

  handleLogOut = () => {
    api.auth
      .logOut()
      .then(() => {
        this.handleRefreshProfile();
      })
      .catch(error => console.log(error));
  };

  handleRefreshProfile = async () => {
    const profile = await api.profile.get();
    this.setState({ profile });
  };
  componentDidMount() {
    this.handleRefreshProfile();
  }
  render() {
    return (
      <React.Fragment>
        {this.state.profile ? (
          <HashRouter>
            <React.Fragment>
              <Header
                isAdmin={this.state.profile.type === 0}
                onLogOut={this.handleLogOut}
              />
              <Switch>
                <Route path="/" exact component={HomePage} />
                <Route
                  path="/dashboard"
                  exact
                  render={props => (
                    <DashboardPage
                      {...props}
                      logs={this.state.logs}
                      environments={this.state.environments}
                      nodes={this.state.nodes}
                      clearActivityLogs={this.handleClearActivityLogs}
                      refreshActivityLogs={this.handleRefreshActivityLogs}
                      refreshDashboardSummary={
                        this.handleRefreshDashboardSummary
                      }
                    />
                  )}
                />
                <Route
                  path="/nodes"
                  exact
                  render={props => (
                    <NodesPage
                      {...props}
                      nodes={this.state.nodes}
                      refreshNodes={this.handleRefreshNodes}
                    />
                  )}
                />
                <Route
                  path="/environments"
                  exact
                  render={props => (
                    <EnvironmentsPage
                      {...props}
                      environments={this.state.environments}
                      refreshEnvironments={this.handleRefreshEnvironments}
                    />
                  )}
                />
                <Route
                  path="/groups"
                  exact
                  render={props => (
                    <GroupsPage
                      {...props}
                      groups={this.state.groups}
                      refreshGroups={this.handleRefreshGroups}
                      nodes={this.state.nodes}
                      refreshNodes={this.handleRefreshNodes}
                    />
                  )}
                />
                <Route
                  path="/users"
                  exact
                  render={props => (
                    <UsersPage
                      {...props}
                      users={this.state.users}
                      refreshUsers={this.handleRefreshUsers}
                      removeUser={this.handleRemoveUser}
                    />
                  )}
                />
                <Route component={ErrorPage} />
              </Switch>
            </React.Fragment>
          </HashRouter>
        ) : (
          <LoginPage onLogIn={this.handleLogIn} />
        )}
      </React.Fragment>
    );
  }
}

export default App;
