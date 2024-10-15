document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.js-sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('.main-content');
    const arrow = document.querySelector('.arrow'); // Selecciona la flecha

    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed'); // Cambiar a 'collapsed'
        navbar.classList.toggle('navbar-collapsed');
        mainContent.classList.toggle('main-content-collapsed');
        
        // Alternar la rotación de la flecha
        arrow.classList.toggle('rotated'); // Asegúrate de que esta clase esté definida en CSS
    });

    // Inicializa los dropdowns de Bootstrap
    var dropdowns = document.querySelectorAll('.dropdown-toggle');
    dropdowns.forEach(function(dropdown) {
        new bootstrap.Dropdown(dropdown);
    });

    // Mantener el dropdown abierto si la URL coincide
    const currentUrl = window.location.href;
    const dropdownLinks = document.querySelectorAll('.sidebar-item a');

    dropdownLinks.forEach(link => {
        link.addEventListener('click', function() {
            const dropdown = link.closest('.sidebar-dropdown');

            // Cerrar otros dropdowns
            const allDropdowns = document.querySelectorAll('.sidebar-dropdown');
            allDropdowns.forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove('show'); // Cerrar otros dropdowns
                    const arrow = d.previousElementSibling.querySelector('.arrow');
                    if (arrow) {
                        arrow.classList.remove('rotated'); // Rotar la flecha hacia abajo
                    }
                }
            });

            // Alternar el dropdown actual
            if (dropdown) {
                dropdown.classList.add('show'); // Asegurarse de que el dropdown actual esté abierto
                const arrow = link.querySelector('.arrow');
                if (arrow) {
                    arrow.classList.add('rotated'); // Asegurarse de que la flecha esté girada
                }
            }
        });

        // Mantener el dropdown abierto si la URL coincide
        if (link.href === currentUrl) {
            const dropdown = link.closest('.sidebar-dropdown');
            if (dropdown) {
                dropdown.classList.add('show'); // Mantener el dropdown abierto
                link.classList.add('active'); // Marcar el enlace como activo
                const arrow = link.querySelector('.arrow');
                if (arrow) {
                    arrow.classList.add('rotated'); // Asegúrate de que la flecha esté girada
                }
            }
            // Marcar el item padre como activo
            const parentItem = link.closest('.sidebar-item');
            if (parentItem) {
                parentItem.classList.add('active'); // Asegúrate de que el item padre esté activo
            }
        }
    });
});
document.getElementById('edit-button').addEventListener('click', function() {
    var input = document.querySelector('input[name="valor_cotizacion"]');
    input.removeAttribute('readonly');  // Habilitar el campo de entrada
    input.focus();  // Enfocar el campo de entrada
    document.getElementById('submit-button').style.display = 'inline-block';  // Mostrar el botón de actualizar
    this.style.display = 'none';  // Ocultar el botón de editar
});
document.addEventListener("DOMContentLoaded", function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
    });
    toastList.forEach(toast => toast.show());
});
