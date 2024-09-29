import { useState } from "react";
import { Button, Stack, TextField } from "@mui/material";
import { useSnackbar } from "notistack";
import { createTodo } from "../services/fastapi.service";
import { useQueryClient } from "@tanstack/react-query";

export default function TodoForm() {
  const queryClient = useQueryClient();
  const { enqueueSnackbar } = useSnackbar();

  const [label, setLabel] = useState("");
  const [quantity, setQuantity] = useState(0);

  const handleChangeLabel = (event) => {
    setLabel(event.target.value);
  };

  const handleChangeQuantity = (event) => {
    setQuantity(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await createTodo(label, quantity);

      enqueueSnackbar(`Created with success`, {
        variant: "success",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
      queryClient.invalidateQueries(["todos"]);
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
        type="text"
        label="Label"
        autoComplete="label"
        value={label}
        onChange={handleChangeLabel}
        required
      />
      <TextField
        variant="standard"
        size="small"
        type="number"
        label="Quantity"
        autoComplete="quantity"
        value={quantity}
        onChange={handleChangeQuantity}
        required
      />
      <Button type="submit">Add</Button>
    </Stack>
  );
}
