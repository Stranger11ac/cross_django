const dtLenguage = { url: "https://cdn.datatables.net/plug-ins/2.1.5/i18n/es-MX.json" };
const tableDatabaseObj = document.getElementById("datatable_database");
const tableBannersObj = document.getElementById("datatableBanners");
let dataTableIsInitialized = false;
let tableDatabase;
let tableBanners;

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        tableDatabase.destroy();
        tableBanners.destroy();
    }

    if (tableDatabaseObj) {
        await listDatabase();
        tableDatabase = $("#datatable_database").DataTable({
            columnDefs: [
                { className: "text-center", targets: [0, 1, 2, 3, 4, 5] },
                { orderable: false, targets: [3, 4, 5] },
                { searchable: false, targets: [0, 3, 4, 5] },
            ],
            language: dtLenguage,
            pageLength: 20,
            destroy: true,
        });
    }

    if (tableBannersObj) {
        await listBanners();
        tableBanners = $("#datatableBanners").DataTable({
            columnDefs: [
                { className: "text-center", targets: [0, 1, 2, 3] },
                { orderable: false, targets: [2, 3] },
                { searchable: false, targets: [2, 3] },
            ],
            language: dtLenguage,
            lengthChange: false,
            paging: false,
            info: false,
            destroy: true,
        });

        const dataLength = tableBanners.rows().count();
        if (dataLength > 10) {
            tableBanners.page.len(10).draw();
            tableBanners.settings()[0].oFeatures.bPaginate = true;
            tableBanners.settings()[0].oFeatures.bInfo = true;
            tableBanners.settings()[0].oFeatures.bLengthChange = true;
        }
    }

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

// Tabla de Dase de Datos (models.Database)
const listDatabase = async () => {
    try {
        const tableId = "tbodyDatabase";
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
                    content += `<tr class="table_odd_items"><td>${dato.id}</td><td>${dato.categoria}</td><td>${dato.titulo}</td><td>${db_image}</td><td>${dato.documento}</td><td><div class="d-flex flex-column align-items-center gap_10"><button type="button" class="btn btn-floating btn-info" onclick="openModal('#editDBModal',${dato.id})"><i class="fa-solid fa-edit fs-12"></i></button><button type="button" class="btn btn-floating btn-danger" onclick="openModal('#deleteDBmodal',${dato.id})"><i class="fa-regular fa-trash-can fs-12"></i></button></div></td></tr>`;
                });
                tbodyDatabase.innerHTML = content;
            })
            .catch((error) => {
                console.error("😥 Error:", error);
                alertSToast("top", 8000, "warning", "Ocurrió un error al obtener los datos. 😥");
            });
    } catch (ex) {
        alert(ex);
        console.error(ex);
    }
};

// Tabla de Banners (models.Banners)
const listBanners = async () => {
    try {
        const tableId = "tbodyBanners";
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
                data.infobanners.map((dato) => {
                    let bannertitulo = "";
                    let cellSpan = "";
                    let titleSpan = "";
                    let bannerDesc = "";
                    let bannervisible = "";
                    if (dato.solo_imagen == false) {
                        bannertitulo = dato.titulo;
                        bannerDesc = dato.descripcion;
                    } else {
                        if (dato.visible == false) {
                            bannervisible = '<small class="bg-danger rounded-pill p-1 mt-3">Banner Invisible</small>';
                        }
                        bannertitulo = `${dato.titulo} <small class="bg-success rounded-pill p-1 mt-3">Solo Imagen y boton</small> ${bannervisible}`;
                        cellSpan = 'colspan="2"';
                        titleSpan = 'class="d-none"';
                    }

                    let bannerImage = "";
                    if (dato.imagen) {
                        bannerImage = `<img src="${dato.imagen}" loading="lazy" class="img-rounded max_w150">`;
                    }
                    content += `<tr class="table_odd_items">
                                    <td ${cellSpan}>${bannertitulo}</td>
                                    <td ${titleSpan}>${bannerDesc}</td>
                                    <td>${bannerImage}</td>
                                    <td>
                                        <div class="d-flex flex-column align-items-center gap_10">
                                            <button type="button" class="btn btn-floating btn-info">
                                                <i class="fa-solid fa-edit fs-12"></i>
                                            </button>
                                            <button type="button" class="btn btn-floating btn-danger">
                                                <i class="fa-regular fa-trash-can fs-12">
                                                </i>
                                            </button>
                                        </div>
                                    </td>
                                </tr>`;
                });
                tbodyBanners.innerHTML = content;
            })
            .catch((error) => {
                console.error("😥 Error:", error);
                alertSToast("top", 8000, "warning", "Ocurrió un error al obtener los Banners. 😥");
            });
    } catch (ex) {
        alert(ex);
        console.error(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();

    setTimeout(() => {
        $("[data-table-container] .row.dt-row ").addClass("table-responsive m-0 my-3");
        $("[data-table-container] .row.dt-row .col-sm-12").addClass("p-0");
    }, 500);
});

// Abrir modal segun su data
function openModal(idMdbModal, dataid) {
    $(idMdbModal).data("get-info", dataid);
    $(idMdbModal).modal("show");
}

if (tableBannersObj) {
    // Para el modal de edición
    $("#editDBModal").on("show.bs.modal", function () {
        const thisdataid = $(this).data("get-info");
        const postUrl = $("#tbodyDatabase").data("url-info");
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
                alertSToast(
                    "center",
                    9000,
                    "error",
                    "Ocurrio un error al obtener los datos. intente de nuevo mas tarde."
                );
            },
        });
    });

    $("#editDBModal").on("hidden.bs.modal", function () {
        const thisModal = $(this);
        thisModal.find("#editid").val("");
        thisModal.find("#editcateg").val("");
        thisModal.find("#editcateg").text("");
        thisModal.find("#edittitulo").val("");
        thisModal.find("#editinfo").val("");
        thisModal.find("#editredirigir").val("");
    });

    // Para el modal de eliminación
    $("#deleteDBmodal").on("show.bs.modal", function () {
        const thisdataid = $(this).data("get-info");
        const postUrl = $("#tbodyDatabase").data("url-info");
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
                alertSToast(
                    "center",
                    9000,
                    "error",
                    "Ocurrio un error al obtener los datos. intente de nuevo mas tarde."
                );
            },
        });
    });

    $("#deleteDBmodal").on("hidden.bs.modal", function () {
        const thisModal = $(this);
        thisModal.find("#deltitulo").text("");
        thisModal.find("#delid").val("");
    });
}
