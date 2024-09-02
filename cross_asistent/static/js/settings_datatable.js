let tableDatabase;
let dataTableIsInitialized = false;

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        tableDatabase.destroy();
    }

    await listDatabase();
    tableDatabase = $("#datatable_database").DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/2.1.5/i18n/es-MX.json",
        },
        columnDefs: [
            { className: "text-center", targets: [0, 1, 2, 3, 4, 5] },
            { orderable: false, targets: [3, 4, 5] },
            { searchable: false, targets: [0, 3, 4, 5] },
        ],
        pageLength: 20,
        destroy: true,
    });
    dataTableIsInitialized = true;

    
    // <label for="filterCategory">Filtrar por Categoría:</label>
    // <select id="filterCategory">
    //     <option value="">Todas</option>
    //     <option value="Preguntas">Preguntas</option>
    //     <option value="OtraCategoria">Otra Categoría</option>
    //     <!-- Agrega más opciones según tus categorías -->
    // </select>
    // Filtro de categoría
    // $("#filterCategory").on("change", function() {
    //     const selectedCategory = $(this).val();
    //     dataTable.column(1).search(selectedCategory).draw();  // Filtrar la columna de categoría (índice 1)
    // });
};

const listDatabase = async () => {
    try {
        const tableId = "tbody_database";
        const databaseList = $(`#${tableId}`).data("list-table");
        await fetch(databaseList)
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((data) => {
                        throw new Error(data.message || "Error desconocido");
                    });
                }
                return response.json();
            })
            .then((data) => {
                $(`[data-table-load='${tableId}']`).addClass("d-none");
                $(`[data-table-container='${tableId}']`).removeClass("d-none");

                let content = ``;
                data.infodb.map((dato) => {
                    let db_image = ``;
                    if (dato.imagen) {
                        db_image = `<img src="${dato.imagen}" loading="lazy" alt="Imagen: ${dato.titulo}" class="img-rounded max_w150">`;
                    }
                    content += `<tr class="table_odd_items">
                                    <td>${dato.id}</td>
                                    <td>${dato.categoria}</td>
                                    <td>${dato.titulo}</td>
                                    <td>${db_image}</td>
                                    <td>${dato.documento}</td>
                                    <td>
                                        <div class="d-flex flex-column align-items-center gap_10">
                                            <button type="button" class="btn btn-floating btn-info" onclick="openModal('#editDBModal',${dato.id})">
                                                <i class="fa-solid fa-edit fs-12"></i>
                                            </button>
                                            <button type="button" class="btn btn-floating btn-danger" onclick="openModal('#deleteDBmodal',${dato.id})">
                                                <i class="fa-regular fa-trash-can fs-12">
                                                </i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>`;
                });
                tbody_database.innerHTML = content;
            })
            .catch((error) => {
                console.error("😥 Error:", error);
                alertSToast("top", 8000, "warning", "Ocurrió un error. Intente nuevamente. 😥");
            });
    } catch (ex) {
        alert(ex);
        console.error(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});

function openModal(idMdbModal, dataid) {
    $(idMdbModal).data("get-info", dataid);
    $(idMdbModal).modal("show");
}

// Para el modal de edición
$("#editDBModal").on("show.bs.modal", function () {
    const thisdataid = $(this).data("get-info");
    const postUrl = $("#tbody_database").data("url-info");
    $.ajax({
        url: postUrl,
        method: "POST",
        data: JSON.stringify({ id: thisdataid }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": formToken,
        },
        success: function (data) {
            const thisModal = $("#editDBModal");
            thisModal.find("#editid").val(thisdataid);
            thisModal.find("#editcateg").val(data.categoria);
            thisModal.find("#editcateg").text(data.categoria);
            thisModal.find("#edittitulo").val(data.titulo);
            thisModal.find("#editinfo").val(data.informacion);

            if (data.redirigir != null || data.redirigir != "") {
                thisModal.find("#editredirigir").val(data.redirigir);
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
            alertSToast("center", 9000, "error", "Ocurrio un error al obtener los datos. intente de nuevo mas tarde.");
        },
    });
});

// // Para el modal de eliminación
$("#deleteDBmodal").on("show.bs.modal", function () {
    const thisdataid = $(this).data("get-info");
    const postUrl = $("#tbody_database").data("url-info");
    $.ajax({
        url: postUrl,
        method: "POST",
        data: JSON.stringify({ id: thisdataid }),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": formToken,
        },
        success: function (data) {
            const thisModal = $("#deleteDBmodal");
            thisModal.find("#deltitulo").text(data.titulo);
            thisModal.find("#delid").val(thisdataid);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.error("Error:", textStatus, errorThrown);
            alertSToast("center", 9000, "error", "Ocurrio un error al obtener los datos. intente de nuevo mas tarde.");
        },
    });
});

$("#editDBModal").on("hidden.bs.modal", function () {
    const thisModal = $(this);
    thisModal.find("#editid").val('');
    thisModal.find("#editcateg").val('');
    thisModal.find("#editcateg").text('');
    thisModal.find("#edittitulo").val('');
    thisModal.find("#editinfo").val('');
    thisModal.find("#editredirigir").val('');
});

$("#deleteDBmodal").on("hidden.bs.modal", function () {
    const thisModal = $(this);
    thisModal.find("#deltitulo").text('');
    thisModal.find("#delid").val('');
});
