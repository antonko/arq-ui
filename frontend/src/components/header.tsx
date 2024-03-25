import {
  ActionIcon,
  Box,
  Button,
  Group,
  useComputedColorScheme,
  useMantineColorScheme,
} from "@mantine/core";
import {
  IconSun,
  IconMoon,
  IconTimelineEventPlus,
  IconReload,
} from "@tabler/icons-react";
import cx from "clsx";

import { rootStore } from "../stores";

import classes from "./header.module.css";
function Header() {
  const { setColorScheme } = useMantineColorScheme();
  const computedColorScheme = useComputedColorScheme("light", {
    getInitialValueInEffect: true,
  });
  return (
    <header className={classes.header}>
      <Box size="xl" className={classes.inner}>
        <h2>arq UI</h2>
        <Group>
          <Button
            leftSection={<IconTimelineEventPlus size={14} />}
            variant="default"
          >
            Enqueue job
          </Button>
          <ActionIcon
            variant="default"
            size="lg"
            aria-label="Toggle color scheme"
            onClick={() => rootStore.clearFilter()}
          >
            <IconReload stroke={1.5} size={20} />
          </ActionIcon>
          <ActionIcon
            onClick={() =>
              setColorScheme(computedColorScheme === "light" ? "dark" : "light")
            }
            variant="default"
            size="lg"
            aria-label="Toggle color scheme"
          >
            <IconSun className={cx(classes.icon, classes.light)} stroke={1.5} />
            <IconMoon className={cx(classes.icon, classes.dark)} stroke={1.5} />
          </ActionIcon>
        </Group>
      </Box>
    </header>
  );
}

export default Header;
