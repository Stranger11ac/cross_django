$(document).ready(function () {
    // Pausar modelo #########################################
    const modelViewer = $("#asistent_model");
    const pauseAnim = $("#pauseAnim");
    let isPaused = false;

    pauseAnim.on("click", function () {
        isPaused = !isPaused;
        if (isPaused) {
            modelViewer[0].pause(); // Para acceder al método de un elemento DOM con jQuery, usa [0]
            pauseAnim.attr("title", "Activar Animacion");
            pauseAnim.html('<i class="fa-solid fa-person-walking fs-20"></i>');
        } else {
            modelViewer[0].play(); // Usamos [0] para acceder al método del elemento
            pauseAnim.attr("title", "Pausar Animacion");
            pauseAnim.html('<i class="fa-solid fa-universal-access fs-20"></i>');
        }
    });

    // Cargar animaciones #########################################
    const numAreas = $("#num_areas");
    const reloadModel = $("#reloadModel");
    const modelAreasContainer = $("#model_areas");
    const areasAnimations = $("#areasAnimations");
    const animationsSelect = $(".animationsSelect");
    let animationsLenght = 0;

    function loadModelAndAnimations(url) {
        modelViewer.attr("src", "_");
        setTimeout(() => {
            modelViewer.attr("src", url);
        }, 700);

        modelViewer.on("load", addAnimationsList);
    }

    function addAnimationsList() {
        const animations = modelViewer[0].availableAnimations;
        animationsLenght = animations.length;
        numAreas.attr("max", animationsLenght);

        if (animationsLenght > 0) {
            $.each(animations, function (index, animation) {
                animationsSelect.append(
                    $("<option>", {
                        value: animation,
                        text: animation,
                    })
                );
            });
        } else {
            animationsSelect.append(
                $("<option>", {
                    text: "No hay animaciones",
                })
            );
        }

        isPaused = false;
        modelViewer[0].play();
        pauseAnim.attr("title", "Pausar Animacion");
        pauseAnim.html('<i class="fa-solid fa-universal-access fs-20"></i>');

        if (animationsLenght > 1) {
            $("#modelAreasCont").slideDown();
        }
    }

    $("#fileInput").on("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            loadModelAndAnimations(url);
            animationsSelect.empty();
        }
    });

    reloadModel.on("click", function () {
        const url = $.trim(reloadModel.data("model"));
        if (url) {
            loadModelAndAnimations(url);
        }
    });

    animationsSelect.on("change", function () {
        const selectedAnimation = $(this).val();
        if (selectedAnimation) {
            modelViewer[0].animationName = selectedAnimation;
            isPaused = false;
            modelViewer[0].play();
            pauseAnim.attr("title", "Pausar Animacion");
            pauseAnim.html('<i class="fa-solid fa-universal-access fs-20"></i>');
        }
    });

    // Areas y animaciones #########################################
    if ($("#modelAreas").is(":checked")) {
        numAreas.on("input", setAreas);
    }
    $("#row_areas, #column_areas").on("input", setGrid);

    function setAreas() {
        const areasLenght = parseInt(numAreas.val(), 10);
        modelAreasContainer.empty();
        areasAnimations.empty();
        for (let i = 1; i <= areasLenght; i++) {
            modelAreasContainer.append(
                `<button type="button" class="item d-flex justify-content-center align-items-center fs-20 item${i}">${i}</button>`
            );
            areasAnimations.append(
                `<div class="col-12 col-md-6">
                    <div class="row">
                    <input type="hidden" name="areaVal" value="${i}">
                        <div class="col-2">
                            <p class="d-flex justify-content-center fs-18 m-0">${i}</p>
                        </div>
                        <div class="col">
                        <select class="form-select animationsSelect">
                            <option selected hidden disabled>Animacion:</option>
                        </select>
                        </div>
                    </div>
                </div>`
            );
            if (areasLenght > animationsLenght && animationsLenght != 1) {
                numAreas.val(animationsLenght);
                alertSToast(
                    "center",
                    7000,
                    "info",
                    "El numero de areas no puede exceder el numero de animaciones del modelo. 😯🤔😬"
                );
            }
        }

        modelViewer.on("load", addAnimationsList);
    }
    function setGrid() {
        const rows = $("#row_areas").val();
        const columns = $("#column_areas").val();

        $("#model_areas").css({
            "--grid-row": rows,
            "--grid-column": columns,
        });
    }

    // Vuelta de registro ##############
    setTimeout(() => {
        reloadModel.click();

        if ($("#modelAreas").is(":checked")) {
            var targetId = $("#modelAreas").data("btn_closed");
            $(targetId).toggleClass("show");
            if (targetId.includes("slide")) {
                $(targetId).slideToggle("slow");
            }
        }

        numAreas.val("5");
        $("#row_areas").val("2");
        $("#column_areas").val("3");
        modelViewer.on("load", function () {
            setAreas();
            setGrid();
        });
    }, 800);
});
