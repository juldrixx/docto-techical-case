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
  TableRow,
  Typography,
} from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import DownloadIcon from "@mui/icons-material/Download";
import { useQuery } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import {
  deleteObject,
  getObject,
  getObjects,
} from "../services/fastapi.service";

export default function ObjectList() {
  const { enqueueSnackbar } = useSnackbar();

  const objects = useQuery({
    queryKey: ["objects"],
    queryFn: () => getObjects(),
  });

  const handleClickDelete = async (object_name) => {
    try {
      await deleteObject(object_name);
      enqueueSnackbar(`Deleted with success`, {
        variant: "success",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
      objects.refetch();
    } catch (e) {
      enqueueSnackbar(`Error: ${e.statusText}`, {
        variant: "error",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
    }
  };

  const handleClickDownload = async (object_name) => {
    try {
      const url = await getObject(object_name);
      const a = document.createElement("a");
      a.href = url;
      a.download = object_name;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {
      enqueueSnackbar(`Error: ${e.statusText}`, {
        variant: "error",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
    }
  };

  if (objects.isLoading)
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
              <TableCell>Name</TableCell>
              <TableCell>Path</TableCell>
              <TableCell />
            </TableRow>
          </TableHead>
          <TableBody>
            {objects.data.files.length === 0 ? (
              <TableRow>
                <TableCell colSpan={3} align="center">
                  <Typography fontWeight={700}>No object</Typography>
                </TableCell>
              </TableRow>
            ) : (
              objects.data.files.map(({ name, path }) => (
                <TableRow key={name}>
                  <TableCell>{name}</TableCell>
                  <TableCell>{path}</TableCell>
                  <TableCell align="right">
                    <IconButton onClick={() => handleClickDownload(name)}>
                      <DownloadIcon />
                    </IconButton>
                    <IconButton onClick={() => handleClickDelete(name)}>
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}
