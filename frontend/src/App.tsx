import { useEffect } from "react";

import "./App.css";
import "./index.css";
import { TableLogs } from "./components/tablejobs/tablejobs";
import { rootStore } from "./stores";
function App() {
  useEffect(() => {
    rootStore.loadData();
  }, []);
  return (
    <>
      <h1>arq UI</h1>
      <TableLogs />
    </>
  );
}

export default App;
