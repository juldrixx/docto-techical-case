import { useState } from "react";
import {
  Box,
  CircularProgress,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  Typography,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { useQuery } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import { deleteTodo, getTodos } from "../services/fastapi.service";

export default function TodoList() {
  const { enqueueSnackbar } = useSnackbar();

  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [page, setPage] = useState(0);

  const todos = useQuery({
    queryKey: ["todos", rowsPerPage, page],
    queryFn: () => getTodos(page, rowsPerPage),
  });

  const handleChangePage = (_, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleClickDelete = async (todo_id) => {
    try {
      await deleteTodo(todo_id);
      enqueueSnackbar(`Deleted with success`, {
        variant: "success",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
      todos.refetch();
      setPage(0);
    } catch (e) {
      enqueueSnackbar(`Error: ${e.statusText}`, {
        variant: "error",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
    }
  };

  if (todos.isLoading)
    return (
      <Box width="100%" textAlign="center">
        <CircularProgress />
      </Box>
    );

  return (
    <Paper sx={{ width: "100%", mb: 2 }}>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Identifier</TableCell>
              <TableCell>Label</TableCell>
              <TableCell align="right">Quantity</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {todos.data.total === 0 ? (
              <TableRow>
                <TableCell colSpan={4} align="center">
                  <Typography fontWeight={700}>No data</Typography>
                </TableCell>
              </TableRow>
            ) : (
              todos.data.todos.map(({ id, label, quantity }) => (
                <TableRow key={id}>
                  <TableCell>{id}</TableCell>
                  <TableCell>{label}</TableCell>
                  <TableCell align="right">{quantity}</TableCell>
                  <TableCell align="right">
                    <IconButton onClick={() => handleClickDelete(id)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        rowsPerPageOptions={[1, 5, 10]}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        count={todos.data.total}
      />
    </Paper>
  );
}
