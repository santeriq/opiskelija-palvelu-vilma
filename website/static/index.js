function acceptRequest(username) {
    fetch("/accept-request", {
      method: "POST",
      body: JSON.stringify({ username: username }),
    }).then((_res) => {
      window.location.href = "/view-role-requests";
    });
  }


function rejectRequest(username) {
    fetch("/reject-request", {
      method: "POST",
      body: JSON.stringify({ username: username }),
    }).then((_res) => {
      window.location.href = "/view-role-requests";
    });
  }