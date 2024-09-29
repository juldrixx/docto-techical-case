const FASTAPI_URL =
  process.env.REACT_APP_FASTAPI_URL || "REACT_APP_FASTAPI_URL_PLACEHOLDER";

export function getRoot() {
  const getInfo = {
    method: "GET",
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/`, getInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.text();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
