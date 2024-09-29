import { Box, LinearProgress, Stack, Typography } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import GitHubButton from "./components/GitHubButton";
import ThemePicker from "./components/ThemePicker";
import { getRoot } from "./services/fastapi.service";
import TodoList from "./components/TodoList";
import TodoForm from "./components/TodoForm";

function Container() {
  const apiMessage = useQuery({
    queryKey: ["apiMessage"],
    queryFn: () => getRoot(),
  });

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
        <Stack width="80%" padding={2} gap={2}>
          <TodoForm />
          <TodoList />
        </Stack>
      </Stack>
    </Box>
  );
}

export default Container;
