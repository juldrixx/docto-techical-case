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
import { getBucketType, getRoot } from "./services/fastapi.service";
import TodoList from "./components/TodoList";
import TodoForm from "./components/TodoForm";
import ObjectForm from "./components/ObjectForm";
import ObjectList from "./components/ObjectList";

function Container() {
  const [tab, setTab] = useState(0);

  const apiMessage = useQuery({
    queryKey: ["apiMessage"],
    queryFn: () => getRoot(),
  });

  const bucketType = useQuery({
    queryKey: ["bucketType"],
    queryFn: () => getBucketType(),
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
          <Tab
            label={bucketType.data?.bucket_type ?? "Object"}
            disabled={!bucketType.data?.bucket_type}
          />
        </Tabs>
        <Stack width="80%" padding={2} gap={2}>
          {tab === 0 ? (
            <>
              <TodoForm />
              <TodoList />
            </>
          ) : (
            <>
              <ObjectForm />
              <ObjectList />
            </>
          )}
        </Stack>
      </Stack>
    </Box>
  );
}

export default Container;
