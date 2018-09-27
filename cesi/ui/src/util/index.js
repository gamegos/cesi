const getConnectedAndNotConnectedNode = nodes => {
  const connectedNodes = [];
  const notConnectedNodes = [];
  for (const node of nodes) {
    if (node.general.connected === true) {
      connectedNodes.push(node);
    } else {
      notConnectedNodes.push(node);
    }
  }

  return { connectedNodes, notConnectedNodes };
};

export default getConnectedAndNotConnectedNode;
