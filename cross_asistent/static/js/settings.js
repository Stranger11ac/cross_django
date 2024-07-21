var alfabetico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
var alfanumerico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
var caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-%$#@!*&^.";
var texto3 = /[a-zA-Z0-9]{3}/;
var formToken = getCSRFToken();
var timerOut = 4000;

function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, 10) == "csrftoken" + "=") {
            return decodeURIComponent(cookie.substring(10));
        }
    }
    const csrfCookie = $("[name=csrfmiddlewaretoken]").val();
    return csrfCookie;
}

$(document).ready(function () {
    try {
        // Detectar cuando se abre cualquier modal
        $(".modal").on("shown.bs.modal", function (e) {
            $("body").addClass("body_minus");
        });

        // Opcional: Detectar cuando se cierra cualquier modal y remover la clase
        $(".modal").on("hidden.bs.modal", function (e) {
            $("body").removeClass("body_minus");
        });

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
            $("#btn_controls_icon").removeClass("fa-comment text_detail").addClass("fa-microphone");
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
            $("#btn_controls_icon").addClass("fa-comment text_detail").removeClass("fa-microphone");
        });

        // Vista de Programador
        // Agrega la clase active al banner con la id mas baja #######################################
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
        $("button[data-editinput]").click(genpass);

        function genpass() {
            $(this).addClass("active");
            var newRandomPass = cadenaRandom(8, caracteres);
            var editInputId = $(this).data("editinput");
            setTimeout(() => {
                $(this).removeClass("active");
            }, 1000);
            $("#" + editInputId)
                .val(newRandomPass)
                .focus();
        }

        // Quitar clase show #####################################
        $("[data-btn_closed]").on("click", function () {
            var targetId = $(this).attr("data-btn_closed");
            $("#" + targetId).toggleClass("show");
        });

        // Resetear formulario / vaciar todo el formulario
        $("[data-reset_form]").on("click", function () {
            var formId = $(this).attr("data-reset_form");
            var formElement = $("#" + formId)[0];

            if (formElement) {
                formElement.reset();
            }
        });

        // Estilo Texto Google #####################
        function colorizeGoogle() {
            const colors = ["#4285F4", "#EA4335", "#FBBC05", "#4285F4", "#34A853", "#EA4335"];
            const googleSpan = $(".style_google");
            const text = googleSpan.text();

            googleSpan.empty();
            for (let i = 0; i < text.length; i++) {
                googleSpan.append(`<span style="color:${colors[i]}">${text[i]}</span>`);
            }
        }
        colorizeGoogle();

        // Cerrar alertas ####################################################
        $(document).on("keydown", function (event) {
            if (event.key === "Escape" || event.keyCode === 27) {
                Swal.close();
            }
        });

        $("#cancelNewEdif").on("click", function () {
            $("#groupTitleMap").slideToggle("fast");
            $("#cancelNewEdif").slideToggle("fast");
            $(".img_form_map").slideToggle();
            $("#isNewEdif").prop("checked", true);

            $("#mapTitle").text("");
            $("#formTitle").val("");
            $("#textTiny").setContent("");
        });

        function obtenerDatosEdificio(infoid, urlConsulta) {
            if (infoid) {
                $.ajax({
                    url: urlConsulta,
                    type: "GET",
                    data: { id: infoid },
                    success: function (data) {
                        $("#isNewEdif").prop("checked", false);
                        $("#groupTitleMap").hide();
                        $(".img_form_map").slideDown();
                        $("#cancelNewEdif").show();

                        $("#mapTitle").text(data.titulo);
                        $("#formTitle").val(data.titulo);
                        tinymce.get("textTiny").setContent(data.informacion);

                        const oldImgUrl = data.imagen_url;
                        let newImgUrl;
                        let suggestImgText;

                        if (data.imagen_url) {
                            $("#suggestImg").hide();
                            newImgUrl = oldImgUrl.replace("/cross_asistent", "");
                            suggestImgText = "(Opcional)";
                        } else {
                            $("#suggestImg").show();
                            newImgUrl = "/static/img/default_image.webp";
                            suggestImgText = "(fachada)";
                        }
                        $("#suggestImgText").text(suggestImgText);
                        $("#imagen_actual").attr("src", newImgUrl);
                    },
                });
            }
        }

        $("#selectEdif").change(function () {
            var infoid = $(this).val();
            const urlConsulta = $(this).data("second-action");
            obtenerDatosEdificio(infoid, urlConsulta);
        });

        $("#color_picker").on("input", function () {
            var color = $(this).val();
            $("#color").val(color);
            $("#colorVal").text(color);
        });

        // js de subir banners inputs
        const inputCleared = $("input[data-init-clear], textarea[data-init-clear]");

        // Itera sobre cada input y textarea seleccionado
        inputCleared.each(function () {
            // Añade un evento 'input' a cada input y textarea
            $(this).on("input", function () {
                let idInput = $(this).attr("id");
                let btnCleared = $(`[data-clear="${idInput}"]`);

                // Muestra u oculta el botón dependiendo del valor del input o textarea
                if ($(this).val() == "") {
                    btnCleared.hide();
                } else {
                    btnCleared.show();
                }
            });
        });

        // Selecciona todos los elementos con el atributo data-clear
        const btnCleared = $("[data-clear]");
        btnCleared.on("click", function () {
            const dataClear = $(this).attr("data-clear");
            // Limpia el valor del input o textarea correspondiente y oculta el botón
            $(`#${dataClear}`).val("");
            $(this).slideUp("fast");
        });

        // Marcar todas las notificaciones como leídas al hacer clic en el botón
        $("#markAsReadButton").on("click", function () {
            $('[id^="notif_"]').each(function () {
                $(this).removeClass(
                    "list-group-item-warning list-group-item-info list-group-item-success list-group-item-danger list-group-item-primary"
                );
            });
            $('[id^="notif_"]').each(function () {
                $(this).addClass("list-group-item-secondary");
            });
            // Obtener todas las IDs que quieres guardar
            var notificationIds = [];
            $('[id^="notif_"]').each(function () {
                notificationIds.push($(this).attr("id"));
            });
            // guardar JSON
            localStorage.setItem("notificationIds", JSON.stringify(notificationIds));
        });

        // Manejar el evento change de los checkboxes
        $(".notification-checkbox").on("change", function () {
            var checkbox = $(this);
            var id = checkbox.data("id");
            var valPost = checkbox.data("val-post");
            var ids = [id];
            $.ajax({
                url: valPost,
                method: "POST",
                data: JSON.stringify({ ids: ids }),
                contentType: "application/json",
                headers: {
                    "X-CSRFToken": formToken,
                },
                success: function (response) {
                    message = response.message;
                    if (response.status === "success") {
                        checkbox
                            .closest("li")
                            .removeClass(
                                "list-group-item-warning list-group-item-info list-group-item-success list-group-item-danger list-group-item-primary"
                            )
                            .addClass("list-group-item-secondary");
                        setTimeout(() => {
                            checkbox.slideUp();
                        }, 2000);
                    } else {
                        console.error(message);
                    }
                    alertSToast("top", 4000, response.icon, message);
                },
            });
        });

        // Cambiar colores de la Interfaz
        $("[data-change-color]").on("click", function () {
            $("[data-change-color]").each(function (index, item) {
                $(item).removeClass("active");
            });
            var color = $(this).addClass("active").data("change-color");
            var rgb = $(this).data("rgb");
            $("body").attr("data-color_prefer", color);
            localStorage.setItem("data-color_prefer", color);
            localStorage.setItem("data-color_rgb", rgb);
        });

        // Cambiar tema
        $("#switchTheme").on("click", function () {
            if ($("#switchTheme").is(":checked")) {
                $("#switchText").text("Claro");
                $("html").attr("data-mdb-theme", "light");
                localStorage.setItem("data-mdb-theme", "light");
            } else {
                $("#switchText").text("Oscuro");
                $("html").attr("data-mdb-theme", "dark");
                localStorage.setItem("data-mdb-theme", "dark");
            }
        });

        // ####################################################
        // ####################################################
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

function cadenaRandom(longitud, caracteres) {
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
}

// Enviar formulario JSON ######################################################################
function jsonSubmit(e) {
    e.preventDefault();
    const thisForm = e.target;
    const formData = new FormData(thisForm);

    if (formData.has("contenidoWord")) {
        const contenidoTiny = tinymce.activeEditor.getContent();
        formData.set("contenidoWord", contenidoTiny);
        const contenidoTextTiny = tinymce.activeEditor.getContent({ format: "text" });
        formData.set("textTiny", contenidoTextTiny);
    }

    fetch(thisForm.action, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": formToken,
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
                dataIcon = "success";
                if (data.icon) {
                    dataIcon = data.icon;
                }

                dataPosition = "center";
                if (data.position) {
                    dataPosition = data.position;
                }

                function dataRedirect(params) {
                    window.location.href = data.redirect_url;
                }

                if (data.functions == "singin") {
                    dataRedirect();
                    return;
                } else if (data.functions == "reload") {
                    var alertfunction = function () {
                        location.reload();
                    };
                } else if (data.functions == "redirect") {
                    var alertfunction = function () {
                        dataRedirect();
                    };
                }

                alertSToast(dataPosition, timerOut, dataIcon, dataMessage, alertfunction);
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

// Funcion de preguntar a chatGPT ######################################################################
var contOutput = document.querySelector("#output");
var btnCloseChat = $("#closeChat");

function chatSubmit(e) {
    e.preventDefault();
    const pregunta = txtQuestion.value;
    const chatForm = e.target;
    this.reset();

    if (!texto3.test(pregunta)) {
        return alertSToast("center", 6000, "warning", "Por favor, escribe una pregunta 🧐😬");
    }

    var tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const htmlBlock = `
        <div class="output_block">
            <div class="btn_detail chat_msg user_submit" data-tokeid="${valID}">
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

                const dataImage = data.answer.imagenes;
                const dataRedirigir = data.answer.redirigir;

                console.log("img:" + typeof dataImage);
                console.log("url:" + typeof dataRedirigir);

                let viewImage = "";
                let btnRedir = "";

                if (dataImage != null) {
                    viewImage = `<br><br> <img src="${dataImage}" class="img-fluid rounded" width="350">`;
                }

                if (dataRedirigir != null) {
                    btnRedir = `<br><br> <a class="btn btn_detail mb-2" style="min-width:300px;" target="_blank" rel="noopener noreferrer" href="${dataRedirigir}" >Ver Mas <i class="fa-solid fa-arrow-up-right-from-square ms-1"></i></a>`;
                }
                const htmlBlock = `
                <div class="chat_msg asistent_response" data-tokeid="${valID}">
                    <span>${data.answer.informacion}  ${btnRedir} </span>
                    <span>${viewImage} </span>
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

if (btnCloseChat && contOutput) {
    btnCloseChat.on("click", function () {
        // Crear y mostrar el mensaje de saludo
        const valID = `uuid${cadenaRandom(5, alfabetico)}`;
        const saludo = "Hola 👋 ¡Bienvenido! Soy tu asistente virtual ¿En qué puedo ayudarte hoy?";
        const htmlBlock = `
                    <div class="btn_detail chat_msg asistent_response" data-tokeid="${valID}">
                        <span>${saludo}</span>
                    </div>`;

        contOutput.insertAdjacentHTML("beforeend", htmlBlock);

        const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);
        setTimeout(function () {
            asistent_response.classList.add("visible");
            scrollToBottom();
        }, 20);
    });
}

// Función para hacer scroll hacia abajo
function scrollToBottom() {
    contOutput.scrollTop = contOutput.scrollHeight;
}
// Hacer scroll con un nuevo mensaje en el chat ######################################################################
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

// Copiar al portapapeles ######################################################################
function copyValInput() {
    const inputs = document.querySelectorAll("input[data-copy]");
    inputs.forEach((input) => {
        const copyText = () => {
            if (!navigator.clipboard) {
                alertSToast("center", 8000, "info", "Tu navegador no admite copiar al portapapeles 😯😥🤔");
                return;
            }
            const textCopy = input.value;
            if (textCopy != "") {
                navigator.clipboard
                    .writeText(textCopy)
                    .then(() => {
                        alertSToast("top", 5000, "success", "Texto Copiado! 🥳");
                    })
                    .catch((error) => {
                        const message = "Error al copiar al portapapeles";
                        console.error(message, ":", error);
                        alertSToast("top", 8000, "error", `${message} 🤔😥`);
                    });
            }
        };

        input.addEventListener("click", copyText);
        input.addEventListener("focus", copyText);
    });
}

copyValInput();

// context menu disabled ######################################################################
document.oncontextmenu = function () {
    return false;
};

// MaterialBox ######################################################################
var imagesZoom = document.querySelectorAll(".materialBoxed");
var instances = M.Materialbox.init(imagesZoom);

// Template Alertas switalert ######################################################################
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
