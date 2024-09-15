document.addEventListener('DOMContentLoaded', function() {
    const body = document.querySelector('body'),
        sidebar = body.querySelector('nav'),
        toggle = body.querySelector(".toggle"),
        mainContent = body.querySelector(".main-content"),
        searchBtn = body.querySelector(".search-box");
  
    // Fonction pour ajuster la largeur du contenu principal
    function adjustMainContent() {
        if (sidebar.classList.contains("close")) {
            mainContent.style.marginLeft = "75px";  // Largeur quand la sidebar est fermée
            mainContent.style.width = "calc(100% - 75px)";
        } else {
            mainContent.style.marginLeft = "270px";  // Largeur quand la sidebar est ouverte
            mainContent.style.width = "calc(100% - 270px)";
        }
    }
  
    // Appel initial pour régler selon l'état initial de la sidebar
    adjustMainContent();
  
    toggle.addEventListener("click", () => {
        sidebar.classList.toggle("close");
        toggle.classList.toggle("bx-chevron-right");
        toggle.classList.toggle("bx-chevron-left");
        adjustMainContent();  // Ajuster chaque fois que la sidebar est ouverte/fermée
    });
  
    searchBtn.addEventListener("click", () => {
        sidebar.classList.remove("close");
        adjustMainContent();  // Assurer que la sidebar est ouverte et ajuster
    });
  });