 // Modal toggling logic
 document.querySelectorAll("[data-modal-target]").forEach(btn => {
    btn.addEventListener("click", () => {
      const modal = document.getElementById(btn.getAttribute("data-modal-target"));
      modal.classList.remove("hidden");
    });
 });

 document.querySelectorAll("[data-close-modal]").forEach(btn => {
    btn.addEventListener("click", () => {
      const modal = document.getElementById(btn.getAttribute("data-close-modal"));
      modal.classList.add("hidden");
    });
});