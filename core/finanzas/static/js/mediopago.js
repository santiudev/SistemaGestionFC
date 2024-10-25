// Función para exportar la tabla de detalle medio de pago a un archivo Excel con estilos usando ExcelJS
document.getElementById('exportarExcelMedioPago').addEventListener('click', function () {
    var table = document.querySelector('table'); // Asegúrate de que esta tabla sea la correcta en detalle_medio_pago.html
    var rows = table.querySelectorAll('tbody tr');

    // Crear un nuevo libro de trabajo y hoja de trabajo
    var workbook = new ExcelJS.Workbook();
    var worksheet = workbook.addWorksheet('Detalle Medio de Pago');

    // Definir las columnas de la hoja de trabajo
    const columns = [
        { header: 'Fecha', key: 'fecha', width: 15 },
        { header: 'Tipo', key: 'tipo', width: 10 },
        { header: 'Categoría', key: 'categoria', width: 20 },
        { header: 'Monto', key: 'monto', width: 15 },
        { header: 'Moneda', key: 'moneda', width: 10 },
        { header: 'Patente', key: 'patente', width: 15 }
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
        a.download = 'detalle_medio_pago.xlsx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, { autohide: true, delay: 5000 });
    });
    toastList.forEach(toast => toast.show());
});
