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

        // Vista de Programador
        // Agrega la clase active al banner con la id mas baja #######################################
        var elements = $('[id^="bannerid_"]');
        var minIdNumber = Infinity;
        let minIdElement = null;

        $('[id^="bannerid_"]').each(function () {
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

        // Enviar chat con enter chatGPT ######################################
        $("#txtQuestion").keydown((evento) => {
            if (evento.keyCode === 13 && !evento.shiftKey) {
                evento.preventDefault();
                $("#chatForm_submit").click();
            }
        });

        // ChatGPT Submit ####################################################
        $("#chatForm").submit(chatSubmit);

        // iniciar sesion ####################################################
        // Crea usuario nuevo desde programador ##############################
        // Registrar un nuevo articulo con TinyMCE ###########################
        $("[data-submit-form]").submit(jsonSubmit);

        // Editar/Crear usuario
        // generar nueva contraseña aleatoria #################################
        $("button[data-editpass]").click(function () {
            $(this).addClass("active");
            var newRandomPass = cadenaRandom(8, caracteres);
            var editInputId = $(this).data("editinput");
            setTimeout(() => {
                $(this).removeClass("active");
            }, 1000);
            $("#" + editInputId)
                .addClass("focus")
                .val(newRandomPass)
                .focus();
        });

        //
        //
    } catch (error) {
        console.error("Error Inesperado: ", error);
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
var texto3 = /[a-zA-Z0-9]{3}/;

function cadenaRandom(longitud, caracteres) {
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
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

// Funcion de preguntar a chatGPT ################################################################
var contOutput = document.querySelector("#output");
function chatSubmit(e) {
    e.preventDefault();
    const pregunta = txtQuestion.value;
    const chatForm = e.target;
    this.reset();

    if (!texto3.test(pregunta)) {
        return alertSToast("center", 6000, "warning", 'Por favor, escribe una pregunta 🧐😬');
    }

    var tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const htmlBlock = `
        <div class="output_block">
            <div class="btn_secondary chat_msg user_submit" data-tokeid="${valID}">
                ${pregunta}
            </div>
        </div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const user_submit = document.querySelector(`.user_submit[data-tokeid="${valID}"]`);
    setTimeout(function () {
        user_submit.classList.add("visible");
        setTimeout(scrollToBottom, 500);
    }, 20);

    fetch(chatForm.action, {
        method: "POST",
        body: JSON.stringify({ question: pregunta }),
        headers: {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": chatForm.querySelector("[name=csrfmiddlewaretoken]").value,
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
            if (data.success) {
                console.table(data.answer);
                const htmlBlock = `
                <div class="btn_detail chat_msg asistent_response" data-tokeid="${valID}">
                    <span>${data.answer.informacion}</span>
                </div>
            `;

                contOutput.insertAdjacentHTML("beforeend", htmlBlock);
                const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);

                setTimeout(function () {
                    setTimeout(function () {
                        asistent_response.classList.add("visible");
                        setTimeout(scrollToBottom, 350);
                    }, 970);
                }, 20);
            } else {
                alertSToast("top", 8000, "error", `Error: ${data.message}`);
            }
        })
        .catch((error) => {
            console.error("😥 Error:", error);
            alertSToast("top", 8000, "warning", "Ocurrió un error. Intente nuevamente. 😥");
        });
}

// Hacer scroll con un nuevo mensaje en el chat ###############################################
if (contOutput) {
    function scrollToBottom() {
        contOutput.scrollTop = contOutput.scrollHeight;
    }
    var observer = new MutationObserver(() => {
        scrollToBottom();
    });
    scrollToBottom();
    observer.observe(contOutput, { childList: true, subtree: true });
}

// Copiar al portapapeles #########################################################
() => {
    const inputs = document.querySelectorAll("input[data-copy]");
    inputs.forEach((input) => {
        input.addEventListener("click", () => {
            if (!navigator.clipboard) {
                alertSToast("center", 8000, "info", "Tu navegador no admite copiar al portapapeles 😯😥🤔");
                return;
            }
            const textCopy = input.value;
            if (textCopy != "") {
                navigator.clipboard
                    .writeText(textCopy)
                    .then(() => {
                        console.log("Texto copiado al portapapeles:", textCopy);
                        alertSToast("top", 5000, "success", "Texto Copiado! 🥳");
                    })
                    .catch((error) => {
                        message = "Error al copiar al portapapeles";
                        console.error(message, ":", error);
                        alertSToast("top", 8000, "error", `${message} 🤔😥`);
                    });
            }
        });
    });
};

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

function obtenerDatosEdificio(articuloId, urlConsulta) {
    console.log(`AJAX: ${urlConsulta}`);
    if (articuloId) {
        $.ajax({
            url: urlConsulta,
            type: "GET",
            data: { id: articuloId },
            success: function (data) {
                $("#edificio_id").val(data.id);
                $("#titulo").val(data.titulo);
                $("#informacion").val(data.informacion);
                $("#color").val(data.color);
                $("#color_picker").val(data.color);
                $("#p1_polygons").val(data.p1_polygons);
                $("#p2_polygons").val(data.p2_polygons);
                $("#p3_polygons").val(data.p3_polygons);
                $("#p4_polygons").val(data.p4_polygons);
                if (data.imagen_url) {
                    const oldImgUrl = data.imagen_url;
                    const newImgUrl = oldImgUrl.replace("/cross_asistent", "");
                    $("#imagen_actual").attr("src", newImgUrl).show();
                } else {
                    $("#imagen_actual").hide();
                }
            },
        });
    } else {
        $("#edificio_id").val("");
        $("#titulo").val("");
        $("#informacion").val("");
        $("#color").val("");
        $("#color_picker").val("#000000");
        $("#p1_polygons").val("");
        $("#p2_polygons").val("");
        $("#p3_polygons").val("");
        $("#p4_polygons").val("");
        $("#imagen_actual").hide();
    }
}

$("#selectArticulo").change(function () {
    var articuloId = $(this).val();
    const urlConsulta = $(this).data("second-action");
    obtenerDatosEdificio(articuloId, urlConsulta);
});


$("#color_picker").on("input", function () {
    var color = $(this).val();
    $("#color").val(color);
});


$("#edificioForm").submit(function (event) {
    event.preventDefault();
    var formData = new FormData(this);

    $.ajax({
        url: $(this).attr("action"),
        type: $(this).attr("method"),
        data: formData,
        contentType: false,
        processData: false,
    });
});
