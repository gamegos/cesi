import axios from "axios";

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
      const response = await getRequest("/v2/activitylogs/20/");
      return response.logs;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  clear: () => deleteRequest("/v2/activitylogs/")
};

const auth = {
  logIn: (username, password) => {
    return postRequest("/v2/auth/login/", { username, password });
  },
  logOut: () => {
    return postRequest("/v2/auth/logout/");
  }
};

const profile = {
  get: async () => {
    try {
      const response = await getRequest("/v2/profile/");
      return response.user;
    } catch (error) {
      console.log(error);
      return null;
    }
  },
  changePassword: (oldPassword, newPassword) => {
    return putRequest("/v2/profile/password/", { oldPassword, newPassword });
  }
};

const nodes = {
  get: async () => {
    try {
      const result = await getRequest("/v2/nodes/");
      return result.nodes;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  getNode: nodeName => {
    return getRequest(`/v2/nodes/${nodeName}/`);
  },
  allProcess: {
    start: nodeName => {
      return getRequest(`/v2/nodes/${nodeName}/all-processes/start/`);
    },
    stop: nodeName => {
      return getRequest(`/v2/nodes/${nodeName}/all-processes/stop/`);
    },
    restart: nodeName => {
      return getRequest(`/v2/nodes/${nodeName}/all-processes/restart/`);
    }
  }
};

const processes = {
  get: nodeName => {
    return getRequest(`/v2/nodes/${nodeName}/processes/`);
  },
  process: {
    get: (nodeName, processName) => {
      return getRequest(`/v2/nodes/${nodeName}/processes/${processName}/`);
    },
    start: (nodeName, processName) => {
      return getRequest(
        `/v2/nodes/${nodeName}/processes/${processName}/start/`
      );
    },
    stop: (nodeName, processName) => {
      return getRequest(`/v2/nodes/${nodeName}/processes/${processName}/stop/`);
    },
    restart: (nodeName, processName) => {
      return getRequest(
        `/v2/nodes/${nodeName}/processes/${processName}/restart/`
      );
    },
    log: (nodeName, processName) => {
      return getRequest(`/v2/nodes/${nodeName}/processes/${processName}/info/`);
    }
  }
};

const users = {
  get: async () => {
    try {
      const result = await getRequest("/v2/users/");
      return result.users;
    } catch (error) {
      console.log(error);
      return [];
    }
  },
  add: (username, password, usertype) => {
    return postRequest("/v2/users/", { username, password, usertype });
  },
  remove: username => {
    return deleteRequest(`/v2/users/${username}/`);
  }
};

const environments = {
  get: async () => {
    try {
      const result = await getRequest("/v2/environments/");
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
      const result = await getRequest("/v2/groups/");
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
