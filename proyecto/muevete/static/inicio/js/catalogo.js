document.addEventListener("DOMContentLoaded", () => {

    const botones = document.querySelectorAll(".btn-filtro");
    const tarjetas = document.querySelectorAll("[data-categoria]");
    const buscador = document.querySelector(".input-buscar");

    let categoriaActiva = "DEPORTIVO"; 

    
    botones.forEach(boton => {
        boton.addEventListener("click", () => {
            categoriaActiva = boton.getAttribute("data-filtro");

            
            botones.forEach(b => b.classList.remove("active"));
            boton.classList.add("active");

            aplicarFiltros();
        });
    });

  
    buscador.addEventListener("input", () => {
        aplicarFiltros();
    });

    
    function aplicarFiltros() {
        const texto = buscador.value.toLowerCase();

        tarjetas.forEach(card => {
            const categoria = card.getAttribute("data-categoria");
            const nombre = card.querySelector("h5").textContent.toLowerCase();

            const coincideCategoria = categoria === categoriaActiva;
            const coincideBusqueda = nombre.includes(texto);

            // Mostrar si cumple ambas condiciones
            if (coincideCategoria && coincideBusqueda) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    // Ejecutar filtros al cargar
    aplicarFiltros();
});
