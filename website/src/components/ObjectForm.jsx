import { useState } from "react";
import { Button, Stack, TextField } from "@mui/material";
import { useSnackbar } from "notistack";
import { uploadObject } from "../services/fastapi.service";
import { useQueryClient } from "@tanstack/react-query";

export default function ObjectForm() {
  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  const [file, setFile] = useState("");

  const handleChangeFile = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const formData = new FormData();
      formData.append("file", file);
      await uploadObject(formData);

      enqueueSnackbar(`Uploaded with success`, {
        variant: "success",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
      queryClient.invalidateQueries(["objects"]);
    } catch (e) {
      enqueueSnackbar(`Error: ${e.statusText}`, {
        variant: "error",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
    }
  };

  return (
    <Stack
      direction="row"
      justifyContent="center"
      component="form"
      onSubmit={handleSubmit}
      gap={2}
    >
      <TextField
        variant="standard"
        size="small"
        type="file"
        label="File to upload"
        onChange={handleChangeFile}
        required
      />
      <Button type="submit">Upload</Button>
    </Stack>
  );
}
