var alfabetico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
var alfanumerico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890123456789";
var caracteres = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890123456789@$!%*.?&";
var texto3 = /[a-zA-Z0-9]{3}/;
var formToken = getCSRFToken();
var timerOut = 5000;
var expressions = {
    name: /^[a-zA-ZÀ-ÿ\s]+$/,
    username: /^(?![0-9_-])[a-zA-Z0-9_-]+$/,
    email: /^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*.?&])[A-Za-z\d@$!%*.?&]{8,}$/,
};

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

// ##############################################################################################
// ###################################### Funciones Jquery ######################################
// ##############################################################################################
$(document).ready(function () {
    try {
        // Detectar cuando se abre cualquier modal
        $(".modal").on("shown.bs.modal", function (e) {
            $("body").addClass("body_minus");
        });
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
        if ($("[data-submit-form]").is("[data-submit-ready]")) {
            setTimeout(() => {
                $('[data-submit-ready] button[type="submit"]').click();
            }, 2000);
        }
        $("[data-submit-blur] .input_blur").on("blur", function () {
            $("[data-submit-blur] button[type='submit']").click();
        });
        $("[data-submit-blur] .input_change").on("change", function () {
            $("[data-submit-blur] button[type='submit']").click();
        });

        // $("[id^='btn_frequence']").each(function() {
        //     console.log($(this).attr('id'));
        // });

        $("[data-submit-click]").on("click", function () {
            const btnSubmitThis = $(this).data("submit-click");
            $("#" + btnSubmitThis)
                .click()
                .attr("disabled", "disabled");

            if (!disabledButtons.includes(btnSubmitThis)) {
                disabledButtons.push(btnSubmitThis);
            }
            localStorage.setItem("disabledButtons", JSON.stringify(disabledButtons));
        });

        // Editar/Crear usuario
        // generar nueva contraseña aleatoria #################################
        $("button[data-editinput]").click(genpass);
        function genpass() {
            $(this).addClass("active");
            var newRandomPass = cadenaRandom(10, caracteres);
            var editInputId = $(this).data("editinput");
            setTimeout(() => {
                $(this).removeClass("active");
            }, 1000);
            $("#" + editInputId)
                .val(`UTC${newRandomPass}`)
                .addClass("active");
        }

        // Quitar clase show #####################################
        $("[data-btn_closed]").on("click", function () {
            var targetId = $(this).data("btn_closed");
            $("#" + targetId).toggleClass("show");
        });

        // Resetear formulario / vaciar todo el formulario
        $("[data-reset_form]").on("click", function () {
            var formId = $(this).data("reset_form");
            var formElement = $("#" + formId)[0];
            setTimeout(() => {
                if (formElement) {
                    formElement.reset();
                }
            }, 1500);
        });

        // Estilo Texto Google ####################################
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

        // Limpiar valor de input ##################################################################
        const inputCleared = $("input[data-init-clear], textarea[data-init-clear]");
        inputCleared.each(function () {
            $(this).on("input", function () {
                let idInput = $(this).attr("id");
                let btnCleared = $(`[data-clear="${idInput}"]`);

                if ($(this).val() == "") {
                    btnCleared.hide();
                } else {
                    btnCleared.show();
                }
            });
        });
        const btnCleared = $("[data-clear]");
        btnCleared.on("click", function () {
            const dataClear = $(this).attr("data-clear");
            $(`#${dataClear}`).val("");
            $(this).slideUp("fast");
        });

        // Notificaciones #############################################################
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
        // Cargar las IDs desde localStorage
        var storedIds = JSON.parse(localStorage.getItem("notificationIds")) || [];
        storedIds.forEach(function (id) {
            $("#" + id).removeClass(
                "list-group-item-warning list-group-item-info list-group-item-success list-group-item-danger list-group-item-primary"
            );
            $("#" + id).addClass("list-group-item-secondary");
        });

        // Interfaz #########################################################
        // Cambiar colores de la Interfaz
        $("[data-change-color]").on("click", function () {
            $("[data-change-color]").each(function (index, item) {
                $(item).removeClass("active");
            });
            var color = $(this).addClass("active").data("change-color");
            var rgb = $(this).data("rgb");
            $("html").attr("data-color_prefer", color);
            localStorage.setItem("data-color_prefer", color);
            localStorage.setItem("data-color_rgb", rgb);
        });
        const colorPrefer = localStorage.getItem("data-color_prefer");
        if (colorPrefer) {
            $(`[data-change-color="${colorPrefer}"]`).addClass("active");
            $("html").attr("data-color_prefer", colorPrefer);
        } else {
            $('[data-change-color="blue"]').addClass("active");
            $("html").attr("data-color_prefer", "blue");
        }
        // Cambiar tema
        $("#switchTheme").on("click", function () {
            if ($("#switchTheme").is(":checked")) {
                $("#switchText").text("Claro");
                $("html").attr("data-mdb-theme", "light");
                localStorage.setItem("data-mdb-theme", "light");
                localStorage.setItem("mapbox-last_layer", "light-v11");
            } else {
                $("#switchText").text("Oscuro");
                $("html").attr("data-mdb-theme", "dark");
                localStorage.setItem("data-mdb-theme", "dark");
                localStorage.setItem("mapbox-last_layer", "dark-v11");
            }
        });
        const colorTheme = localStorage.getItem("data-mdb-theme");
        if (colorTheme) {
            if (colorTheme == "light") {
                $("#switchText").text("Claro");
                $("#switchTheme").prop("checked", true);
                $("html").attr("data-mdb-theme", "light");
                localStorage.setItem("mapbox-last_layer", "light-v11");
            } else if (colorTheme == "dark") {
                $("#switchText").text("Oscuro");
                $("#switchTheme").prop("checked", false);
                $("html").attr("data-mdb-theme", "dark");
                localStorage.setItem("mapbox-last_layer", "dark-v11");
            }
        }

        // Firma del blog ##################################################
        // obtener texto sin espacios en inicio y final (trim)
        const oldSignature = $.trim($("#firmaPerfilTexto").text());
        $("#new_firma").on("input", function () {
            const inputText = $(this).val();

            // Verificar si el texto está vacío
            if (inputText.trim() === "") {
                $("#firmaPerfilTexto").text(oldSignature);
            } else {
                $("#firmaPerfilTexto").text(inputText);
            }
        });

        // Colocar imagen del input file #############################################
        function readURL(input, elementId) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $(`#${elementId}`).attr("src", e.target.result);
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
        $("[data-img_dom]").change(function () {
            idImgDom = $(this).data("img_dom");
            readURL(this, idImgDom);
        });

        // Inpits del perfil ##########################################################
        $("[data-input_transparent]").on({
            focus: function () {
                $(this).toggleClass("input_transparent");
            },
            blur: function () {
                $(this).toggleClass("input_transparent");
            },
        });
        var otherChanges = false;
        function togglePassBlock() {
            if (otherChanges) {
                $("#updatePassBlock").slideUp("fast");
            } else {
                $("#profileSaved").slideUp("fast", function () {
                    $("#updatePassBlock").slideUp("fast");
                });
            }
        }
        // Poner visible la seccion de la password
        $("#updatePassBtn").on("click", function () {
            let thisBtn = $(this);
            $("#updatePassText").toggle();

            if ($("#updatePassBtn").hasClass("bg_blue-green")) {
                $("#profileSaved").slideDown("fast", function () {
                    $("#updatePassBlock").slideDown("fast", function () {
                        $("html, body").scrollTop($(document).height());
                    });
                });
            } else {
                togglePassBlock();
            }
            if (thisBtn.text() == "Cambiar Contraseña") {
                thisBtn.toggleClass("bg_blue-green bg_blue-red");
                thisBtn.text("No Cambiar Contraseña");
                if (!otherChanges) {
                    $("#passwordSend").val("");
                }
                $("#newPass").val("");
                $("#confNewPass").val("");
            } else {
                thisBtn.toggleClass("bg_blue-green bg_blue-red");
                thisBtn.text("Cambiar Contraseña");
            }
        });
        // Detectar cambios en los inputs
        $("[data-input_change]").each(function () {
            const thisInput = $(this);
            const originalNameInput = thisInput.attr("name");
            var oldValueInput = thisInput.val();
            var oldNameInput = originalNameInput;

            thisInput.on("input", function () {
                if (thisInput.val() == oldValueInput) {
                    thisInput.attr("name", `${originalNameInput}`);
                    togglePassBlock();
                    otherChanges = false;
                } else {
                    thisInput.attr("name", `${originalNameInput}Changed`);
                    $("#profileSaved").slideDown("fast");
                    otherChanges = true;

                    if (thisInput.val() == "") {
                        thisInput.attr("name", `${originalNameInput}`);
                    }
                }
            });

            thisInput.on("blur", function () {
                if (thisInput.val() == "") {
                    thisInput.attr("name", `${originalNameInput}`);
                    togglePassBlock();
                    otherChanges = false;
                }
            });

            thisInput.on("click", function () {
                oldNameInput = originalNameInput;
            });
        });
        // Desplegar boton si se elimina la foto de perfil
        $("input#deletePicture").change(function () {
            if ($(this).is(":checked")) {
                $('[for="deletePicture"]').addClass("btn_press");
                $("#profileSaved").slideDown("fast");
                otherChanges = true;
            } else {
                $('[for="deletePicture"]').removeClass("btn_press");
                togglePassBlock();
                otherChanges = false;
            }
        });

        // Editar Blog ################################################################
        $("#formularioArticulo #blogNewUpdate").change(function () {
            blogIdGet = $("#formularioArticulo #blogNewUpdate").val();
            dataGetBlog = $("#formularioArticulo #blogNewUpdate").data("get-blog");
            if (blogIdGet != "newBlog") {
                $.ajax({
                    url: dataGetBlog,
                    type: "GET",
                    data: { id: blogIdGet },
                    success: function (data) {
                        $("#formularioArticulo #imgArticle").attr("src", "/static/img/default_image.webp");
                        if (data.encabezado) {
                            $("#formularioArticulo #imgArticle").attr("src", data.encabezado);
                        }
                        $("#formularioArticulo #titulo").addClass("active").val(data.titulo);
                        const blogContent = data.contenido;
                        tinymce.get("mainTiny").setContent(blogContent);
                        $("#formularioArticulo .blogSubmit").html(
                            'Modificar <i class="fa-regular fa-paper-plane ms-1"></i>'
                        );
                        $("#formularioArticulo .btnModal").slideDown("fast");
                        $("#blogDelete #blogDeleteTitle").text(data.titulo);
                        $("#blogDelete #blogIdDelete").val(blogIdGet);
                    },
                    error: function (error) {
                        console.error("Error al obtener datos: " + error);
                        alertSToast(
                            "center",
                            8000,
                            "error",
                            "UPS! 😯🤔🧐<br> hubo un error al obtener los datos, consulte la consola."
                        );
                    },
                });
            } else {
                $("#formularioArticulo #imgArticle").attr("src", "/static/img/default_image.webp");
                $("#formularioArticulo #titulo").removeClass("active").val("");
                tinymce.get("mainTiny").setContent("");
                $("#formularioArticulo .blogSubmit").html('Publicar <i class="fa-regular fa-paper-plane ms-1"></i>');
                $("#formularioArticulo .btnModal").slideUp("fast");
                $("#blogDelete #blogDeleteTitle").text("");
                $("#blogDelete #blogIdDelete").val("");
            }
        });

        // Editar Evento -Calendario ######################################
        // Cambiar clase del select option
        $("[data-select_addClass]").change(function () {
            const newClass = $(this).val();
            $(this).attr("class", `form-select change_bg ${newClass}`);
        });

        //
        //
        //
    } catch (error) {
        console.error("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ah ocurrido un error inesperado. codigo: #304`);
    }
});

// ##############################################################################################
// #################################### Funciones JAVASCRIPT ####################################
// ##############################################################################################

// Cerrar la sesion ##########################################################
if (document.querySelector("main").classList.contains("main_container")) {
    window.location.href = "/logout";
}

// Crear cadena de caracteres random ###############################3
function cadenaRandom(longitud, caracteres) {
    var cadenaAleatoria = "";
    for (var i = 0; i < longitud; i++) {
        var indice = Math.floor(Math.random() * caracteres.length);
        cadenaAleatoria += caracteres.charAt(indice);
    }
    return cadenaAleatoria;
}

// Funcion de preguntar a chatGPT https://platform.openai.com/ #################################
const contOutput = document.querySelector("#output");
const toggleAudioButton = document.querySelector("#toggleAudio");
const audioIcon = document.querySelector("#audioIcon");
const RepAudioButton = document.querySelector("#RepAudio");
let audioEnabled = true;
let saludoMostrado = false;

// Funcion para Controlar el Audio ######################
function playAudio(audioUrl) {
    if (audioUrl && audioEnabled) {
        const audio = new Audio(audioUrl);
        audio.playbackRate = 1.5;

        audio.play().catch((error) => {
            console.error("Error al reproducir el audio:", error);
        });
        const checkAudioState = setInterval(function () {
            if (!audioEnabled) {
                audio.pause();
            }
        }, 100);
        audio.addEventListener("ended", function () {
            clearInterval(checkAudioState);
        });
    }
}

// Funcion para Mostrar y Mandar la Pregunta del Usuario ################
function chatSubmit(e) {
    e.preventDefault();
    const pregunta = txtQuestion.value;
    const chatForm = e.target;
    chatForm.reset();

    if (!texto3.test(pregunta)) {
        return alertSToast("center", 6000, "warning", "Por favor, escribe una pregunta 🧐😬");
    }

    const tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const htmlBlock = `<div class="output_block"><div class="btn_detail chat_msg user_submit" data-tokeid="${valID}">${pregunta}</div></div>`;
    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const user_submit = document.querySelector(`.user_submit[data-tokeid="${valID}"]`);
    setTimeout(() => {
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
                displayChatbotResponse(data.answer);
            } else {
                alertSToast("top", 8000, "error", `Error: ${data.message}`);
            }
        })
        .catch((error) => {
            console.error("😥 Error:", error);
            alertSToast("top", 8000, "warning", "Ocurrió un error. Intente nuevamente. 😥");
        });
}

// Función para Manejar y Mostrar la Respuesta del Chatbot #################
function displayChatbotResponse(answer) {
    const tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const dataImage = answer.imagenes;
    const dataRedirigir = answer.redirigir;
    const dataAudio = answer.audio_url;

    let viewImage = "";
    let btnRedir = "";

    if (dataImage != null) {
        viewImage = `<br><br> <img src="${dataImage}" class="img-rounded max_w300 max_h300">`;
    }

    if (dataRedirigir && dataRedirigir.trim() !== "") {
        btnRedir = `<br><br> <a class="btn btn_detail mb-2 max_w300" target="_blank" rel="noopener noreferrer" href="${dataRedirigir}" >Ver Mas <i class="fa-solid fa-arrow-up-right-from-square ms-1"></i></a>`;
    }

    const htmlBlock = `<div class="chat_msg asistent_response" data-tokeid="${valID}">${answer.informacion} ${btnRedir} ${viewImage}</div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);

    setTimeout(function () {
        asistent_response.classList.add("visible");
        setTimeout(scrollToBottom, 350);

        playAudio(dataAudio);
    }, 20);
}

// Menejar el Saludo Inicial ######################
if (contOutput && !saludoMostrado) {
    const valID = `uuid${cadenaRandom(5, alfabetico)}`;
    const htmlBlock = `<div class="chat_msg asistent_response" data-tokeid="${valID}"><span>Hola!!! Soy Hawky, tu asistente virtual de la Universidad Tecnologica de Coahuila! <br>¿En qué puedo ayudarte?</span></div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);

    const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);
    setTimeout(function () {
        asistent_response.classList.add("visible");
        scrollToBottom();
    }, 220);

    RepAudioButton.addEventListener("click", function () {
        if (!saludoMostrado) {
            playAudio("/static/audio/welcome.mp3");
        }
        saludoMostrado = true;
    });
}

// Función para Actualizar el Chat con la Pregunta del Usuario por Voz###########
function updateChat(question) {
    const tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const htmlBlock = `<div class="output_block"><div class="btn_detail chat_msg user_submit" data-tokeid="${valID}">${question}</div></div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const userSubmit = document.querySelector(`.user_submit[data-tokeid="${valID}"]`);
    setTimeout(() => {
        userSubmit.classList.add("visible");
        setTimeout(scrollToBottom, 500);
    }, 20);
}
function scrollToBottom() {
    contOutput.scrollTop = contOutput.scrollHeight;
}

// Control de Boton de Audio #########################

if (toggleAudioButton && audioIcon) {
    toggleAudioButton.addEventListener("click", function () {
        audioEnabled = !audioEnabled;
        if (audioEnabled) {
            audioIcon.classList.remove("fa-volume-mute");
            audioIcon.classList.add("fa-volume-high");
        } else {
            audioIcon.classList.remove("fa-volume-high");
            audioIcon.classList.add("fa-volume-mute");
        }
    });
}

// Control de Reconocimiento de Voz #########################
const recVoice = document.getElementById("recVoice");
let isRecognizing = false;

if (recVoice) {
    const startRecognitionUrl = recVoice.getAttribute("data-start");
    const stopRecognitionUrl = recVoice.getAttribute("data-stop");

    recVoice.addEventListener("click", () => {
        if (isRecognizing) {
            stopRecognition(stopRecognitionUrl);
        } else {
            startRecognition(startRecognitionUrl);
        }
    });
}

function startRecognition(startRecognitionUrl) {
    fetch(startRecognitionUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                isRecognizing = true;
                recVoice.innerHTML = '<i class="fa-solid fa-stop"></i>';
            } else {
                console.error("Error:", data.message);
            }
        });
}

function stopRecognition(stopRecognitionUrl) {
    fetch(stopRecognitionUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}",
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                isRecognizing = false;
                recVoice.innerHTML = '<i class="fa-solid fa-microphone"></i>';

                if (data.response) {
                    if (data.response.question) {
                        const question = data.response.question;
                        updateChat(question);
                    }
                    if (data.response.chatbot_answer) {
                        const chatbotAnswer = data.response.chatbot_answer;
                        displayChatbotResponse(chatbotAnswer);
                    }
                }
            } else {
                console.error("Error:", data.message);
            }
        })
        .catch((error) => console.error("Error en la solicitud:", error));
}

// Hacer scroll con un nuevo mensaje en el chat ####################
function scrollToBottom() {
    contOutput.scrollTop = contOutput.scrollHeight;
}
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
    // input.addEventListener("focus", copyText);
});

// MaterialBox https://materializecss.com/ ################################################
var imagesZoom = document.querySelectorAll(".materialBoxed");
var instances = M.Materialbox.init(imagesZoom);

// $(".materialBoxed").click(function () {
//     if($(this).hasClass('active')) {
//         // $(".navbar-collapse").css('z-index', 0);
//         $(".navbar-collapse").css('background', 'blue');
//     } else {
//         $(".navbar-collapse").css('background', 'red');
//     }
// })

// Enviar formulario JSON ######################################################################
function jsonSubmit(e) {
    e.preventDefault = e.preventDefault || function () {};
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
            if (data.success == true) {
                // thisForm.reset();
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

                const passwordInputs = document.querySelectorAll('input[type="password"]');
                passwordInputs.forEach((input) => (input.value = ""));

                alertSToast(dataPosition, timerOut, dataIcon, dataMessage, alertfunction);
            } else if (data.success == false) {
                console.error(dataMessage);

                if (data.valSelector) {
                    console.log(data.valSelector);
                    function addInvalidClass(valueSelector) {
                        document.querySelector(`[data-selector-input="${valueSelector}"]`).classList.add("is-invalid");
                        document.querySelector(`[data-selector-input="${valueSelector}"]`).classList.remove("is-valid");
                    }
                    addInvalidClass(data.valSelector);
                }

                alertSToast("top", timerOut + 6000, "warning", dataMessage);
            }
        })
        .catch((error) => {
            console.error("😥 Error:", error);
            errorMessage = error.message || "Ocurrió un error. Intente nuevamente. 😥";
            alertSToast("center", timerOut + 8000, "error", errorMessage);
        });
}

// alertSToast('top', 8000, 'success', '<br>lo normal');
// Template Alertas switalert ###################################################
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

// context menu disabled ######################################################################
document.oncontextmenu = function () {
    return false;
};
