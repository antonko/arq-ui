import { Box } from "@mantine/core";
import { observer } from "mobx-react-lite";

import { rootStore } from "../stores";

export const TableJobs = observer(() => {
  const rows = rootStore.tableJobs.items?.map((row) => (
    <div key={row.id}>{row.id}</div>
  ));
  return (
    <Box>
      <h1>TableJobs</h1>
      <div>{rows}</div>
    </Box>
  );
});
