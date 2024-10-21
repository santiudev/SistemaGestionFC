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
    var filter = input.value.toLowerCase(); // Obtener el valor del campo de búsqueda global

    // Limpiar mensaje de "No hay resultados" antes de aplicar filtros
    limpiarMensajeNoHayResultados();

    // Obtener fechas de los filtros
    var fechaInicio = document.getElementById('fechaInicio').value;
    var fechaFin = document.getElementById('fechaFin').value;
    var fechaInicioDate = fechaInicio ? convertirFecha(fechaInicio) : null;
    var fechaFinDate = fechaFin ? convertirFecha(fechaFin) : null;
    if (fechaFinDate) {
        fechaFinDate.setHours(23, 59, 59, 999); // Incluir todo el día
    }

    // Recorrer cada fila y aplicar los filtros
    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var mostrar = true;

        // Filtrar por fecha
        if (filtros['fecha'] || filtros['fechaFin']) {
            var fechaCell = convertirFecha(cells[0].innerText.trim());
            if ((filtros['fecha'] && fechaCell < convertirFecha(filtros['fecha'])) || 
                (filtros['fechaFin'] && fechaCell > convertirFecha(filtros['fechaFin']))) {
                mostrar = false;
            }
        }

        // Filtrar por tipo (Ingreso/Salida)
        if (filtros['tipo'] && filtros['tipo'] !== '' && !cells[1].innerText.toLowerCase().includes(filtros['tipo'])) {
            mostrar = false;
        }

        // Filtrar por categoría
        if (filtros['categoria'] && filtros['categoria'] !== 'todas' && !cells[2].innerText.toLowerCase().includes(filtros['categoria'])) {
            mostrar = false;
        }

        // Filtrar por monto
        if (filtros['monto'] && filtros['monto'] !== '') {
            var montoDesde = parseFloat(document.getElementById('montoDesde').value) || null;
            var montoHasta = parseFloat(document.getElementById('montoHasta').value) || null;
            var montoCell = parseFloat(cells[3].innerText.replace(/,/g, ''));
            if ((montoDesde !== null && montoCell < montoDesde) || (montoHasta !== null && montoCell > montoHasta)) {
                mostrar = false;
            }
        }

        // Filtrar por moneda
        if (filtros['moneda'] && filtros['moneda'] !== 'todos' && !cells[4].innerText.toLowerCase().includes(filtros['moneda'])) {
            mostrar = false;
        }

        // Filtrar por patente
        if (filtros['patente'] && filtros['patente'] !== '' && !cells[5].innerText.toLowerCase().includes(filtros['patente'])) {
            mostrar = false;
        }

        // Filtrar por medio de pago
        if (filtros['medio_pago'] && filtros['medio_pago'] !== 'todos' && !cells[6].innerText.toLowerCase().includes(filtros['medio_pago'])) {
            mostrar = false;
        }

        // Filtrar por búsqueda global
        if (filter && !Array.from(cells).some(cell => cell.innerText.toLowerCase().includes(filter))) {
            mostrar = false;
        }

        // Mostrar u ocultar la fila según el resultado de los filtros
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

    // Actualizar los íconos de los filtros activos
    actualizarEstadoIconosFiltros();
}

// Función para actualizar el estado de los íconos de filtro
function actualizarEstadoIconosFiltros() {
    Object.keys(filtros).forEach(columna => {
        var filterBtn = document.querySelector(`.filter-btn[data-column="${columna}"]`);
        if (filtros[columna] && filtros[columna] !== '' && filtros[columna] !== 'todos') {
            filterBtn.classList.add('active'); // Agregar clase activa si hay un valor
        } else {
            filterBtn.classList.remove('active'); // Remover clase activa si no hay valor
        }
    });
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

function filtrarPorRangoMonto() {
    var montoDesde = document.getElementById('montoDesde').value;
    var montoHasta = document.getElementById('montoHasta').value;

    // Convertir los valores de los montos a número
    montoDesde = montoDesde ? parseFloat(montoDesde) : null;
    montoHasta = montoHasta ? parseFloat(montoHasta) : null;

    var table = document.getElementById('tablaMovimientos');
    var rows = table.getElementsByTagName('tr');
    var hayResultados = false;

    // Limpiar el mensaje de "No hay resultados" antes de aplicar el filtro
    limpiarMensajeNoHayResultados();

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var mostrar = true;

        // Obtener el valor del monto de la celda
        var montoCell = parseFloat(cells[3].innerText.replace(/,/g, '')); // Convertir el monto a número (eliminar comas)

        // Verificar si el monto está dentro del rango
        if ((montoDesde !== null && montoCell < montoDesde) || (montoHasta !== null && montoCell > montoHasta)) {
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
    // Si el valor es vacío, eliminamos el filtro
    if (valor === '') {
        delete filtros[columna]; // Eliminar el filtro si no hay valor
    } else {
        filtros[columna] = valor.toLowerCase(); // Mantener el filtro existente
    }
    aplicarFiltros(); // Aplicar todos los filtros

    // Cambiar el estado del ícono de filtro
    var filterBtn = document.querySelector(`.filter-btn[data-column="${columna}"]`);
    if (valor) {
        filterBtn.classList.add('active'); // Agregar clase activa si hay un valor
    } else {
        filterBtn.classList.remove('active'); // Remover clase activa si no hay valor
    }
}

// Función para mostrar el filtro como popup fijo
function mostrarFiltroPopup(event, filtroId) {
    // Oculta todos los demás popups primero
    document.querySelectorAll('.filter-popup').forEach(popup => {
        if (!popup.classList.contains('d-none')) {
            popup.classList.add('d-none');
        }
    });

    // Muestra el filtro solicitado como un popup flotante
    const filtro = document.getElementById(filtroId);
    if (filtro.classList.contains('d-none')) {
        filtro.classList.remove('d-none');
        filtro.style.position = 'fixed'; // Cambia a posición fija
        filtro.style.top = `${event.clientY + window.scrollY}px`; // Ajusta la posición respecto al viewport
        filtro.style.left = `${event.clientX}px`; // Ajusta la posición horizontal
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

function convertirFecha(fechaString) {
    // Si la fecha está en formato 'YYYY-MM-DD'
    if (fechaString.includes('-')) {
        let partes = fechaString.split('-');
        return new Date(partes[0], partes[1] - 1, partes[2]); // Año, Mes (0-based), Día
    } 

    // Si la fecha está en formato 'D/M/YYYY'
    if (fechaString.includes('/')) {
        let partes = fechaString.split('/');
        return new Date(partes[2], partes[1] - 1, partes[0]); // Año, Mes (0-based), Día
    }

    return null; // Retornar null si no cumple ninguno de los formatos
}

function filtrarPorRangoFechas() {
    // Capturar los valores de fecha
    var fechaInicio = document.getElementById('fechaInicio').value;
    var fechaFin = document.getElementById('fechaFin').value;

    // Convertir las fechas de entrada a objetos Date usando convertirFecha()
    var fechaInicioDate = fechaInicio ? convertirFecha(fechaInicio) : null;
    var fechaFinDate = fechaFin ? convertirFecha(fechaFin) : null;

    // Ajustar la fecha final para incluir todo el día hasta las 23:59:59
    if (fechaFinDate) {
        fechaFinDate.setHours(23, 59, 59, 999);
    }

    var table = document.getElementById('tablaMovimientos');
    var rows = table.getElementsByTagName('tr');
    var hayResultados = false;

    // Limpiar el mensaje de "No hay resultados" antes de aplicar el filtro
    limpiarMensajeNoHayResultados();

    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var mostrar = true;

        // Obtener la fecha de la celda y convertirla usando convertirFecha
        var fechaTexto = cells[0].innerText.trim(); // Asegurarse de eliminar espacios innecesarios
        var fechaCell = convertirFecha(fechaTexto);

        // Verificar si la fecha está dentro del rango
        if (fechaInicioDate && fechaCell < fechaInicioDate) {
            mostrar = false;
        }
        if (fechaFinDate && fechaCell > fechaFinDate) {
            mostrar = false;
        }

        // Mostrar u ocultar la fila en función de si se cumple el criterio
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

function reiniciarFiltros() {
    // Limpiar el filtro de búsqueda global
    document.getElementById('filtroTabla').value = '';

    // Limpiar todos los campos de filtro individuales (fechas, tipo, categoría, etc.)
    document.getElementById('fechaInicio').value = '';
    document.getElementById('fechaFin').value = '';
    document.getElementById('montoDesde').value = '';
    document.getElementById('montoHasta').value = '';
    
    // Limpiar selectores
    document.querySelectorAll('select').forEach(select => select.value = '');

    // Reiniciar los íconos de filtros
    document.querySelectorAll('.filter-btn i').forEach(icono => {
        icono.classList.remove('text-dark');  // Elimina el color oscuro de los iconos
        icono.classList.add('text-secondary'); // Retorna a su estado inicial
    });

    // Limpia el objeto de filtros
    filtros = {
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

    // Volver a mostrar todas las filas de la tabla
    aplicarFiltros();
}

