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

export function getTodos(page = 0, rowsPerPage = 100) {
  const getInfo = {
    method: "GET",
  };

  return new Promise((resolve, reject) => {
    fetch(
      `${FASTAPI_URL}/todos?limit=${rowsPerPage}&skip=${page * rowsPerPage}`,
      getInfo
    )
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function deleteTodo(todo_id) {
  const deleteInfo = {
    method: "DELETE",
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/todos/${todo_id}`, deleteInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function createTodo(label, quantity) {
  const postInfo = {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ label, quantity }),
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/todos`, postInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function uploadObject(file) {
  const postInfo = {
    method: "POST",
    headers: {
      Accept: "application/json",
    },
    body: file,
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/objects`, postInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function getObjects() {
  const getInfo = {
    method: "GET",
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/objects`, getInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}

export function deleteObject(object_name) {
  const deleteInfo = {
    method: "DELETE",
  };

  return new Promise((resolve, reject) => {
    fetch(`${FASTAPI_URL}/objects/${object_name}`, deleteInfo)
      .then((result) => {
        if (!result.ok) throw result;
        return result.json();
      })
      .then((result) => {
        resolve(result);
      })
      .catch((error) => {
        reject(error);
      });
  });
}
