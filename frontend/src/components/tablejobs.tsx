import {
  Table,
  UnstyledButton,
  Group,
  Text,
  Center,
  rem,
  Pagination,
  Paper,
  Box,
  LoadingOverlay,
  Badge,
  Tooltip,
} from "@mantine/core";
import {
  IconSelector,
  IconChevronDown,
  IconChevronUp,
} from "@tabler/icons-react";
import { observer } from "mobx-react-lite";
import React from "react";

import { rootStore } from "../stores";

import classes from "./tablejobs.module.css";

interface IThProps {
  children: React.ReactNode;
  onSort(): void;
  name: string;
}

function Th({ children, onSort, name }: IThProps) {
  let Icon = IconSelector;
  if (rootStore.tableJobs.sort_by === name) {
    Icon =
      rootStore.tableJobs.sort_order === "asc"
        ? IconChevronUp
        : IconChevronDown;
  }
  return (
    <Table.Th className={classes.th}>
      <UnstyledButton onClick={onSort} className={classes.control}>
        <Group justify="space-between">
          <Text fw={500} fz="sm">
            {children}
          </Text>
          <Center className={classes.icon}>
            <Icon style={{ width: rem(16), height: rem(16) }} stroke={1.5} />
          </Center>
        </Group>
      </UnstyledButton>
    </Table.Th>
  );
}

function StatusControl(status: string, success: boolean) {
  let label = "";
  let color = "";
  let displayStatus = status;

  switch (status) {
    case "complete":
      label = success ? "Success" : "Failed";
      color = success ? "green" : "red";
      displayStatus = "complete";
      break;
    case "queued":
      label = "Queued";
      color = "gray";
      break;
    case "deferred":
      label = "Deferred";
      color = "gray";
      break;
    case "in_progress":
      label = "In Progress";
      color = "blue";
      break;
    default:
      label = "Unknown";
      color = "gray";
      break;
  }

  return (
    <Tooltip label={label} position="top" withArrow>
      <Badge color={color}>{displayStatus}</Badge>
    </Tooltip>
  );
}

export const TableJobs = observer(() => {
  const rows = rootStore.tableJobs.items.map((row) => (
    <React.Fragment key={row.id}>
      <Table.Tr
        key={row.id}
        className={classes.tr}
        onClick={() => rootStore.tableJobs.setToggleJob(row.id)}
      >
        <Table.Td className={classes.td}>{row.enqueue_time}</Table.Td>
        <Table.Td className={classes.td}>{row.id}</Table.Td>
        <Table.Td className={classes.td}>
          {StatusControl(row.status, row.success)}
        </Table.Td>
        <Table.Td className={classes.td}>{row.function}</Table.Td>
        <Table.Td className={classes.td}>{row.start_time}</Table.Td>
        <Table.Td className={classes.td}>{row.execution_duration}</Table.Td>
        <Table.Td className={classes.td}>{row.args}</Table.Td>
      </Table.Tr>
      <Table.Tr className={classes.expander_tr} key={`"${row.id}1`}>
        <Table.Td colSpan={7}>
          <div
            className={`${classes.expandedContent} ${
              rootStore.tableJobs.toggle_jobs.includes(row.id)
                ? classes.expandedContentshow
                : ""
            }`}
          >
            <Paper shadow="xs" p="xl">
              <Text>
                {row.enqueue_time} <br />
                {row.id} <br />
                {row.status} <br />
                {row.function} <br />
                {row.start_time} <br />
                {row.execution_duration} <br />
                {row.args} <br />
              </Text>
            </Paper>
          </div>
        </Table.Td>
      </Table.Tr>
    </React.Fragment>
  ));

  return (
    <>
      <Box pos="relative">
        <LoadingOverlay
          visible={rootStore.isLoading}
          zIndex={200}
          overlayProps={{ radius: "sm", blur: 1 }}
        />
        <Table
          horizontalSpacing="md"
          verticalSpacing="xs"
          miw={700}
          layout="fixed"
        >
          <Table.Tbody>
            <Table.Tr>
              <Th
                onSort={() => rootStore.setSortBy("enqueue_time")}
                key="enqueue_time"
                name="enqueue_time"
              >
                Enqueue time
              </Th>
              <Th onSort={() => rootStore.setSortBy("id")} key="id" name="id">
                ID
              </Th>
              <Th
                onSort={() => rootStore.setSortBy("status")}
                key="status"
                name="status"
              >
                Status
              </Th>
              <Th
                onSort={() => rootStore.setSortBy("function")}
                key="functio"
                name="function"
              >
                Function
              </Th>
              <Th
                onSort={() => rootStore.setSortBy("start_time")}
                key="start_time"
                name="start_time"
              >
                Start Time
              </Th>
              <Th
                onSort={() => rootStore.setSortBy("execution_duration")}
                key="duration"
                name="execution_duration"
              >
                Duration
              </Th>
              <Th
                onSort={() => rootStore.setSortBy("args")}
                key="args"
                name="args"
              >
                Args
              </Th>
            </Table.Tr>
          </Table.Tbody>
          <Table.Tbody>{rows}</Table.Tbody>
        </Table>
      </Box>
      <Center mt="xl">
        <Pagination
          total={rootStore.totalPages}
          value={rootStore.currentPage}
          onChange={(value) => rootStore.setPage(value)}
          disabled={rootStore.isLoading}
        />
      </Center>
    </>
  );
});
