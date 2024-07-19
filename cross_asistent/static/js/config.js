// Notificaciones ######################################
// Cargar las IDs desde localStorage
var storedIds = JSON.parse(localStorage.getItem("notificationIds")) || [];
storedIds.forEach(function (id) {
    $("#" + id).removeClass(
        "list-group-item-warning list-group-item-info list-group-item-success list-group-item-danger list-group-item-primary"
    );
    $("#" + id).addClass("list-group-item-secondary");
});

// Colores de la Interfaz #################################
const colorPrefer = localStorage.getItem("data-color_prefer");
if (colorPrefer) {
    $(`[data-change-color="${colorPrefer}"]`).addClass("active");
    $("body").attr("data-color_prefer", colorPrefer);
} else {
    $('[data-change-color="blue"]').addClass("active");
    $("body").attr("data-color_prefer", "blue");
}

// Color de tema #################################
const colorTheme = localStorage.getItem("data-mdb-theme");
if (colorTheme) {
    if (colorTheme == "light") {
        $("#switchText").text("Claro");
        $("#switchTheme").prop("checked", true);
        $("html").attr("data-mdb-theme", "light");
    } else {
        $("#switchText").text("Oscuro");
        $("#switchTheme").prop("checked", false);
        $("html").attr("data-mdb-theme", "dark");
    }
}
