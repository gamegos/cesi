import React from "react";
import { Card, CardTitle, Badge, CustomInput } from "reactstrap";

import getConnectedAndNotConnectedNode from "util/index";

const FilterOfEnvironments = props => {
  const { checks, environments, onInputChange } = props;
  const extendedEnvironments = environments.map(environment => {
    const {
      connectedNodes,
      notConnectedNodes
    } = getConnectedAndNotConnectedNode(environment.members);
    return { ...environment, connectedNodes, notConnectedNodes };
  });
  return (
    <React.Fragment>
      {extendedEnvironments.length > 0 &&
        extendedEnvironments.map(environment => (
          <Card body key={environment.name}>
            <CardTitle>
              <CustomInput
                type="checkbox"
                name={environment.name}
                id={environment.name}
                label={environment.name}
                onChange={onInputChange}
                checked={checks.indexOf(environment.name) >= 0}
                inline
              />
              <Badge color="secondary">{environment.members.length}</Badge>
            </CardTitle>

            <Card body>
              <CardTitle>
                Connected{" "}
                <Badge color="secondary">
                  {environment.connectedNodes.length}
                </Badge>
              </CardTitle>
              {environment.connectedNodes.map(member => (
                <p key={member.general.name}>{member.general.name}</p>
              ))}
            </Card>
            <Card body>
              <CardTitle>
                Not-Connected{" "}
                <Badge color="secondary">
                  {environment.notConnectedNodes.length}
                </Badge>
              </CardTitle>
              {environment.notConnectedNodes.map(member => (
                <p key={member.general.name}>{member.general.name}</p>
              ))}
            </Card>
          </Card>
        ))}
    </React.Fragment>
  );
};

export default FilterOfEnvironments;
