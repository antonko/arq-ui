import { observer } from "mobx-react-lite";

import { rootStore } from "../../stores";

export const TableLogs = observer(() => {
  const rows = rootStore.tableJobs.items?.map((row) => (
    <div key={row.id}>{row.id}</div>
  ));
  return (
    <div>
      <h1>TableLogs</h1>
      <div>{rows}</div>
    </div>
  );
});
