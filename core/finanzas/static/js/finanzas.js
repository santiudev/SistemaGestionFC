// Función para filtrar la tabla según el texto introducido en el campo de búsqueda
function filtrarTabla() {
    // Llama a aplicarFiltros para que se apliquen todos los filtros
    aplicarFiltros();
}

// Función para aplicar todos los filtros
function aplicarFiltros() {
    var table = document.getElementById('tablaMovimientos');
    var rows = table.getElementsByTagName('tr');
    var hayResultados = false; // Variable para verificar si hay resultados
    var input = document.getElementById('filtroTabla');
    var filter = input.value.toLowerCase(); // Obtener el valor del campo de búsqueda

    // Limpiar mensaje de "No hay resultados" antes de aplicar filtros
    limpiarMensajeNoHayResultados();

    // Obtener fechas de los filtros
    var fechaInicio = document.getElementById('fechaInicio').value;
    var fechaFin = document.getElementById('fechaFin').value;
    var fechaInicioDate = fechaInicio ? new Date(fechaInicio) : null;
    var fechaFinDate = fechaFin ? new Date(fechaFin) : null;

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var mostrar = true;

        // Verificar filtros individuales
        if (filtros['fecha'] && !cells[0].innerText.toLowerCase().includes(filtros['fecha'])) {
            mostrar = false;
        }
        if (filtros['tipo'] && !cells[1].innerText.toLowerCase().includes(filtros['tipo'])) {
            mostrar = false;
        }
        if (filtros['categoria'] && !cells[2].innerText.toLowerCase().includes(filtros['categoria'])) {
            mostrar = false;
        }
        if (filtros['detalles'] && !cells[3].innerText.toLowerCase().includes(filtros['detalles'])) {
            mostrar = false;
        }
        if (filtros['monto'] && !cells[4].innerText.toLowerCase().includes(filtros['monto'])) {
            mostrar = false;
        }
        if (filtros['moneda'] && !cells[5].innerText.toLowerCase().includes(filtros['moneda'])) {
            mostrar = false;
        }
        if (filtros['patente'] && !cells[6].innerText.toLowerCase().includes(filtros['patente'])) {
            mostrar = false;
        }
        if (filtros['medio_pago'] && !cells[7].innerText.toLowerCase().includes(filtros['medio_pago'])) {
            mostrar = false;
        }
        if (filtros['comprobante'] && !cells[8].innerText.toLowerCase().includes(filtros['comprobante'])) {
            mostrar = false;
        }

        // Verificar el campo de búsqueda
        if (filter && !Array.from(cells).some(cell => cell.innerText.toLowerCase().includes(filter))) {
            mostrar = false;
        }

        // Verificar el rango de fechas
        var fechaCell = convertirFecha(cells[0].innerText);
        if (fechaInicioDate && fechaCell < fechaInicioDate) {
            mostrar = false;
        }
        if (fechaFinDate && fechaCell > fechaFinDate) {
            mostrar = false;
        }

        if (mostrar) {
            rows[i].style.display = '';
            hayResultados = true; // Se encontró al menos un resultado
        } else {
            rows[i].style.display = 'none';
        }
    }

    // Mostrar mensaje si no se encuentra ningún elemento
    if (!hayResultados) {
        mostrarMensajeNoHayResultados();
    }

    // Cambiar el estado del ícono de filtro de fecha
    var filterBtnFecha = document.querySelector('.filter-btn[data-column="fecha"]');
    if (fechaInicio || fechaFin) {
        filterBtnFecha.classList.add('active'); // Agregar clase activa si hay un valor
    } else {
        filterBtnFecha.classList.remove('active'); // Remover clase activa si no hay valor
    }
}

// Función para mostrar el mensaje de "No hay resultados"
function mostrarMensajeNoHayResultados() {
    var table = document.getElementById('tablaMovimientos');
    var noResultadosRow = table.insertRow(1); // Insertar en la segunda posición
    var noResultadosCell = noResultadosRow.insertCell(0);
    noResultadosCell.colSpan = 10; // Ajustar según el número de columnas
    noResultadosCell.textContent = 'No hay resultados';
    noResultadosCell.style.textAlign = 'center'; // Centrar el texto
    noResultadosRow.style.display = ''; // Asegurarse de que la fila sea visible
}

// Función para limpiar el mensaje de "No hay resultados"
function limpiarMensajeNoHayResultados() {
    var table = document.getElementById('tablaMovimientos');
    var rows = table.getElementsByTagName('tr');
    for (var i = 1; i < rows.length; i++) {
        if (rows[i].cells[0] && rows[i].cells[0].textContent === 'No hay resultados') {
            table.deleteRow(i);
            break; // Salir del bucle después de eliminar la fila
        }
    }
}

// Función para exportar la tabla a un archivo Excel con estilos usando ExcelJS
document.getElementById('exportarExcel').addEventListener('click', function () {
    var table = document.getElementById('tablaMovimientos');
    var rows = table.querySelectorAll('tbody tr');

    // Crear un nuevo libro de trabajo y hoja de trabajo
    var workbook = new ExcelJS.Workbook();
    var worksheet = workbook.addWorksheet('Lista de Movimientos');

    // Definir las columnas de la hoja de trabajo (sin la columna de estado)
    const columns = [
        { header: 'Fecha', key: 'fecha', width: 15 },
        { header: 'Tipo', key: 'tipo', width: 10 },
        { header: 'Categoría', key: 'categoria', width: 20 },
        { header: 'Detalles', key: 'detalles', width: 25 },
        { header: 'Monto', key: 'monto', width: 15 },
        { header: 'Moneda', key: 'moneda', width: 10 },
        { header: 'Patente', key: 'patente', width: 15 },
        { header: 'Medio de Pago', key: 'medio_pago', width: 20 },
        { header: 'N° Comprobante', key: 'numero_comprobante', width: 20 }
    ];

    worksheet.columns = columns;

    // Aplicar estilo al encabezado
    worksheet.getRow(1).eachCell((cell) => {
        cell.font = { bold: true, color: { argb: 'FFFFFFFF' } };
        cell.fill = {
            type: 'pattern',
            pattern: 'solid',
            fgColor: { argb: 'FF595959' }
        };
        cell.alignment = { horizontal: 'center', vertical: 'middle' };
    });

    // Recoger los datos visibles de la tabla y añadirlos a la hoja de trabajo
    rows.forEach((row) => {
        if (row.style.display !== 'none') {
            var rowData = [];
            row.querySelectorAll('td').forEach((col) => {
                rowData.push(col.textContent.trim());
            });
            if (rowData.length > 0) {
                worksheet.addRow(rowData);
            }
        }
    });

    // Aplicar estilo a las filas del cuerpo
    worksheet.eachRow((row, rowNumber) => {
        if (rowNumber !== 1) { // No aplicar estilo a la fila de encabezado
            row.eachCell((cell) => {
                cell.alignment = { horizontal: 'center', vertical: 'middle' };
                cell.border = {
                    top: { style: 'thin' },
                    left: { style: 'thin' },
                    bottom: { style: 'thin' },
                    right: { style: 'thin' }
                };
            });
        }
    });

    // Exportar el archivo Excel
    workbook.xlsx.writeBuffer().then((data) => {
        var blob = new Blob([data], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
        var url = window.URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = 'lista_movimientos.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
});


function limpiarBusqueda() {
    document.getElementById('filtroTabla').value = '';
    limpiarMensajeNoHayResultados(); // Eliminar la fila "No hay resultados"
    filtrarTabla(); // Llama a la función de filtrado para mostrar todas las filas nuevamente
}



/* FILTROS POR SEPARADOS*/ 

var filtros = {
    fecha: "",
    tipo: "",
    categoria: "",
    detalles: "",
    monto: "",
    moneda: "",
    patente: "",
    medio_pago: "",
    comprobante: ""
};

function filtrarPorColumna(columna, valor) {
    filtros[columna] = valor.toLowerCase();
    aplicarFiltros();

    // Cambiar el estado del ícono de filtro
    var filterBtn = document.querySelector(`.filter-btn[data-column="${columna}"]`);
    if (valor) {
        filterBtn.classList.add('active'); // Agregar clase activa si hay un valor
    } else {
        filterBtn.classList.remove('active'); // Remover clase activa si no hay valor
    }
}

function mostrarFiltroPopup(event, filtroId) {
    // Oculta todos los demás popups primero
    document.querySelectorAll('.filter-popup').forEach(popup => {
        if (!popup.classList.contains('d-none')) {
            popup.classList.add('d-none');
        }
    });

    // Muestra el filtro solicitado
    const filtro = document.getElementById(filtroId);
    if (filtro.classList.contains('d-none')) {
        filtro.classList.remove('d-none');
    } else {
        filtro.classList.add('d-none');
    }

    // Evita que el evento se propague al documento
    event.stopPropagation();
}

// Oculta los popups si se hace clic fuera de ellos
document.addEventListener('click', function () {
    document.querySelectorAll('.filter-popup').forEach(popup => {
        popup.classList.add('d-none');
    });
});

// Evita que el popup se cierre cuando se hace clic dentro de él
document.querySelectorAll('.filter-popup').forEach(popup => {
    popup.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});
function filtrarPorRangoFechas() {
    var fechaInicio = document.getElementById('fechaInicio').value;
    var fechaFin = document.getElementById('fechaFin').value;

    // Convertir las fechas a objetos Date
    var fechaInicioDate = fechaInicio ? new Date(fechaInicio) : null;
    var fechaFinDate = fechaFin ? new Date(fechaFin) : null;

    // Verificar si la fecha de fin es anterior a la fecha de inicio
    if (fechaInicioDate && fechaFinDate && fechaFinDate < fechaInicioDate) {
        alert("La fecha de fin no puede ser anterior a la fecha de inicio."); // Mensaje de error
        return; // Salir de la función si la condición se cumple
    }

    var table = document.getElementById('tablaMovimientos');
    var rows = table.getElementsByTagName('tr');
    var hayResultados = false;

    // Limpiar el mensaje de "No hay resultados" antes de aplicar el filtro
    limpiarMensajeNoHayResultados();

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var mostrar = true;

        // Obtener la fecha de la celda
        var fechaCell = convertirFecha(cells[0].innerText);

        // Verificar si la fecha está dentro del rango
        if (fechaInicioDate && fechaCell < fechaInicioDate) {
            mostrar = false;
        }
        if (fechaFinDate && fechaCell > fechaFinDate) {
            mostrar = false;
        }

        if (mostrar) {
            rows[i].style.display = '';
            hayResultados = true;
        } else {
            rows[i].style.display = 'none';
        }
    }

    // Mostrar mensaje si no se encuentra ningún elemento
    if (!hayResultados) {
        mostrarMensajeNoHayResultados();
    }

    // Ocultar el popup de fechas después de aplicar el filtro
    document.getElementById('filtroFecha').classList.add('d-none');
}
// Función para convertir una fecha en formato "j/n/Y" a un objeto Date
function convertirFecha(fechaStr) {
    var partes = fechaStr.split('/'); // Separar por '/'
    return new Date(partes[2], partes[1] - 1, partes[0]); // año, mes (0-11), día
}