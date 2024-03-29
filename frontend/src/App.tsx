import {
  ColorSchemeScript,
  MantineProvider,
  Stack,
  Container,
  Space,
  Box,
  Flex,
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
import { TimeLine } from "./components/timeline";
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
        <Flex mih={"100vh"} direction="column">
          <Box style={{ flexGrow: 1 }}>
            <Header />
            <Space h="xl" />
            <Container size="xl">
              <Stack gap="xl">
                <Space h="xs" />
                <Statistics />
                <Space h="xs" />
                <TimeLine />
                <Filters />
                <TableJobs />
              </Stack>
            </Container>
          </Box>
          <Footer />
        </Flex>
      </MantineProvider>
    </>
  );
}

export default App;
