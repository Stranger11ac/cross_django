$(document).ready(function () {
    try {
        var input = $("#searchInput");

        function filtertable() {
            var value = input.val().toLowerCase();
            $("#searchInput").text(value);

            var result = $(".accordion-item").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                return $(this).is(":visible");
            }).length;
        }

        input.on("input", filtertable);

        function generarCadenaAleatoria(longitud) {
            var caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
            var cadenaAleatoria = '';
            for (var i = 0; i < longitud; i++) {
                var indice = Math.floor(Math.random() * caracteres.length);
                cadenaAleatoria += caracteres.charAt(indice);
            }
            return cadenaAleatoria;
        }

        var tokid = generarCadenaAleatoria(5);

    } catch (error) {
        console.log("Error Inesperado: ", error);
        alertSToast('top', 8000, 'error', '😥 Ah ocurrido un error en el filtro de busqueda. Code:#CC320');
    }
});
