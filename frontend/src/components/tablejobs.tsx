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
  Space,
  ScrollArea,
  SimpleGrid,
  Code,
  Button,
} from "@mantine/core";
import {
  IconSelector,
  IconChevronDown,
  IconChevronUp,
} from "@tabler/icons-react";
import { format } from "date-fns";
import { observer } from "mobx-react-lite";
import React from "react";

import { rootStore } from "../stores";
import { AbortStatus } from "../stores/models";

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
  const rows = rootStore.tableJobs.items.map((job) => (
    <React.Fragment key={job.id}>
      <Table.Tr
        key={job.id}
        className={classes.tr}
        onClick={() => rootStore.tableJobs.setToggleJob(job.id)}
      >
        <Table.Td className={classes.td}>
          {format(job.enqueue_time, "yyyy-MM-dd HH:mm:ss")}
        </Table.Td>
        <Table.Td className={classes.td}>{job.id}</Table.Td>
        <Table.Td className={classes.td}>
          {StatusControl(job.status, job.success)}
        </Table.Td>
        <Table.Td className={classes.td}>{job.function}</Table.Td>
        <Table.Td className={classes.td}>
          {job.start_time && format(job.start_time, "yyyy-MM-dd HH:mm:ss")}
        </Table.Td>
        <Table.Td className={classes.td}>{job.execution_duration} </Table.Td>
      </Table.Tr>
      <Table.Tr className={classes.expander_tr} key={`"${job.id}1`}>
        <Table.Td colSpan={6}>
          <div
            className={`${classes.expandedContent} ${
              rootStore.tableJobs.toggle_jobs.includes(job.id)
                ? classes.expandedContentshow
                : ""
            }`}
          >
            <Paper p="md">
              <SimpleGrid cols={2} spacing="xl">
                <Box>
                  <Table
                    horizontalSpacing="sm"
                    verticalSpacing="sm"
                    highlightOnHover
                    striped
                    styles={{}}
                  >
                    <Table.Tbody>
                      <Table.Tr
                        style={{ overflow: "hidden", textOverflow: "ellipsis" }}
                      >
                        <Table.Td>id</Table.Td>
                        <Table.Td
                          style={{
                            overflow: "hidden",
                          }}
                        >
                          {job.id}
                        </Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>queue name</Table.Td>
                        <Table.Td>{job.queue_name}</Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>function</Table.Td>
                        <Table.Td>{job.function}</Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>status</Table.Td>
                        <Table.Td>{job.status}</Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>job try</Table.Td>
                        <Table.Td>{job.job_try}</Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>success</Table.Td>
                        <Table.Td>{String(job.success)}</Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>enqueue time</Table.Td>
                        <Table.Td>
                          {format(job.enqueue_time, "yyyy-MM-dd HH:mm:ss")}
                        </Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>start time</Table.Td>
                        <Table.Td>
                          {job.start_time &&
                            format(job.start_time, "yyyy-MM-dd HH:mm:ss")}
                        </Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>finish time</Table.Td>
                        <Table.Td>
                          {job.finish_time &&
                            format(job.finish_time, "yyyy-MM-dd HH:mm:ss")}
                        </Table.Td>
                      </Table.Tr>
                      <Table.Tr>
                        <Table.Td>execution duration (sec)</Table.Td>
                        <Table.Td>{job.execution_duration}</Table.Td>
                      </Table.Tr>
                    </Table.Tbody>
                  </Table>
                </Box>
                <Box>
                  {job.is_abortable() && (
                    <>
                      <Button
                        onClick={() => rootStore.abortJob(job.id)}
                        loading={job.abort_status === AbortStatus.InProgress}
                        disabled={job.abort_status === AbortStatus.Completed}
                      >
                        Abort job
                      </Button>
                      <Space h="xl" />
                    </>
                  )}
                  args:
                  <Code block mt={10} mah={200}>
                    {job.args}
                  </Code>
                  <br />
                  kwargs:
                  <Code block mt={10} mah={200}>
                    {(() => {
                      try {
                        return JSON.stringify(JSON.parse(job.kwargs), null, 2);
                      } catch (e) {
                        return job.kwargs;
                      }
                    })()}
                  </Code>
                  <br />
                  result:
                  <Code block mt={10} mah={500}>
                    {(() => {
                      try {
                        return JSON.stringify(JSON.parse(job.result), null, 2);
                      } catch (e) {
                        return job.result;
                      }
                    })()}
                  </Code>
                  <br />
                </Box>
              </SimpleGrid>
            </Paper>
          </div>
        </Table.Td>
      </Table.Tr>
    </React.Fragment>
  ));

  return (
    <>
      <ScrollArea>
        <Box pos="relative" miw={900}>
          <LoadingOverlay
            visible={rootStore.isLoading}
            zIndex={200}
            overlayProps={{ radius: "sm", blur: 1 }}
          />
          <Paper withBorder p="md" radius="md">
            <Table
              highlightOnHover
              horizontalSpacing="md"
              verticalSpacing="lg"
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
                  <Th
                    onSort={() => rootStore.setSortBy("id")}
                    key="id"
                    name="id"
                  >
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
                </Table.Tr>
              </Table.Tbody>
              <Table.Tbody>{rows}</Table.Tbody>
            </Table>
          </Paper>
        </Box>
      </ScrollArea>
      <Space h="md" />
      <Center>
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
