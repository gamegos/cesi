import React from "react";
import { Card, CardTitle, Badge, CustomInput } from "reactstrap";

const FilterOfGroups = props => {
  const { groups, checks, onInputChange } = props;
  return (
    <React.Fragment>
      {groups.length > 0 &&
        groups.map(group => (
          <Card body key={group.name}>
            <CardTitle>
              <CustomInput
                type="checkbox"
                name={group.name}
                id={group.name}
                label={group.name}
                onChange={onInputChange}
                checked={checks.indexOf(group.name) >= 0}
                inline
              />
              <Badge color="secondary">{group.environments.length}</Badge>
            </CardTitle>

            {group.environments.map(environment => (
              <Card body key={environment.name}>
                <CardTitle>
                  {environment.name}{" "}
                  <Badge color="secondary">{environment.members.length}</Badge>
                </CardTitle>
                {environment.members.map(member => (
                  <p key={member}>{member}</p>
                ))}
              </Card>
            ))}
          </Card>
        ))}
    </React.Fragment>
  );
};

export default FilterOfGroups;
