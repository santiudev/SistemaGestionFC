document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.js-sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('.main-content');

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('sidebar-collapsed');
        navbar.classList.toggle('navbar-collapsed');
        mainContent.classList.toggle('main-content-collapsed');
    });

    // Elimina la inicialización manual de los dropdowns y los eventos personalizados
});