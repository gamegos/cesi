import React from "react";
import { ListGroup, ListGroupItem } from "reactstrap";

const ActivityLogList = ({ logs }) => {
  return (
    <ListGroup>
      {logs.map(log => (
        <ListGroupItem key={log}>{log}</ListGroupItem>
      ))}
    </ListGroup>
  );
};

export default ActivityLogList;
