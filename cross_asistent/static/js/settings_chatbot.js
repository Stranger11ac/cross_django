var alfabetico = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12345678901234567890";
var texto3 = /[a-zA-Z0-9]{3}/;
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

let microphonerecord = false;
let newMessageChat = false;
let lastText = "";
let microphoneSpeech = true;
let isSpeaking = false;

// Activar y desactivar micrófono ###########################################
const recVoice = $(".controls_btn_microphone");
const textarea = document.getElementById("txtQuestion");
const submitButton = document.getElementById("chatForm_submit");
let finalTranscript = "";
let recognition;
let recognizing = false;

// Dictado de texto ##################################
const speakButton = $(".speak_btn");
const voiceSelect = document.getElementById("voice_select");
const rateInput = document.getElementById("rate_input");

// ##############################################################################################
// ###################################### Funciones Jquery ######################################
// ##############################################################################################
$(document).ready(function () {
    try {
        // abrir menu del asistente ##############################################################
        recVoice.click(() => {
            $(".asistent_group").addClass("open open_controls");
            $(".btn_controls").addClass("text-white");
            changeMicrophone();
            setTimeout(() => {
                $(".btn_controls").addClass("readyRecVoice");
            }, 1100);
        });
        function changeMicrophone() {
            if (microphoneSpeech) {
                $("#btn_controls_icon").removeClass("fa-comment").addClass("fa-microphone");
            } else {
                $("#btn_controls_icon").removeClass("fa-comment").addClass("fa-microphone-slash");
            }
        }
        if ($(".asistent_group").hasClass("open")) {
            changeMicrophone();
        }
        // Abrir chat #######################
        $(".toggle_controls").click(() => {
            microphonerecord = false;
            const asistentGroup = $(".asistent_group.open");
            asistentGroup.toggleClass("close_controls open_keyboard open_controls");
            if (!isMobile) {
                setTimeout(function () {
                    $(".controls_input #txtQuestion").focus();
                }, 900);
            }

            let modelViewer = $("#asistent_model");
            const hdrSaved = localStorage.getItem("model_hdr");

            if (asistentGroup.hasClass("open_keyboard")) {
                $("#changeScene").addClass("none").css("--delay", "7");
                modelViewer.attr("environment-image", "");
                modelViewer.attr("skybox-image", "");
            } else {
                $("#changeScene").removeClass("none").css("--delay", "3");
                if (hdrSaved != "") {
                    modelViewer.attr("environment-image", `/media/hdri/${hdrSaved}.hdr`);
                    modelViewer.attr("skybox-image", `/media/hdri/${hdrSaved}.hdr`);
                } else {
                    modelViewer.attr("environment-image", "");
                    modelViewer.attr("skybox-image", "");
                }
            }
        });
        $(".controls_btn_close").click(() => {
            $(".asistent_group").removeClass("open open_controls close_controls open_keyboard");
            $(".btn_controls").removeClass("readyRecVoice");
            $("#btn_controls_icon").addClass("fa-comment").removeClass("fa-microphone");
            if (recognizing) {
                stopRecording();
            }
        });

        // Enviar chat con enter chatGPT ######################################
        $("#txtQuestion").keydown((evento) => {
            if (evento.keyCode === 13 && !evento.shiftKey) {
                evento.preventDefault();
                $("#chatForm_submit").click();
            }
        });

        // Posicion de controles del asistente ######################################
        const verticalCtrlsCheckbox = $("#vesticalCtrls");
        const boxControls = $(".box_asistent_controls");

        const isVertical = localStorage.getItem("Vertical-controls") === "true";
        boxControls.toggleClass("controls_vertical", isVertical);
        verticalCtrlsCheckbox.prop("checked", isVertical);

        verticalCtrlsCheckbox.on("click", function () {
            const isChecked = verticalCtrlsCheckbox.is(":checked");
            boxControls.toggleClass("controls_vertical", isChecked);
            localStorage.setItem("Vertical-controls", isChecked);
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

// Activar y desactivar micrófono ###########################################
try {
    // Verifica si el navegador soporta la Web Speech API
    if ("webkitSpeechRecognition" in window) {
        recognition = new webkitSpeechRecognition();
        recognition.lang = "es-MX";
        recognition.continuous = true;
        recognition.interimResults = true;

        recognition.onstart = function () {
            recognizing = true;
            microphonerecord = true;
            finalTranscript = "";
        };

        recognition.onresult = function (event) {
            let interimTranscript = "";

            for (let i = event.resultIndex; i < event.results.length; i++) {
                let transcript = event.results[i][0].transcript;

                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            textarea.value = finalTranscript + interimTranscript;
        };

        recognition.onerror = function (event) {
            console.error("Error de reconocimiento:", event.error);
            if (event.error === "not-allowed") {
                alertSToast("top", 8000, "error", "Permiso de micrófono denegado. Por favor, permite el acceso al micrófono.");
            } else if (event.error === "no-speech") {
                alertSToast("top", 8000, "error", "No se detectó ninguna voz. Por favor, intenta de nuevo.");
            } else if (event.error === "network") {
                alertSToast("top", 8000, "error", "Error de red. Por favor, verifica tu conexión.");
            }

            console.error("Error de reconocimiento: ", event.error);
            recognizing = false;
            microphonerecord = false;
            $("#btn_controls_icon").removeClass("fa-stop").addClass("fa-microphone");
            $(".btn_controls").removeClass("readyRecVoice");
        };

        recognition.onend = function () {
            recognizing = false;
            $("#btn_controls_icon").removeClass("fa-stop").addClass("fa-microphone");
        };

        function stopRecording() {
            recognition.stop();
            $("#btn_controls_icon").addClass("fa-microphone").removeClass("fa-stop");
        }

        recVoice.on("click", function () {
            if (recVoice.hasClass("readyRecVoice")) {
                if (recognizing) {
                    stopRecording();
                    setTimeout(() => {
                        submitButton.click();
                    }, 500);
                } else {
                    try {
                        isSpeaking = true;
                        speakButton.click();
                        $("#btn_controls_icon").addClass("fa-stop").removeClass("fa-microphone");
                        recognition.start();
                    } catch (error) {
                        console.error("Error al iniciar el reconocimiento: ", error);
                        alertSToast("top", 8000, "error", "No se pudo iniciar el reconocimiento de voz.");
                    }
                }
            }
        });
    } else {
        microphoneSpeech = false;
        console.warn("Este navegador no soporta la Web Speech API");
        $("#btn_controls_icon").addClass("fa-microphone-slash");
        recVoice.on("click", function () {
            alertSToast("center", 9000, "warning", "Al parecer tu navegador no permite activar el micrófono. 🤔😯😥");
        });
    }
} catch (error) {
    alertSToast("top", 10000, "warning", error);
}

// Dictado de texto ##################################
if ("speechSynthesis" in window) {
    const synth = window.speechSynthesis;

    let voices = [];
    let utterance;

    function loadVoices() {
        voices = synth.getVoices();
        voiceSelect.innerHTML = "";

        let defaultOptionAdded = false;

        voices.forEach((voice, index) => {
            if (voice.lang.startsWith("es")) {
                const option = document.createElement("option");
                option.textContent = `${voice.name} (${voice.lang})`;
                option.value = index;
                voiceSelect.appendChild(option);

                // Check for the specific voice and set it as selected if available
                if (voice.name.includes("Microsoft Sebastian") && voice.lang === "es-VE") {
                    voiceSelect.value = index;
                    defaultOptionAdded = true;
                } else if (voice.name.includes("Microsoft Raul") && voice.lang === "es-Mx") {
                    voiceSelect.value = index;
                    defaultOptionAdded = true;
                }
            }
        });

        // If the default voice is not found, select the first Spanish voice available
        if (!defaultOptionAdded && voiceSelect.options.length > 0) {
            voiceSelect.value = 0;
        }
    }

    if (synth.onvoiceschanged !== undefined) {
        synth.onvoiceschanged = loadVoices;
    }
    loadVoices();

    function removeEmojis(text) {
        return text
            .replace("*", "")
            .replace("#", "")
            .replace("(", "")
            .replace(")", "")
            .replace(">", "")
            .replace("<", "")
            .replace("br", "")
            .replace("<br>", "")
            .replace(/[\u{1F600}-\u{1F64F}]/gu, "") // Emoticonos
            .replace(/[\u{1F300}-\u{1F5FF}]/gu, "") // Símbolos y pictogramas
            .replace(/[\u{1F680}-\u{1F6FF}]/gu, "") // Transporte y símbolos de mapa
            .replace(/[\u{2600}-\u{26FF}]/gu, "") // Otros símbolos
            .replace(/[\u{2700}-\u{27BF}]/gu, "") // Símbolos de dingbats
            .replace(/[\u{1F900}-\u{1F9FF}]/gu, "") // Símbolos suplementarios
            .replace(/[\u{1FA70}-\u{1FAFF}]/gu, ""); // Objetos misceláneos
    }

    function ttsCustom(valuetext) {
        if (isSpeaking) {
            $(".speak_btn i").addClass("fa-volume-high").removeClass("fa-volume-xmark");
            synth.cancel();
            isSpeaking = false;
        } else {
            $(".speak_btn i").removeClass("fa-volume-high").addClass("fa-volume-xmark");

            valuetext = removeEmojis(valuetext);
            utterance = new SpeechSynthesisUtterance(valuetext);
            const selectedVoice = voices[voiceSelect.value];
            utterance.voice = selectedVoice;
            utterance.rate = parseFloat(rateInput.value) || 1;

            synth.speak(utterance);
            isSpeaking = true;

            utterance.onend = () => {
                isSpeaking = false;
                $(".speak_btn i").addClass("fa-volume-high").removeClass("fa-volume-xmark");
            };
        }
    }
} else {
    console.warn("Este navegador no soporta API de síntesis de voz");
    alertSToast("center", 7000, "warning", "Al parecer tu navegador no permite la API de síntesis de voz. 😯😥🥲");
}

// Espera a que el DOM se cargue para manejar el botón de hablar
document.addEventListener("DOMContentLoaded", () => {
    let initialText = $('[data-tokeid="initialMessage"]').text();
    speakButton.on("click", () => {
        if (!newMessageChat) {
            ttsCustom(initialText);
        }
    });
});

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
        $(".speak_btn i").removeClass("fa-volume-high").addClass("fa-spinner fa-spin-pulse");
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
                    $(".speak_btn i").removeClass("fa-volume-high fa-spinner fa-spin-pulse").addClass("fa-volume-xmark");
                }
                displayChatbotResponse(data.answer);
            } else {
                console.error("😥 Error:", data.message);
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
        btnRedir = `<br><br> <a class="btn bg_detail mb-2 max_w300" ${btnBlanck} href="${dataRedirigir}" >Ver Más <i class="fa-solid fa-up-right-from-square ms-1"></i></a>`;
    }

    lastText = varAnswer.informacion;
    chatText = varAnswer.informacion.replace(/\n/g, "<br>");
    const htmlBlock = `<div class="chat_msg asistent_response" data-tokeid="${valID}">${chatText} ${viewImage} ${btnRedir}</div>`;

    contOutput.insertAdjacentHTML("beforeend", htmlBlock);
    const asistent_response = document.querySelector(`.asistent_response[data-tokeid="${valID}"]`);
    document.querySelector(`.asistent_response[data-tokeid="loadInfoDelete"]`).remove();
    setTimeout(function () {
        asistent_response.classList.add("visible");
        setTimeout(scrollToBottom, 350);

        if (microphonerecord) {
            let speachText = $(`[data-tokeid="${valID}"]`).text();
            ttsCustom(speachText);
        }
    }, 20);
}

speakButton.on("click", () => {
    if (newMessageChat) {
        ttsCustom(lastText);
    }
});

// Saludo Inicial ######################
if (contOutput && saludoMostrado) {
    const initialMessage = `<div class="chat_msg asistent_response" data-tokeid="initialMessage"><span>¡Hola! Soy Hawky 👋😁, tu asistente virtual de la Universidad Tecnológica de Coahuila. Puedes preguntarme sobre trámites, carreras, costos u otros temas de la universidad. ¿En qué puedo ayudarte? 🫡🤘😋</span></div>`;

    contOutput.insertAdjacentHTML("beforeend", initialMessage);
    const elementInitMsg = document.querySelector(`.asistent_response[data-tokeid="initialMessage"]`);
    setTimeout(function () {
        elementInitMsg.classList.add("visible");
    }, 500);
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
