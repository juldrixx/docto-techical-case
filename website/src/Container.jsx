import { useState } from "react";
import {
  Box,
  LinearProgress,
  Stack,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import GitHubButton from "./components/GitHubButton";
import ThemePicker from "./components/ThemePicker";
import { getRoot } from "./services/fastapi.service";
import TodoList from "./components/TodoList";
import TodoForm from "./components/TodoForm";
import S3ObjectForm from "./components/S3ObjectForm";
import S3ObjectList from "./components/S3ObjectList";

function Container() {
  const [tab, setTab] = useState(0);

  const apiMessage = useQuery({
    queryKey: ["apiMessage"],
    queryFn: () => getRoot(),
  });

  const handleChangeTab = (_, newTab) => {
    setTab(newTab);
  };

  return (
    <Box
      width="100%"
      height="100%"
      bgcolor={(theme) => theme.palette.background.paper}
      overflow="hidden auto"
    >
      <ThemePicker />
      <GitHubButton />
      <Stack
        alignItems="center"
        justifyContent="space-between"
        padding={2}
        gap={2}
      >
        {apiMessage.isLoading ? (
          <LinearProgress sx={{ width: "80%" }} />
        ) : (
          <Typography>{apiMessage.data}</Typography>
        )}
        <Tabs value={tab} onChange={handleChangeTab}>
          <Tab label="Todo" />
          <Tab label="S3" />
        </Tabs>
        <Stack width="80%" padding={2} gap={2}>
          {tab === 0 ? (
            <>
              <TodoForm />
              <TodoList />
            </>
          ) : (
            <>
              <S3ObjectForm />
              <S3ObjectList />
            </>
          )}
        </Stack>
      </Stack>
    </Box>
  );
}

export default Container;
