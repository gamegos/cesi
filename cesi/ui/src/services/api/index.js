import axios from "axios";

const API_PREFIX = "/api/v2";

const getRequest = url => {
  return axios
    .get(url)
    .then(res => res.data)
    .catch(error => {
      throw error.response.data;
    });
};

const postRequest = (url, data) => {
  return axios
    .post(url, data)
    .then(res => res.data)
    .catch(error => {
      throw error.response.data;
    });
};

const putRequest = (url, data) => {
  return axios
    .put(url, data)
    .then(res => res.data)
    .catch(error => {
      throw error.response.data;
    });
};

const deleteRequest = url => {
  return axios
    .delete(url)
    .then(res => res.data)
    .catch(error => {
      throw error.response.data;
    });
};

const activitylogs = {
  get: async () => {
    try {
      const response = await getRequest(`${API_PREFIX}/activitylogs/20/`);
      return response.logs;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  clear: () => deleteRequest(`${API_PREFIX}/activitylogs/`)
};

const auth = {
  logIn: (username, password) => {
    return postRequest(`${API_PREFIX}/auth/login/`, { username, password });
  },
  logOut: () => {
    return postRequest(`${API_PREFIX}/auth/logout/`);
  }
};

const profile = {
  get: async () => {
    try {
      const response = await getRequest(`${API_PREFIX}/profile/`);
      return response.user;
    } catch (error) {
      console.log(error);
      return null;
    }
  },
  changePassword: (oldPassword, newPassword) => {
    return putRequest(`${API_PREFIX}/profile/password/`, {
      oldPassword,
      newPassword
    });
  }
};

const nodes = {
  get: async () => {
    try {
      const result = await getRequest(`${API_PREFIX}/nodes/`);
      return result.nodes;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  getNode: nodeName => {
    return getRequest(`${API_PREFIX}/nodes/${nodeName}/`);
  },
  allProcess: {
    start: nodeName => {
      return getRequest(`${API_PREFIX}/nodes/${nodeName}/all-processes/start/`);
    },
    stop: nodeName => {
      return getRequest(`${API_PREFIX}/nodes/${nodeName}/all-processes/stop/`);
    },
    restart: nodeName => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/all-processes/restart/`
      );
    }
  }
};

const processes = {
  get: nodeName => {
    return getRequest(`${API_PREFIX}/nodes/${nodeName}/processes/`);
  },
  process: {
    get: (nodeName, processName) => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/processes/${processName}/`
      );
    },
    start: (nodeName, processName) => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/processes/${processName}/start/`
      );
    },
    stop: (nodeName, processName) => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/processes/${processName}/stop/`
      );
    },
    restart: (nodeName, processName) => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/processes/${processName}/restart/`
      );
    },
    log: (nodeName, processName) => {
      return getRequest(
        `${API_PREFIX}/nodes/${nodeName}/processes/${processName}/info/`
      );
    }
  }
};

const users = {
  get: async () => {
    try {
      const result = await getRequest(`${API_PREFIX}/users/`);
      return result.users;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  add: (username, password, usertype) => {
    return postRequest(`${API_PREFIX}/users/`, {
      username,
      password,
      usertype
    });
  },
  remove: username => {
    return deleteRequest(`${API_PREFIX}/users/${username}/`);
  }
};

const environments = {
  get: async () => {
    try {
      const result = await getRequest(`${API_PREFIX}/environments/`);
      console.log("GetEnvironments:", result);
      return Promise.all(
        result.environments.map(async environment => {
          const name = environment.name;
          let members = await Promise.all(
            environment.members.map(member =>
              nodes.getNode(member.general.name)
            )
          );
          members = members.map(member => member.node);
          return { name, members };
        })
      );
    } catch (error) {
      console.log(error);
      return [];
    }
  }
};

const groups = {
  get: async () => {
    try {
      const result = await getRequest(`${API_PREFIX}/groups/`);
      console.log(result);
      return result.groups;
    } catch (error) {
      console.log(error);
      return [];
    }
  }
};
export default {
  activitylogs,
  auth,
  profile,
  nodes,
  processes,
  users,
  environments,
  groups
};
