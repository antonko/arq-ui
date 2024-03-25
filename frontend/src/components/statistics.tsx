import { Group, Paper, SimpleGrid, Text } from "@mantine/core";
import {
  IconActivity,
  IconBug,
  IconCircleNumber0,
  IconProgress,
} from "@tabler/icons-react";
import { observer } from "mobx-react-lite";

import { rootStore } from "../stores";

import classes from "./statistics.module.css";

const Card = ({
  title,
  value,
  description,
  icon,
}: {
  title: string;
  value: number;
  description: string;
  icon: React.ReactNode;
}) => (
  <Paper withBorder p="md" radius="md">
    <Group justify="space-between">
      <Text size="xs" c="dimmed" className={classes.title}>
        {title}
      </Text>
      {icon}
    </Group>
    <Group align="flex-end" gap="xs" mt={25}>
      <Text className={classes.value}>{value}</Text>
    </Group>
    <Text size="xs" c="dimmed" mt={7}>
      {description}
    </Text>
  </Paper>
);

export const Statistics = observer(() => (
  <SimpleGrid cols={{ xs: 1, sm: 2, md: 4 }}>
    <Card
      title="Total jobs"
      value={rootStore.statistics.total}
      description="Total jobs in the database"
      icon={
        <IconCircleNumber0
          className={classes.icon}
          size="1.4rem"
          stroke={1.5}
        />
      }
    />
    <Card
      title="Queued"
      value={rootStore.statistics.queued}
      description="Total jobs in the queue"
      icon={
        <IconActivity className={classes.icon} size="1.4rem" stroke={1.5} />
      }
    />
    <Card
      title="In progress"
      value={rootStore.statistics.in_progress}
      description="Total jobs in progress"
      icon={
        <IconProgress className={classes.icon} size="1.4rem" stroke={1.5} />
      }
    />
    <Card
      title="Errors"
      value={rootStore.statistics.failed}
      description="Total jobs with errors"
      icon={<IconBug className={classes.icon} size="1.4rem" stroke={1.5} />}
    />
  </SimpleGrid>
));
