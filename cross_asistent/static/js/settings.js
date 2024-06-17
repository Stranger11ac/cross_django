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
        $("#question").keydown(chatSubmit);

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
        $("#singinForm").submit(singInUp);
        $("#signupForm").submit(singInUp);

        // generate password random
        // console.log($('[data-input_pass^="generatePass"]'));

        // generar contraseña para usuarios nuevos
        var pass_random = generarPassAleatoria(8);
        $("#pass_newuser").val(pass_random);

        // Editar usuario
        // generar nueva contraseña aleatoria ##################################
        $('button[data-editpass="edit_newpass"]').on("click", function () {
            $(this).addClass("active");
            var newRandomPass = generarPassAleatoria(8);
            var editInputId = $(this).data("editinput");
            setTimeout(() => {
                $(this).removeClass("active");
            }, 1000);
            $("#" + editInputId)
                .val(newRandomPass)
                .focus();
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
    } catch (error) {
        console.log("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ah ocurrido un error JQ. ${error}`);
    }
});

// Funciones JAVASCRIPT ###########################
// Cerrar la sesion ##########################################################
if (document.querySelector("main").classList.contains("main_container")) {
    window.location.href = "/logout";
}

// Crear una cadena aleatoria de la longitud que se dese ###########################
function generarCadenaAleatoria(longitud) {
    var caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
}

function generarPassAleatoria(longitud) {
    var caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-%$#@!*&^.";
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
}

function chatSubmit(e) {
    e.preventDefault();
    if (e.key === "Enter") {
        if (e.shiftKey) {
            const cursorPos = this.selectionStart;
            const textBefore = this.value.substring(0, cursorPos);
            const textAfter = this.value.substring(cursorPos);
            this.value = textBefore + "\n" + textAfter;
            this.selectionStart = cursorPos + 1;
            this.selectionEnd = cursorPos + 1;
        } else {
            document.getElementById("chatForm_submit").click();
        }
    }
}
// Funcion de iniciar secion y Registrar nuevo Usuario ######################################################################
function singInUp(e) {
    e.preventDefault();
    const thisForm = e.target;
    const formData = new FormData(thisForm);
    const timerOut = 8000;

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
                if (data.functionForm == "singin") {
                    window.location.href = data.redirect_url;
                } else {
                    thisForm.reset();
                    alertSToast("center", timerOut + 4000, "success", dataMessage, function () {
                        location.reload();
                    });
                }
            } else {
                alertSToast("top", timerOut + 2000, "warning", dataMessage);
            }
        })
        .catch((error) => {
            console.error("😥 Error:", error);
            errorMessage = error.message || "Ocurrió un error. Intente nuevamente. 😥";
            alertSToast("center", timerOut + 3000, "error", errorMessage);
        });
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
