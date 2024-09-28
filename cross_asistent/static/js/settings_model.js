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
    const modelAreasContainer = $("#model_areas");
    const areasAnimations = $("#areasAnimations");
    let animationsLenght = 0;

    function loadModelAndAnimations(url) {
        modelViewer.attr("src", "/static/img/howki-final.glb");
        setTimeout(() => {
            modelViewer.attr("src", url);
        }, 500);

        modelViewer.on("load", addAnimationsList);
    }

    function addAnimationsList() {
        const animationsSelect = $(".animationsSelect");
        const animOtherSelect = $(".animationsSelect.selectList");
        const animations = modelViewer[0].availableAnimations;
        animationsLenght = animations.length;
        $("#num_areas").attr("max", animationsLenght);
        animationsSelect.empty();

        if (animationsLenght > 1) {
            animOtherSelect.append("<option hidden selected disabled>Animaciones:</option>");
            $.each(animations, function (index, animation) {
                animationsSelect.append(
                    $("<option>", {
                        value: animation,
                        text: animation,
                    })
                );
            });

            isPaused = false;
            modelViewer[0].play();
            pauseAnim.attr("title", "Pausar Animacion");
            pauseAnim.html('<i class="fa-solid fa-universal-access fs-20"></i>');
            $("#modelAreasCont").slideDown();
        } else {
            $("#modelAreasCont").slideUp();
            if (animationsLenght == 0) {
                animationsSelect.append($("<option>", { text: "No hay animaciones", disabled: true }));
            }
        }
    }

    $("#fileInput").on("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            loadModelAndAnimations(url);
        }
    });

    reloadModel.on("click", function () {
        const url = $.trim($(this).data("model"));
        if (url) {
            loadModelAndAnimations(url);
        }
    });

    $("#animationsSelect").on("change", function () {
        const selectedAnimation = $(this).val();
        if (selectedAnimation) {
            modelViewer[0].animationName = selectedAnimation;
            isPaused = false;
            modelViewer[0].play();
            pauseAnim.attr("title", "Pausar Animacion");
            pauseAnim.html('<i class="fa-solid fa-universal-access fs-20"></i>');
        }
    });

    // Ejecutar Animacion con click #########################################
    function playAnimation(setAnimationName) {
        modelViewer[0].animationName = setAnimationName;
        modelViewer[0].play();
        setTimeout(() => {
            const defaultAnimation = $("#animationsSelect").val();
            modelViewer[0].animationName = defaultAnimation;
        }, 1500.0);
    }

    // Areas y animaciones #########################################
    $("#num_areas").on("input", function () {
        if ($("#modelAreas").is(":checked")) {
            const numAreas = parseInt($("#num_areas").val(), 10);
            modelAreasContainer.empty();
            areasAnimations.empty();

            for (let i = 1; i <= numAreas; i++) {
                areasAnimations.append(
                    `<div class="col-12 mb-3">
                        <fieldset class="p-2">
                            <legend class="px-2 mb-0">Botton ${i}:</legend>
                            <select class="form-select animationsSelect selectList" data-add-action="#actionAnim${i}">
                                <option selected hidden disabled>Animacion:</option>
                            </select>
                            <div class="row mt-4">
                                <div class="col-12 col-md-4">
                                <div data-mdb-input-init class="form-outline">
                                    <input type="number" id="areaTime" name="areaTime" min="1" value="1.8" class="form-control text-end" />
                                    <label class="form-label" for="areaTime">Duracion:(s)</label>
                                </div>
                                </div>
                                <div class="col-6 col-md-4">
                                <div data-mdb-input-init class="form-outline">
                                    <input type="number" id="areaHeight" name="areaHeight" min="1" value="1" class="form-control text-end" />
                                    <label class="form-label" for="areaHeight">Alto:</label>
                                </div>
                                </div>
                                <div class="col-6 col-md-4">
                                <div data-mdb-input-init class="form-outline">
                                    <input type="number" id="areaWidth" name="areaWidth" min="1" value="1" class="form-control text-end" />
                                    <label class="form-label" for="areaWidth">Largo:</label>
                                </div>
                                </div>
                            </div>
                        </fieldset>
                    </div>`
                );
                modelAreasContainer.append(
                    `<button type="button" id="actionAnim${i}" class="item play-anim-btn d-flex justify-content-center align-items-center fs-20">${i}</button>`
                );
            }
            addAnimationsList();
            $(".animationsSelect").on("change", function () {
                const dataAction = $(this).attr("data-add-action");
                const thisVal = $(this).val();
                $(dataAction).attr("data-animation", thisVal).addClass("visible");
            });

            $(".play-anim-btn").click(function () {
                let nameAnim = $(this).attr("data-animation");
                playAnimation(nameAnim);
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

    // Vuelta de registro #########################################
    setTimeout(() => {
        reloadModel.click();

        if ($("#modelAreas").is(":checked")) {
            var targetId = $("#modelAreas").data("btn_closed");
            $(targetId).toggleClass("show");
            if (targetId.includes("slide")) {
                $(targetId).slideToggle("slow");
            }
        }
    }, 500);
});
