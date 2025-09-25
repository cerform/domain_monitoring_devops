document.addEventListener('DOMContentLoaded', function () {
  // =======================
  // Utility Functions
  // =======================
  function showStatus(el, message, isSuccess) {
    if (!el) return;
    el.textContent = message;
    el.classList.remove("status-success", "status-error");
    el.classList.add(isSuccess ? "status-success" : "status-error");
  }

  function openModal(modal) {
    if (modal) modal.style.display = "flex";
  }

  function closeModal(modal) {
    if (modal) modal.style.display = "none";
  }

  // =======================
  // Global Elements
  // =======================
  fetch('/get_username', { credentials: 'same-origin' })
    .then(res => res.json())
    .then(data => {
      const username = data.username;

  const greeting = document.getElementById("greeting");
  const addDomainModal = document.getElementById("addDomainModal");
  const openAddDomainBtn = document.getElementById("openAddDomain");
  const addDomainForm = document.getElementById("addDomainForm");
  const addDomainStatus = document.getElementById("addDomainStatus");

  const bulkUploadModal = document.getElementById("bulkUploadModal");
  const openBulkUploadBtn = document.getElementById("openBulkUpload");
  const bulkUploadForm = document.getElementById("bulkUploadForm");
  const bulkUploadStatus = document.getElementById("bulkUploadStatus");

  const deleteDomainModal = document.getElementById("deleteDomainModal");
  const deleteDomainText = document.getElementById("deleteDomainText");
  const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");
  const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");

  const bulkActions = document.querySelector(".bulk-actions");
  const selectAllCheckbox = document.getElementById("selectAll");
  let domainsToDelete = [];

  const scanNowBtn = document.getElementById("scanNowBtn");
  // =======================
  // Initialize Greeting
  // =======================
  if (greeting && username) {
    greeting.textContent = `Hello ${username}!`;
  }
  // =======================
  // Add Domain Modal
  // =======================
  openAddDomainBtn?.addEventListener("click", () => {
    openModal(addDomainModal);
    addDomainForm.reset();
    addDomainStatus.textContent = "";
  });

  addDomainForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const domain = document.getElementById("domainInput").value.trim();
    showStatus(addDomainStatus, "Adding...", true);

    try {
      const res = await fetch("/add_domain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domain }),
      });
      const result = await res.json();
      if (result.ok) {
        showStatus(addDomainStatus, result.message, true);
        setTimeout(() => {
          closeModal(addDomainModal);
          location.reload();
        }, 1200);
      } else {
        showStatus(addDomainStatus, result.error, false);
      }
    } catch {
      showStatus(addDomainStatus, "Request failed. Try again.", false);
    }
  });

  // =======================
  // Bulk Upload Modal
  // =======================
  openBulkUploadBtn?.addEventListener("click", () => {
    openModal(bulkUploadModal);
    bulkUploadForm.reset();
    bulkUploadStatus.textContent = "";
  });

  bulkUploadForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(bulkUploadForm);
    showStatus(bulkUploadStatus, "Uploading...", true);

    try {
      const res = await fetch("/bulk_upload", { method: "POST", body: formData });
      const result = await res.json();
      if (result.ok) {
        showStatus(bulkUploadStatus, result.message, true);
        setTimeout(() => {
          closeModal(bulkUploadModal);
          location.reload();
        }, 1500);
      } else {
        showStatus(bulkUploadStatus, result.error, false);
      }
    } catch {
      showStatus(bulkUploadStatus, "Upload failed. Try again.", false);
    }
  });

  // =======================
  // Delete Logic
  // =======================
  function openDeleteModal(domains, message) {
    domainsToDelete = domains;
    deleteDomainText.textContent = message;
    openModal(deleteDomainModal);
  }

  function attachDeleteHandlers() {
    document.querySelectorAll(".delete-domain-btn").forEach((btn) => {
      btn.onclick = () => {
        const domain = btn.getAttribute("data-domain");
        openDeleteModal([domain], `Delete '${domain}'?`);
      };
    });
  }
  attachDeleteHandlers();

  document.getElementById("bulkDeleteBtn")?.addEventListener("click", () => {
    const checked = Array.from(document.querySelectorAll(".select-domain:checked"));
    if (!checked.length) return alert("No domains selected!");
    const domains = checked.map((cb) => cb.value);
    openDeleteModal(domains, `Delete ${domains.length} domain(s)?`);
  });

  document.getElementById("deleteAllBtn")?.addEventListener("click", () => {
    const all = Array.from(document.querySelectorAll(".select-domain")).map((cb) => cb.value);
    if (!all.length) return alert("No domains available!");
    openDeleteModal(all, `Delete ALL ${all.length} domains?`);
  });

  cancelDeleteBtn?.addEventListener("click", () => {
    closeModal(deleteDomainModal);
    domainsToDelete = [];
  });

  confirmDeleteBtn?.addEventListener("click", async () => {
    if (!domainsToDelete.length) return;

    try {
      const response = await fetch("/delete_domain", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ domains: domainsToDelete }),
      });
      const result = await response.json();

      if (result.ok) {
        domainsToDelete.forEach((domain) => {
          document.querySelector(`.select-domain[value="${domain}"]`)?.closest("tr")?.remove();
        });
      } else {
        alert(result.error);
      }
    } catch {
      alert("Failed to delete domains.");
    }
    closeModal(deleteDomainModal);
    domainsToDelete = [];
  });

  // =======================
  // Checkbox Logic
  // =======================
  function attachCheckboxHandlers() {
    document.querySelectorAll(".select-domain").forEach((cb) => {
      cb.onchange = toggleBulkActions;
    });

    selectAllCheckbox?.addEventListener("change", () => {
      const allChecks = document.querySelectorAll(".select-domain");
      allChecks.forEach((cb) => (cb.checked = selectAllCheckbox.checked));
      toggleBulkActions();
    });
  }

  function toggleBulkActions() {
    const anyChecked = document.querySelectorAll(".select-domain:checked").length > 0;
    bulkActions.style.display = anyChecked ? "flex" : "none";
  }
  attachCheckboxHandlers();
  toggleBulkActions();

  // =======================
  // Scan Now
  // =======================
  scanNowBtn?.addEventListener("click", async () => {
    scanNowBtn.disabled = true;
    scanNowBtn.textContent = "Scanning...";
    try {
      await fetch("/scan_domains");
      location.reload();
    } catch {
      alert("Scan failed.");
    } finally {
      scanNowBtn.disabled = false;
      scanNowBtn.textContent = "Scan Now";
    }
  });

  // =======================
  // Modal Closing
  // =======================
  document.querySelectorAll(".modal .close").forEach((btn) => {
    btn.addEventListener("click", () => closeModal(btn.closest(".modal")));
  });
  window.addEventListener("click", (e) => {
    if (e.target.classList.contains("modal")) closeModal(e.target);
  });
});
});