document.querySelectorAll(".btn-detail").forEach(btn => {
  btn.addEventListener("click", () => {
    const row = btn.closest("tr");
    const id = row.dataset.id;
    fetch(`/moderation/events/${id}/`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("eventUser").textContent = data.user;
        document.getElementById("eventName").textContent = data.event;
        document.getElementById("eventDate").textContent = data.registered_at;
        document.getElementById("eventStatus").textContent = data.status;
        document.getElementById("eventModal").classList.remove("hidden");

        document.getElementById("btnApprove").onclick = () => updateStatus(id, "approve");
        document.getElementById("btnReject").onclick = () => updateStatus(id, "reject");
      });
  });
});

function updateStatus(id, action) {
  fetch(`/moderation/events/${id}/action/`, {
    method: "POST",
    headers: { "X-CSRFToken": getCSRFToken() },
    body: new URLSearchParams({ action })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      document.querySelector(`tr[data-id="${id}"] .status`).textContent = data.new_status;
      document.getElementById("eventModal").classList.add("hidden");
    }
  });
}

function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

document.getElementById("btnCloseEvent").onclick = () => {
  document.getElementById("eventModal").classList.add("hidden");
};
