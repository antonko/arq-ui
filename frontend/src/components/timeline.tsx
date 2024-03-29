import { Divider, Group, HoverCard, Stack, Text, Title } from "@mantine/core";
import { format } from "date-fns";
import { observer } from "mobx-react-lite";

import { rootStore } from "../stores";
import { ColorStatistics } from "../stores/models";

import classes from "./timeline.module.css";

export const TimeLine = observer(() => {
  function getCssColor(color: ColorStatistics, colorIntensity: number): string {
    const colorMap: { [key in ColorStatistics]: string } = {
      [ColorStatistics.red]: "255, 0, 0",
      [ColorStatistics.green]: "50, 205, 50",
      [ColorStatistics.gray]: "128, 128, 128",
      [ColorStatistics.orange]: "255, 165, 0",
    };

    const rgb = colorMap[color] || "0, 0, 0";

    return `rgba(${rgb}, ${colorIntensity})`;
  }

  const items = rootStore.statistics_hourly?.map((item) => (
    <HoverCard
      width={280}
      shadow="md"
      openDelay={200}
      key={item.date.toString()}
    >
      <HoverCard.Target>
        <div
          className={`${classes.item} target`}
          style={{
            backgroundColor: getCssColor(item.color, item.color_intensity),
          }}
        ></div>
      </HoverCard.Target>
      <HoverCard.Dropdown>
        <Stack p="xs" gap="xs">
          <Title order={6}>{format(item.date, "yyyy-MM-dd HH:mm:ss")}</Title>
          <Divider size={1} />
          <Group p={0} m={0} justify="space-between">
            <Text>Total created:</Text>
            <Text>1</Text>
          </Group>
          <Group justify="space-between">
            <Text>Total completed:</Text>
            <Text>3</Text>
          </Group>
          <Group justify="space-between">
            <Text>Total failed:</Text>
            <Text>1</Text>
          </Group>
          <Group justify="space-between">
            <Text>Total in progress:</Text>
            <Text>11</Text>
          </Group>
        </Stack>
      </HoverCard.Dropdown>
    </HoverCard>
  ));

  return (
    <>
      <div className={`${classes.root} root`}>{items}</div>
    </>
  );
});
