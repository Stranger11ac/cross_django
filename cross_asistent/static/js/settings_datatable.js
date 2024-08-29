let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5] },
        { orderable: false, targets: [3, 4, 5] },
        { searchable: false, targets: [0, 3, 4, 5] },
    ],
    pageLength: 20,
    destroy: true,
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listDatabase();
    dataTable = $("#datatable_database").DataTable(dataTableOptions);
    dataTableIsInitialized = true;
};

const listDatabase = async () => {
    try {
        const databaseList = $("#tbody_database").data("list-table");
        const url_dbUpdate = $("#tbody_database").data("url-dbupdate");
        const url_dbdelete = $("#tbody_database").data("url-dbdelete");
        const response = await fetch(databaseList);
        const data = await response.json();

        let content = ``;
        data.infodb.forEach((dato, index) => {
            let db_image = ``;
            if (dato.imagen) {
                db_image = `<img src="${dato.imagen}" alt="Imagen: ${dato.titulo}" class="img-rounded materialBoxed hover-shadow max_w150">`;
            }

            content += `
                <tr class="table_odd_items">
                    <td>${dato.id}</td>
                    <td>${dato.categoria}</td>
                    <td>${dato.titulo}</td>
                    <td>${db_image}</td>
                    <td>${dato.documento}</td>
                    <td>
                        <div class="d-flex flex-column align-items-center gap_10">
                            <button type="button" class="btn btn-floating btn-info" data-mdb-ripple-init data-mdb-modal-init
                                data-mdb-target="#editDBModal${dato.id}">
                                <i class="fa-solid fa-edit fs-12"></i>
                            </button>
                            <button type="button" class="btn btn-floating btn-danger" data-mdb-ripple-init data-mdb-modal-init
                                data-mdb-target="#eliminar_modal${dato.id}">
                                <i class="fa-regular fa-trash-can fs-12"></i>
                            </button>
                        </div>

                        <!-- Modal: Edit database -->
                        <div class="modal fade" id="editDBModal${dato.id}" tabindex="-1" aria-labelledby="editDBModalLabel${dato.id}"
                            aria-hidden="true" data-mdb-backdrop="static" data-mdb-keyboard="false">
                            <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="editDBModalLabel${dato.id}">Editar Informacion</h5>
                                        <button type="button" class="btn-close" data-mdb-ripple-init data-mdb-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body text-start">
                                        <form method="post" action="${url_dbUpdate}" data-submit-form id="dbUpdate" autocomplete="off">
                                            <input type="text" class="d-none" value="${dato.id}" name="id">
                                            <div class="row pt-2">
                                                <div class="col">
                                                    <div class="form-outline mb-4" data-mdb-input-init>
                                                        <i class="fa-solid fa-heading trailing"></i>
                                                        <input type="text" id="titulo${dato.id}" name="titulo"
                                                            class="form-control active form-icon-trailing" value="${dato.titulo}" required />
                                                        <label class="form-label" for="titulo${dato.id}">Título:</label>
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="form-outline mb-4" data-mdb-input-init>
                                                <i class="fa-solid fa-keyboard trailing"></i>
                                                <textarea class="form-control active form-icon-trailing" id="informacion${dato.id}"
                                                    name="informacion" rows="5" required>${dato.informacion}</textarea>
                                                <label for="informacion${dato.id}" class="form-label">Información:</label>
                                            </div>
                                            <div class="row">
                                                <div class="col-12">
                                                    <div class="form-outline mb-4" data-mdb-input-init>
                                                        <i class="fa-solid fa-link trailing"></i>
                                                        <input type="url" id="redirigir${dato.id}" name="redirigir"
                                                            class="form-control active form-icon-trailing" value="${dato.redirigir}" />
                                                        <label class="form-label" for="redirigir${dato.id}">Redirigir: (url / liga)</label>
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="mb-4">
                                                        <label for="documentos${dato.id}" class="form-label">Cambiar Documento: (PDF)</label>
                                                        <input type="file" class="form-control" id="documentos${dato.id}" name="documento"
                                                            accept="application/pdf">
                                                    </div>
                                                </div>
                                                <div class="col-md-6">
                                                    <div class="mb-4">
                                                        <label for="imagenes${dato.id}" class="form-label">Cambiar Imágen:</label>
                                                        <input type="file" class="form-control" id="imagenes${dato.id}" name="imagen"
                                                            accept="image/jpeg, image/png, image/webp*">
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="col">
                                                    <button type="submit" class="btn btn_detail btn-block">Guardar</button>
                                                </div>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Modal: Eliminar database -->
                        <div class="modal fade " id="eliminar_modal${dato.id}" tabindex="-1" aria-labelledby="labelModal${dato.id}"
                            aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="labelModal${dato.id}">
                                            Eliminar dato</h5>
                                        <button type="button" class="btn-close" data-mdb-ripple-init data-mdb-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <h3 class="text-center mb-2">¿Quieres eliminar el dato <u>${dato.titulo}</u>?
                                        </h3>
                                        <h6 class="text-center">"${dato.id} - ${dato.titulo}"</h6>
                                        <p class="text-center">Se eliminará toda la información relacionada <br> Esta acción es permanente</p>
                                    </div>
                                    <div class="modal-footer justify-content-between">
                                        <button type="button" class="btn btn_detail" data-mdb-ripple-init data-mdb-dismiss="modal">Cancelar</button>
                                        <form method="post" action="${url_dbdelete}" data-submit-form>
                                            <input type="text" value="${dato.id}" name="id" class="d-none">
                                            <button type="submit" class="btn btn-danger">Eliminar <i class="fa-regular fa-trash-can ms-1"></i></button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>`;
        });
        tbody_database.innerHTML = content;
    } catch (ex) {
        alert(ex);
        console.error(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});
