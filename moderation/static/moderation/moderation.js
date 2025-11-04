document.querySelectorAll(".btn-detail").forEach(btn => {
  btn.addEventListener("click", () => {
    const row = btn.closest("tr");
    const type = row.dataset.type;
    const id = row.dataset.id;
    fetch(`/moderation/reports/${type}/${id}/`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("modalType").textContent = data.type;
        document.getElementById("modalUser").textContent = data.user;
        document.getElementById("modalReason").textContent = data.reason;
        document.getElementById("modalDate").textContent = data.created_at;
        document.getElementById("modalStatus").textContent = data.status;
        document.getElementById("reportModal").classList.remove("hidden");
      });
  });
});
