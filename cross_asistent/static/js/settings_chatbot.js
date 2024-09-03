var alfabetico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12345678901234567890";
var texto3 = /[a-zA-Z0-9]{3}/;
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

let microphonerecord = false;
let newMessageChat = false;
let lastText = ""; // Definir lastText a nivel global

// ##############################################################################################
// ###################################### Funciones Jquery ######################################
// ##############################################################################################
$(document).ready(function () {
    try {
        // abrir menu del asistente ##############################################################
        $(".controls_btn_microphone").click(() => {
            $(".asistent_group").addClass("open open_controls bg-body-tertiary");
            $(".btn_controls").addClass("text-white");
            $("#btn_controls_icon").removeClass("fa-comment").addClass("fa-microphone");
            setTimeout(() => {
                $(".btn_controls").addClass("readyRecVoice");
            }, 1100);
        });
        $(".toggle_controls").click(() => {
            microphonerecord = false;
            $(".asistent_group.open").toggleClass("close_controls open_keyboard open_controls");
            if (!isMobile) {
                setTimeout(function () {
                    $(".controls_input #txtQuestion").focus();
                }, 1500);
            }
        });
        $(".controls_btn_close").click(() => {
            $(".asistent_group").removeClass("open open_controls close_controls open_keyboard bg-body-tertiary");
            $(".btn_controls").removeClass("readyRecVoice");
            $("#btn_controls_icon").addClass("fa-comment").removeClass("fa-microphone");
            stopRecording();
        });

        // Enviar chat con enter chatGPT ######################################
        $("#txtQuestion").keydown((evento) => {
            if (evento.keyCode === 13 && !evento.shiftKey) {
                evento.preventDefault();
                $("#chatForm_submit").click();
            }
        });

        // ChatGPT Submit ####################################################
        $("#chatForm").submit(chatSubmit);
    } catch (error) {
        console.error("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ha ocurrido un error inesperado. código: #304`);
    }
});

// ##############################################################################################
// #################################### Funciones JAVASCRIPT ####################################
// ##############################################################################################

// Función de preguntar a chatGPT https://platform.openai.com/ #################################
const contOutput = document.querySelector("#output");
let audioEnabled = true;
let saludoMostrado = true;

// Función para Mostrar y Mandar la Pregunta del Usuario ################
function chatSubmit(e) {
    newMessageChat = true;
    e.preventDefault();
    const pregunta = txtQuestion.value;
    const chatForm = e.target;
    chatForm.reset();

    if (!texto3.test(pregunta)) {
        return alertSToast("center", 6000, "warning", "Por favor, envía una pregunta más descriptiva 🧐😯😬");
    }

    const tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const htmlBlock = `<div class="output_block"><div class="bg_detail chat_msg user_submit" data-tokeid="${valID}">${pregunta}</div></div>`;
    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const user_submit = document.querySelector(`.user_submit[data-tokeid="${valID}"]`);
    setTimeout(() => {
        user_submit.classList.add("visible");
        setTimeout(scrollToBottom, 500);
    }, 20);

    const loadInfo = `<div class="chat_msg asistent_response my-4" data-tokeid="loadInfoDelete"><div class="pulse-container"><div class="pulse-bubble bg_detail pulse-bubble-1"></div><div class="pulse-bubble bg_detail pulse-bubble-2"></div><div class="pulse-bubble bg_detail pulse-bubble-3"></div></div></div>`;
    contOutput.insertAdjacentHTML("beforeend", loadInfo);
    setTimeout(function () {
        document.querySelector(`.asistent_response[data-tokeid="loadInfoDelete"]`).classList.add("visible");
        setTimeout(scrollToBottom, 500);
    }, 200);

    if (microphonerecord) {
        $("#speak_btn_icon").removeClass("fa-regular fa-circle-play").addClass("fa-solid fa-spinner fa-spin-pulse");
    }

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
                if (microphonerecord) {
                    $("#speak_btn_icon")
                        .removeClass("fa-regular fa-circle-play fa-spinner fa-spin-pulse")
                        .addClass("fa-solid fa-circle-pause");
                }
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
function displayChatbotResponse(varAnswer) {
    const tokendid = cadenaRandom(5, alfabetico);
    const valID = `uuid${tokendid}`;

    const dataImage = varAnswer.imagenes;
    const dataRedirigir = varAnswer.redirigir;
    const dataRedirigirBlank = varAnswer.blank;

    let viewImage = "";
    let btnBlanck = "";
    let btnRedir = "";

    if (dataImage != null) {
        viewImage = `<br><br> <img src="${dataImage}" class="img-rounded max_w300 max_h350">`;
    }

    if (dataRedirigirBlank) {
        btnBlanck = 'target="_blank" rel="noopener noreferrer"';
    }

    if (dataRedirigir && dataRedirigir.trim() !== "") {
        btnRedir = `<br><br> <a class="btn bg_detail mb-2 max_w300" ${btnBlanck} href="${dataRedirigir}" >Ver Más <i class="fa-solid fa-arrow-up-right-from-square ms-1"></i></a>`;
    }

    lastText = varAnswer.informacion;
    const htmlBlock = `<div class="chat_msg asistent_response" data-tokeid="${valID}">${lastText} ${btnRedir} ${viewImage}</div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);
    document.querySelector(`.asistent_response[data-tokeid="loadInfoDelete"]`).remove();
    setTimeout(function () {
        asistent_response.classList.add("visible");
        setTimeout(scrollToBottom, 350);
    }, 20);
}

// Saludo Inicial ######################
if (contOutput && saludoMostrado) {
    const initialMessage = `<div class="chat_msg asistent_response" data-tokeid="initialMessage"><span>¡Hola!!! Soy Hawky 👋😁, tu asistente virtual de la Universidad Tecnológica de Coahuila! <br>¿En qué puedo ayudarte? 🫡🤘😋</span></div>`;

    contOutput.insertAdjacentHTML("beforeend", initialMessage);
    const elementInitMsg = document.querySelector(`.asistent_response[data-tokeid="initialMessage"]`);
    setTimeout(function () {
        elementInitMsg.classList.add("visible");
    }, 500);
}

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
