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
    const reloadModel = $("#reloadModel");
    const animationsSelect = $("#animationsSelect");
    let animationsLenght = 0;

    function loadModelAndAnimations(url) {
        modelViewer.attr("src", "_");
        setTimeout(() => {
            modelViewer.attr("src", url);
        }, 700);

        modelViewer.on("load", function () {
            const animations = modelViewer[0].availableAnimations;
            animationsSelect.empty();
            console.log("En Funcion:", animations.length);
            animationsLenght = animations.length;
            if (animations.length > 0) {
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
                        text: "No animations found",
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
        });
    }

    $("#fileInput").on("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            loadModelAndAnimations(url);
        }
    });

    reloadModel.on("click", function () {
        const url = $.trim(reloadModel.data("model"));
        if (url) {
            loadModelAndAnimations(url);
        }
    });

    setTimeout(() => {
        reloadModel.click();
    }, 500);

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
    $("#modelAreas").on("change", function () {
        if ($(this).is(":checked")) {
            $("#num_areas").on("input", function () {
                const numAreas = parseInt($(this).val(), 10);
                const modelAreasContainer = $("#model_areas");
                modelAreasContainer.empty();
                for (let i = 1; i <= numAreas; i++) {
                    modelAreasContainer.append(
                        `<button type="button" class="item d-flex justify-content-center align-items-center fs-20 item${i}">${i}</button>`
                    );
                }
            });
        }
    });

    $("#row_areas, #column_areas").on("input", function () {
        const rows = $("#row_areas").val();
        const columns = $("#column_areas").val();

        $("#model_areas").css({
            "--grid-row": rows,
            "--grid-column": columns,
        });
    });
});
