import { Box, Stack } from "@mui/material";
import { useQuery } from "@tanstack/react-query";
import GitHubButton from "./components/GitHubButton";
import ThemePicker from "./components/ThemePicker";
import { getRoot } from "./services/fastapi.service";

function Container() {
  const test = useQuery({
    queryKey: ["test"],
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
      <Stack alignItems="center" justifyContent="space-between" padding={2}>
        {test.data}
      </Stack>
    </Box>
  );
}

export default Container;
