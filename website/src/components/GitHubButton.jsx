import GitHubIcon from "@mui/icons-material/GitHub";
import { IconButton } from "@mui/material";

export default function GitHubButton() {
  return (
    <IconButton
      size="large"
      target="_blank"
      href="https://github.com/juldrixx/docto-technical-case"
      sx={{ position: "absolute", left: 0, top: 0 }}
    >
      <GitHubIcon fontSize="large" />
    </IconButton>
  );
}