import {
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
import { useQuery } from "@tanstack/react-query";
import { useSnackbar } from "notistack";
import { deleteObject, getObjects } from "../services/fastapi.service";

export default function S3ObjectList() {
  const { enqueueSnackbar } = useSnackbar();

  const s3Objects = useQuery({
    queryKey: ["s3_objects"],
    queryFn: () => getObjects(),
  });

  const handleClickDelete = async (object_name) => {
    try {
      await deleteObject(object_name);
      enqueueSnackbar(`Deleted with success`, {
        variant: "success",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
      s3Objects.refetch();
    } catch (e) {
      enqueueSnackbar(`Error: ${e.statusText}`, {
        variant: "error",
        anchorOrigin: { horizontal: "right", vertical: "bottom" },
      });
    }
  };

  if (s3Objects.isFetching) return <CircularProgress />;

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
            {s3Objects.data.files.length === 0 ? (
              <TableRow>
                <TableCell colSpan={3} align="center">
                  <Typography fontWeight={700}>No object</Typography>
                </TableCell>
              </TableRow>
            ) : (
              s3Objects.data.files.map(({ name, path }) => (
                <TableRow key={name}>
                  <TableCell>{name}</TableCell>
                  <TableCell>{path}</TableCell>
                  <TableCell align="right">
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
