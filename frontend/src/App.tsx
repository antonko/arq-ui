import {
  ColorSchemeScript,
  MantineProvider,
  Stack,
  Container,
} from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { useEffect } from "react";

import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";
import Header from "./components/header";
import { TableJobs } from "./components/tablejobs";
import { rootStore } from "./stores";

function App() {
  useEffect(() => {
    rootStore.loadData();
  }, []);
  return (
    <>
      <ColorSchemeScript defaultColorScheme="auto" />
      <MantineProvider
        defaultColorScheme="auto"
        theme={{ primaryColor: "gray" }}
      >
        <Notifications />
        <Container size="xl">
          <Stack mih={"100vh"}>
            <Header />
            <TableJobs />
          </Stack>
        </Container>
      </MantineProvider>
    </>
  );
}

export default App;
