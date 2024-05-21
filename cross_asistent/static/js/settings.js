// context menu disabled ####################################
document.oncontextmenu = function () {
    return false;
};

$(document).ready(function () {
    // alertSToast('center', 8000, 'info', camera_orbit);
    // $('#asistent_model').attr('camera-orbit', camera_orbit);
    const modelViewer = $("#asistent_model");
    const camera_orbit = modelViewer.attr("camera-orbit");

    modelViewer.on("loaded", function () {
        setTimeout(function () {
            modelViewer.attr("camera-orbit", camera_orbit);
        }, 3000);
    });
});

// Template Alerta switalert ################################
function alertSToast(posittionS, timerS, iconS, titleS, didCloseS) {
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
        didClose: () => {
            didCloseS;
            // window.location.href = "https://utcrutas.000webhostapp.com/singin";
        },
    });
    Toast.fire({
        icon: iconS,
        title: titleS,
    });
}

// alertSToast('top', 8000, 'success', '<br>lo normal');
