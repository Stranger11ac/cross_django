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
