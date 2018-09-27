import React from "react";
import { UncontrolledAlert } from "reactstrap";

const FormMessage = props => {
  const { message, status } = props;
  return (
    <React.Fragment>
      {status && (
        <UncontrolledAlert color={status}>{message}</UncontrolledAlert>
      )}
    </React.Fragment>
  );
};

export default FormMessage;
