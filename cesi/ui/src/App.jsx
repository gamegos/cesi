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
    loggedIn: false,
    profile: null,
    logs: [],
    nodes: [],
    environments: [],
    users: [],
    groups: []
  };

  getActivityLogs = async () => {
    try {
      const result = await api.activitylogs.get();
      return result.logs;
    } catch (error) {
      console.log(error);
      return [];
    }
  };

  refreshActivityLogs = () => {
    console.log("Refreshing...");
    this.getActivityLogs().then(logs => this.setState({ logs }));
  };

  clearActivityLogs = () => {
    api.activitylogs.clear().then(_ => this.setState({ logs: [] }));
  };

  getGroups = async () => {
    try {
      const result = await api.groups.get();
      console.log(result);
      return result.groups;
    } catch (error) {
      console.log(error);
      return [];
    }
  };

  refreshGroups = () => {
    this.getGroups().then(groups => {
      this.setState({ groups });
    });
  };

  getNodes = async () => {
    try {
      const result = await api.nodes.get();
      return result.nodes;
    } catch (error) {
      console.log(error);
      return [];
    }
  };

  refreshNodes = () => {
    this.getNodes().then(nodes => {
      this.setState({ nodes });
    });
  };

  getEnvironmets = async () => {
    const result = await api.environments.get();

    return Promise.all(
      result.environments.map(async environment => {
        const name = environment.name;
        let members = await Promise.all(
          environment.members.map(member => api.nodes.getNode(member))
        );
        members = members.map(member => member.node);
        return { name, members };
      })
    );
  };

  refreshEnvironments = () => {
    this.getEnvironmets().then(environments => {
      this.setState({ environments });
    });
  };

  getUsers = async () => {
    try {
      const result = await api.users.get();
      return result.users;
    } catch (error) {
      console.log(error);
      return [];
    }
  };
  refreshUsers = () => {
    this.getUsers().then(users => this.setState({ users }));
  };
  removeUser = username => {
    api.users
      .remove(username)
      .then(_ => this.refreshUsers())
      .catch(error => console.log(error));
  };
  handleLogIn = (username, password) => {
    api.auth
      .logIn(username, password)
      .then(_ => {
        this.getProfile();
      })
      .catch(error => {
        console.log(error);
      });
  };

  handleLogOut = () => {
    api.auth
      .logOut()
      .then(_ => {
        this.setState({
          profile: null,
          loggedIn: false
        });
      })
      .catch(error => {
        console.log(error);
      });
  };

  getProfile = () => {
    api.profile
      .get()
      .then(json => {
        this.setState({
          profile: json.user,
          loggedIn: true
        });
      })
      .catch(error => {
        console.log(error);
      });
  };
  componentDidMount() {
    this.getProfile();
  }
  render() {
    console.log("Render");
    return (
      <React.Fragment>
        {this.state.loggedIn ? (
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
                      clearActivityLogs={this.clearActivityLogs}
                      refreshActivityLogs={this.refreshActivityLogs}
                      refreshEnvironments={this.refreshEnvironments}
                      refreshNodes={this.refreshNodes}
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
                      refreshNodes={this.refreshNodes}
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
                      refreshEnvironments={this.refreshEnvironments}
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
                      refreshGroups={this.refreshGroups}
                      nodes={this.state.nodes}
                      refreshNodes={this.refreshNodes}
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
                      refreshUsers={this.refreshUsers}
                      removeUser={this.removeUser}
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
