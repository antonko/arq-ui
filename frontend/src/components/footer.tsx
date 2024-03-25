import { Container, Group, ActionIcon, rem, Text, Anchor } from "@mantine/core";
import { IconBrandGithub } from "@tabler/icons-react";

import classes from "./footer.module.css";
function Footer() {
  return (
    <footer className={classes.footer}>
      <Container size="xl" className={classes.afterFooter}>
        <Text c="dimmed" size="sm">
          © Anton Kovalev
        </Text>
        <Group
          gap={0}
          className={classes.social}
          justify="flex-end"
          wrap="nowrap"
        >
          <Anchor href="https://github.com/antonko/arq-ui" target="_blank">
            <ActionIcon size="lg" color="gray" variant="subtle">
              <IconBrandGithub
                style={{ width: rem(18), height: rem(18) }}
                stroke={1.5}
              />
            </ActionIcon>
          </Anchor>
        </Group>
      </Container>
    </footer>
  );
}

export default Footer;
