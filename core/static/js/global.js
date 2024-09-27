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

    // Inicializa los dropdowns de Bootstrap
    var dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(function(dropdown) {
        new bootstrap.Dropdown(dropdown);
    });
});