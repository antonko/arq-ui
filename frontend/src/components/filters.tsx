import {
  ActionIcon,
  CloseButton,
  Grid,
  MultiSelect,
  Select,
  TextInput,
  rem,
} from "@mantine/core";
import { IconSearch } from "@tabler/icons-react";
import { observer } from "mobx-react-lite";

import { rootStore } from "../stores";

export const Filters = observer(() => {
  return (
    <Grid>
      <Grid.Col span="auto">
        <Select
          multiple={false}
          placeholder="Function"
          data={rootStore.functions}
          value={rootStore.filterJobs.function}
          onChange={(value) => {
            rootStore.setFilterFunction(value);
          }}
        />
      </Grid.Col>
      <Grid.Col span="auto">
        <MultiSelect
          placeholder="Status"
          data={["deferred", "queued", "in_progress", "complete", "not_found"]}
          defaultValue={[]}
          clearable
          value={rootStore.filterJobs.status}
          onChange={(value) => {
            rootStore.setFilterStatus(value);
          }}
        />
      </Grid.Col>
      <Grid.Col span="auto">
        <TextInput
          placeholder="Search"
          miw="228px"
          value={rootStore.filterJobs.search}
          leftSection={
            <IconSearch
              style={{ width: rem(16), height: rem(16) }}
              stroke={1.5}
            />
          }
          onChange={(event) => {
            rootStore.setFilterSearch(event.currentTarget.value);
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              rootStore.loadData();
            }
          }}
          rightSectionPointerEvents="all"
          rightSection={
            <CloseButton
              aria-label="Clear input"
              onClick={() => {
                rootStore.setFilterSearch("");
                rootStore.loadData();
              }}
              style={{
                display: rootStore.filterJobs.search.length ? "flex" : "none",
              }}
            />
          }
        />
      </Grid.Col>
      <Grid.Col span="content">
        <ActionIcon
          variant="default"
          size="lg"
          aria-label="Toggle color scheme"
          onClick={() => {
            rootStore.loadData();
          }}
        >
          <IconSearch stroke={1.5} size={20} />
        </ActionIcon>
      </Grid.Col>
    </Grid>
  );
});
