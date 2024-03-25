import {
  ColorSchemeScript,
  MantineProvider,
  Stack,
  Container,
  Space,
} from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { useEffect } from "react";

import "@mantine/core/styles.css";
import "@mantine/notifications/styles.css";
import { Filters } from "./components/filters";
import Footer from "./components/footer";
import Header from "./components/header";
import { Statistics } from "./components/statistics";
import { TableJobs } from "./components/tablejobs";
import TimeLine from "./components/timeline";
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
        <Header />
        <Space h="xl" />
        <Container size="xl">
          <Stack mih={"100vh"}>
            <Statistics />
            <Space h="sm" />
            <TimeLine />
            <Space h="sm" />
            <Filters />
            <TableJobs />
            <Space h="lg" />
          </Stack>
        </Container>
        <Footer />
      </MantineProvider>
    </>
  );
}

export default App;
