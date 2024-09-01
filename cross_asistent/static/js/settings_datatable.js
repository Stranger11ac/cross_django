let dataTable;
let dataTableIsInitialized = false;

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listDatabase();
    dataTable = $("#datatable_database").DataTable({
        language: {
            url: "https://cdn.datatables.net/plug-ins/2.1.5/i18n/es-MX.json",
        },
        columnDefs: [
            { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
            { orderable: false, targets: [3, 4, 5] },
            { searchable: false, targets: [0, 3, 4, 5] },
        ],
        pageLength: 20,
        destroy: true,
    });
    dataTableIsInitialized = true;
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
                    content += `<tr class="table_odd_items"><td>${dato.id}</td><td>${dato.categoria}</td><td>${dato.titulo}</td><td>${db_image}</td><td>${dato.documento}</td><td><div class="d-flex flex-column align-items-center gap_10"><button type="button" class="btn btn-floating btn-info" data-mdb-ripple-init data-mdb-toggle="modal" data-mdb-target="#editDBModal" onclick="alertasweet('#editDBModal')"><i class="fa-solid fa-edit fs-12"></i></button><button type="button" class="btn btn-floating btn-danger" data-mdb-ripple-init data-mdb-toggle="modal" data-mdb-target="#deleteDBmodal"><i class="fa-regular fa-trash-can fs-12"></i></button></div></td></tr>`;
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

function alertasweet(idMdbModal) {
    console.log(idMdbModal);
    alertSToast("top", 6000, "info", "click: " + idMdbModal);
    $(idMdbModal).modal("show");
}

// // Manejador de clic para mostrar el modal
// $("[data-mdb-toggle='modal']").on("click", function () {
//     const mdbModal = $(this).data("mdb-target");
//     alertSToast("top", 6000, "info", "click: " + mdbModal);
//     $(mdbModal).modal("show");
// });

// // Para el modal de edición
// $("#editDBModal").on("show.bs.modal", function (event) {
//     const button = $(event.relatedTarget);
//     alertSToast("top", 8000, "info", "Edit modal button clicked");
// });

// // Para el modal de eliminación
// $("#deleteDBmodal").on("show.bs.modal", function (event) {
//     const button = $(event.relatedTarget);
//     alertSToast("top", 8000, "info", "Delete modal button clicked");
// });

// $("[data-mdb-modal]").on("click", () => {
//     alertSToast("top", 6000, "info", "click");
//     // $(mdbModal).modal("show");
// });

// $(document).ready(function () {
//     // $("#deleteDBmodal").modal("show");
// });

// // Para el modal de edición
// // $("#editDBModal").on("show.bs.modal", function (event) {
// //     const button = $(event.relatedTarget);
// //     alertSToast("top", 8000, "info", button);
// // });

// // Para el modal de eliminación
// // $("#deleteDBmodal").on("show.bs.modal", function (event) {
// //     const button = $(event.relatedTarget);
// //     alertSToast("top", 8000, "info", button);
// // });
