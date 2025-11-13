document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector(".input-buscar");
    const cards = document.querySelectorAll(".card-coche");

    searchInput.addEventListener("input", () => {
      const query = searchInput.value.toLowerCase();

      cards.forEach(card => {
        const title = card.querySelector("h5").textContent.toLowerCase();
        card.style.display = title.includes(query) ? "" : "none";
      });
    });
  });

