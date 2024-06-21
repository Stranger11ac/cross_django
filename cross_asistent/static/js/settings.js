$(document).ready(function () {
    try {
        // Filtro de busqueda ###################################################################
        var input = $("#searchInput");
        function filtertable() {
            var value = input.val().toLowerCase();
            $("#searchInput").text(value);
            var result = $(".results_item").filter(function () {
                $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
                return $(this).is(":visible");
            }).length;
        }

        input.on("input", filtertable);

        // abrir menu del asistente ##############################################################
        $(".controls_btn_microphone").click(() => {
            $(".asistent_group").addClass("open open_controls bg-body-tertiary");
            $(".btn_controls").addClass("btn_detail").removeClass("btn_secondary");
            $("#btn_controls_icon").removeClass("fa-comment").addClass("fa-microphone");
        });

        $(".toggle_controls").click(() => {
            $(".asistent_group.open").toggleClass("close_controls open_keyboard open_controls");
            // Detectar si es un dispositivo móvil
            const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
            // Solo ejecutar el setTimeout si no es un dispositivo móvil
            if (!isMobile) {
                setTimeout(function () {
                    $(".controls_input #question").focus();
                }, 1000);
            }
        });

        $(".controls_btn_close").click(() => {
            $(".asistent_group").removeClass("open open_controls close_controls open_keyboard bg-body-tertiary");
            $(".btn_controls").removeClass("btn_detail").addClass("btn_secondary");
            $("#btn_controls_icon").addClass("fa-comment").removeClass("fa-microphone");
        });

        // Envia el formulario al chat con un enter ###############################
        $("#question").keydown(submitChat);

        // Vista de Programador
        // Agrega la clase active al banner con la id mas baja #######################################
        var elements = $('[id^="bannerid_"]');
        var minIdNumber = Infinity;
        let minIdElement = null;

        elements.each(function () {
            var id = $(this).attr("id");
            var number = parseInt(id.split("_")[1]);
            if (number < minIdNumber) {
                minIdNumber = number;
                minIdElement = $(this);
            }
        });

        if (minIdElement !== null) {
            minIdElement.addClass("active");
        }

        // iniciar sesion ####################################################
        $("#singinForm").submit(jsonSubmit);
        $("#signupForm").submit(jsonSubmit);
        // Crea usuario nuevo desde programador ####################################
        $("#createuserprog").submit(jsonSubmit);
        // Registrar un nuevo articulo con TinyMCE ##################################
        $("#formularioArticulo").submit(jsonSubmit);

        // Editar/Crear usuario
        // generar nueva contraseña aleatoria ##################################
        $('button[data-editpass="edit_newpass"]').on("click", function () {
            $(this).addClass("active");
            var newRandomPass = cadenaRandom(8, caracteres);
            var editInputId = $(this).data("editinput");
            setTimeout(() => {
                $(this).removeClass("active");
            }, 1000);
            $("#" + editInputId)
                .val(newRandomPass)
                .focus();
        });

<<<<<<< HEAD
        // Registrar un nuevo articulo con TinyMCE ##################################
        $("#formularioArticulo").submit(articleForm);

        //  ##################################
        function obtenerDatosEdificio(articuloId) {
            if (articuloId) {
                $.ajax({
                    url: "/obtenerEdificio/",
                    type: 'GET',
                    data: { 'id': articuloId },
                    success: function(data) {
                        $("#edificio_id").val(data.id);
                        $("#titulo").val(data.titulo);
                        $("#informacion").val(data.informacion);
                        if (data.imagen_url) {
                            $("#imagen_actual").attr("src", data.imagen_url).show();
                        } else {
                            $("#imagen_actual").hide();
                        }
                    }
                });
            } else {
                $("#edificio_id").val('');
                $("#titulo").val('');
                $("#informacion").val('');
                $("#imagen_actual").hide();
            }
        }
    
        $("#selectArticulo").change(function() {
            var articuloId = $(this).val();
            sessionStorage.setItem('ultimoArticuloId', articuloId);
            obtenerDatosEdificio(articuloId);
        });
    
        var ultimoArticuloId = sessionStorage.getItem('ultimoArticuloId');
        if (ultimoArticuloId) {
            $("#selectArticulo").val(ultimoArticuloId);
            obtenerDatosEdificio(ultimoArticuloId);
        }
    
        $("#edificioForm").on('submit', function(event) {
            event.preventDefault();
    
            $.ajax({
                url: $(this).attr('action'),
                type: $(this).attr('method'),
                data: new FormData(this),
                processData: false,
                contentType: false,
                success: function(response) {
                    $("#successMessage").show().delay(3000).fadeOut();
                }
            });
        });

        // Convertir scroll vertical en horizontal ############################
        var $tableContainer = $("#table-container");
        if (!$tableContainer.length) {
            return;
        }
        function isOverflowing($element) {
            var element = $element[0];
            return element.scrollWidth > element.clientWidth;
        }
        function handleWheelEvent(e) {
            if (e.originalEvent.deltaY > 0) {
                this.scrollLeft += 300;
            } else {
                this.scrollLeft -= 300;
            }
            e.preventDefault();
        }
        function toggleWheelEvent() {
            if (isOverflowing($tableContainer)) {
                $tableContainer.on("wheel", handleWheelEvent);
            } else {
                $tableContainer.off("wheel", handleWheelEvent);
            }
        }
        toggleWheelEvent();
        $(window).on("resize", function () {
            toggleWheelEvent();
        });
=======
        // $("#edificio").change(function() {
        //     $("#filtroEdificio").submit();
        // });
>>>>>>> 3f89d094b41d807cad7ec02bc0e574c22bbd6451
    } catch (error) {
        console.log("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ah ocurrido un error JQ.`);
    }
});

// ############################################################################
// ########################### Funciones JAVASCRIPT ###########################
// ############################################################################

// Cerrar la sesion ##########################################################
if (document.querySelector("main").classList.contains("main_container")) {
    window.location.href = "/logout";
}

// Crear una cadena aleatoria de la longitud que se dese ###########################
var alfabetico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
var alfanumerico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
var caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-%$#@!*&^.";

function cadenaRandom(longitud, caracteres) {
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
}

function submitChat(event) {
    event.preventDefault();
    if (event.key === "Enter") {
        if (event.shiftKey) {
            const cursorPos = this.selectionStart;
            const textBefore = this.value.substring(0, cursorPos);
            const textAfter = this.value.substring(cursorPos);
            this.value = textBefore + "\n" + textAfter;
            this.selectionStart = cursorPos + 1;
            this.selectionEnd = cursorPos + 1;
        } else {
            chatForm_submit.click();
        }
    }
}

// Funcion de iniciar secion y Registrar nuevo Usuario ######################################################################
function jsonSubmit(e) {
    e.preventDefault();
    const timerOut = 6000;
    const thisForm = e.target;
    const formData = new FormData(thisForm);

    if (formData.has("contenidoWord")) {
        const contenidoTiny = tinymce.activeEditor.getContent();
        formData.set("contenidoWord", contenidoTiny);
    }

    fetch(thisForm.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": thisForm.querySelector("[name=csrfmiddlewaretoken]").value,
        },
    })
        .then((response) => {
            if (!response.ok) {
                return response.json().then((data) => {
                    throw new Error(data.message || "Error desconocido");
                });
            }
            return response.json();
        })
        .then((data) => {
            dataMessage = data.message;
            if (data.success) {
                thisForm.reset();
                if (data.functionForm == "singin") {
                    window.location.href = data.redirect_url;
                } else {
                    alertSToast("center", timerOut + 4000, "success", dataMessage, function () {
                        location.reload();
                    });
                }
            } else {
                console.error(dataMessage);
                alertSToast("top", timerOut + 2000, "warning", dataMessage);
            }
        })
        .catch((error) => {
            console.error("😥 Error:", error);
            errorMessage = error.message || "Ocurrió un error. Intente nuevamente. 😥";
            alertSToast("center", timerOut + 3000, "error", errorMessage);
        });
}

// Función para obtener el token CSRF de manera segura #############################################
function getCSRFToken() {
    const csrfCookie = document.querySelector("[name=csrfmiddlewaretoken]").value;
    return csrfCookie;
    // const csrfCookie = document.cookie.split(";").find((cookie) => cookie.trim().startsWith("csrftoken="));
    // if (csrfCookie) {
    //     return csrfCookie.split("=")[1];
    // } else {
    //     console.error("CSRF token not found in cookies.");
    //     return "";
    // }
}

// context menu disabled ####################################
document.oncontextmenu = function () {
    return false;
};

// Template Alertas switalert ################################
function alertSToast(posittionS, timerS, iconS, titleS, didDestroyS) {
    const Toast = Swal.mixin({
        toast: true,
        position: posittionS,
        showConfirmButton: false,
        showCloseButton: true,
        timer: timerS,
        timerProgressBar: true,
        customClass: {
            icon: "icon_alert",
            title: "title_alert",
            timerProgressBar: "progressbar_alert",
            closeButton: "close_button_alert",
        },
        didOpen: (toast) => {
            toast.addEventListener("mouseenter", Swal.stopTimer);
            toast.addEventListener("mouseleave", Swal.resumeTimer);
        },
        didDestroy: didDestroyS,
    });
    Toast.fire({
        icon: iconS,
        title: titleS,
    });
}

// alertSToast('top', 8000, 'success', '<br>lo normal');
