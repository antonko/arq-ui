import { HoverCard, Text } from "@mantine/core";
import Selecto from "react-selecto";

import classes from "./timeline.module.css";

function TimeLine() {
  const renderContainers = () => {
    const containers = [];

    for (let i = 0; i < 60; i++) {
      containers.push(
        <HoverCard width={280} shadow="md" openDelay={500} key={i}>
          <HoverCard.Target>
            <div className={`${classes.item} target`}></div>
          </HoverCard.Target>
          <HoverCard.Dropdown>
            <Text size="sm">
              Info for item {i} <br />
            </Text>
          </HoverCard.Dropdown>
        </HoverCard>,
      );
    }
    return containers;
  };

  return (
    <>
      <Selecto
        container={document.body}
        dragContainer={".root"}
        selectableTargets={[".target"]}
        selectByClick={true}
        selectFromInside={true}
        continueSelect={false}
        toggleContinueSelect={"shift"}
        keyContainer={window}
        hitRate={0}
        onSelect={(e) => {
          e.added.forEach((el) => {
            el.classList.add(classes.selected);
          });
          e.removed.forEach((el) => {
            el.classList.remove(classes.selected);
          });
        }}
      />
      <div className={`${classes.root} root`}>{renderContainers()}</div>
    </>
  );
}

export default TimeLine;
