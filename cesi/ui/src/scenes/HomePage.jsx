import React from "react";

const HomePage = () => {
  return (
    <div>
      <h1>Cesi</h1>
      <p>Cesi provides a web interface that manages many supervisors.</p>
      <p>We used these technologies:</p>
      <ul>
        <li>Python3 (+3.4)</li>
        <li>Flask (+1.0)</li>
        <li>ReactJs (+16.0)</li>
      </ul>
      <a href="https://github.com/gamegos/cesi">
        Source Code and Documentation
      </a>
      <br />
      <br />
      <h4>Dashboard</h4>
      <p>
        We can see that the total number of nodes, number of connected nodes and
        number of not connected nodes in this page. Also we can see total number
        of process, number of running process, number of stopped process and the
        all activity logs.
      </p>
      <h4>Nodes</h4>
      <p>....</p>
      <h4>Environments</h4>
      <p>....</p>
      <h4>Groups</h4>
      <p>....</p>
      <h4>Users</h4>
      <p>....</p>
    </div>
  );
};

export default HomePage;
