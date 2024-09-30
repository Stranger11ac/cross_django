$(document).ready(function () {
    const modelViewer = $("#asistent_model");
    const originalAnim = modelViewer.attr("animation-name");
    let animations;
    let columns;
    let rows;

    modelViewer.on("load", () => (animations = modelViewer[0].availableAnimations));

    // Cambiar Orbita #########################################
    const cameraHorizontalInput = $("#cameraHorizontal");
    const cameraVerticalInput = $("#cameraVertical");
    const cameraDistanceInput = $("#cameraDistance");
    function changeOrbit() {
        const valHor = cameraHorizontalInput.val();
        const valVer = cameraVerticalInput.val();
        const valDis = cameraDistanceInput.val();
        if (valHor && valVer && valDis) {
            modelViewer.attr("camera-orbit", `${valHor}deg ${valVer}deg ${valDis}m`);
        }
    }
    cameraHorizontalInput.on("input", changeOrbit);
    cameraVerticalInput.on("input", changeOrbit);
    cameraDistanceInput.on("input", changeOrbit);
    changeOrbit();

    // Pausar modelo #########################################
    const pauseAnim = $("#pauseAnim");
    let isPaused = false;
    pauseAnim.on("click", function () {
        isPaused = !isPaused;
        isPaused ? modelViewer[0].pause() : modelViewer[0].play();
        pauseAnim
            .attr("title", isPaused ? "Activar Animación" : "Pausar Animación")
            .html(isPaused ? '<i class="fa-solid fa-circle-play fs-20"></i>' : '<i class="fa-regular fa-circle-pause fs-20"></i>');
    });

    // Cargar animaciones #########################################
    const reloadModel = $("#reloadModel");
    const modelAreasContainer = $("#model_areas");
    const areasAnimations = $("#areasAnimations");
    const animationsSelect = $("#animationsSelect");
    let animationsLenght = 0;
    function loadModelAndAnimations(url) {
        modelViewer.attr("src", "/static/img/howki-final.glb");
        setTimeout(() => {
            modelViewer.attr("src", url);
        }, 100);

        modelViewer.on("load", function () {
            animationsLenght = animations.length;
            $("#num_areas").attr("max", animationsLenght);
            animationsSelect.empty();

            if (animationsLenght > 0) {
                $.each(animations, function (index, animation) {
                    animationsSelect.append(
                        $("<option>", {
                            value: animation,
                            text: animation,
                        })
                    );
                });

                if (originalAnim) {
                    $(`#animationsSelect option[value="${originalAnim}"]`).attr("selected", true);
                }
                $("#modelAreasCont").slideDown();
            } else {
                $("#modelAreasCont").slideUp();
                if (animationsLenght == 0) {
                    animationsSelect.append("<option hidden selected disabled>No hay animaciones</option>");
                }
            }

            isPaused = false;
            modelViewer[0].play();
            pauseAnim.attr("title", "Pausar Animacion").html('<i class="fa-regular fa-circle-pause fs-20"></i>');
        });
    }
    function addAnimationsAnother() {
        const animOtherSelect = $(".animationsSelect.selectList");
        animOtherSelect.empty();
        if (animationsLenght > 1) {
            animOtherSelect.append("<option hidden selected disabled>Animaciones:</option>");
            $.each(animations, function (index, animation) {
                animOtherSelect.append(
                    $("<option>", {
                        value: animation,
                        text: animation,
                    })
                );
            });
        } else {
            $("#modelAreasCont").slideUp();
            if (animationsLenght == 0) {
                animOtherSelect.append("<option hidden selected disabled>No hay animaciones</option>");
            }
        }
    }
    $("#fileInput").on("change", function (event) {
        const file = event.target.files[0];
        if (file) {
            const validExtensions = ["glb", "gltf"];
            const fileExtension = file.name.split(".").pop().toLowerCase();
            if (!validExtensions.includes(fileExtension)) {
                return alertSToast("center", 8000, "error", "Por favor proporciona un archivo tipo GLB o GLTF");
            }
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
            pauseAnim.attr("title", "Pausar Animacion").html('<i class="fa-regular fa-circle-pause fs-20"></i>');
        }
    });

    // Ejecutar Animacion con click #########################################
    function playAnimation(setAnimationName) {
        clearTimeout(window.animTimer);
        modelViewer[0].animationName = setAnimationName;
        modelViewer[0].play();
        // modelViewer[0].reset();

        window.animTimer = setTimeout(() => {
            const defaultAnimation = $("#animationsSelect").val();
            modelViewer[0].animationName = defaultAnimation;
            modelViewer[0].play();
            isPaused = false;
            pauseAnim.attr("title", "Pausar Animacion").html('<i class="fa-regular fa-circle-pause fs-20"></i>');
        }, 2000);
    }

    // Areas y animaciones #########################################
    function setAnimAreas() {
        if ($("#modelAreas").is(":checked")) {
            const numAreas = parseInt($("#num_areas").val(), 10);
            if (numAreas != null || numAreas != "" || numAreas != 0) {
                modelAreasContainer.empty();
                areasAnimations.empty();
                for (let i = 1; i <= numAreas; i++) {
                    areasAnimations.append(
                        `<div class="col-12"><fieldset class="p-2"><legend class="px-2 mb-0">Botton ${i}:</legend><select class="form-select animationsSelect selectList" data-add-action="#actionAnim${i}" name="areaAnim"><option selected hidden disabled>Animacion:</option></select><div class="row mt-4"><div class="col-4 col-md-4 mb-4 mb-md-0"><div data-mdb-input-init class="form-outline"><input type="number" id="areaTime${i}" data-anim-btn="#actionAnim${i}" name="areaTime" min="1" value="2" class="form-control text-end" /><label class="form-label" for="areaTime${i}">Duracion: (s)</label></div></div><div class="col-4 col-md-4"><div data-mdb-input-init class="form-outline"><input type="number" id="areaHeight${i}" data-anim-btn="#actionAnim${i}" name="areaHeight" min="1" max="${rows}" value="1" class="form-control text-end" /><label class="form-label" for="areaHeight${i}">Alto:</label></div></div><div class="col-4 col-md-4"><div data-mdb-input-init class="form-outline"><input type="number" id="areaWidth${i}" data-anim-btn="#actionAnim${i}" name="areaWidth" min="1" max="${columns}" value="1" class="form-control text-end" /><label class="form-label" for="areaWidth${i}">Largo:</label></div></div></div></fieldset></div>`
                    );
                    modelAreasContainer.append(
                        `<button type="button" id="actionAnim${i}" class="item visible play-anim-btn d-flex justify-content-center align-items-center fs-20" disabled>${i}</button>`
                    );
                    $("[data-mdb-input-init]").each(function () {
                        new mdb.Input(this);
                    });
                }
                $(".animationsSelect").on("change", function () {
                    const dataAction = $(this).attr("data-add-action");
                    const thisVal = $(this).val();
                    $(dataAction).attr("data-animation", thisVal).addClass("visible");
                    $(dataAction).removeAttr("disabled");
                });
                $('input[name="areaHeight"]').on("input", function () {
                    if ($("#modelAreas").is(":checked")) {
                        const numSpanH = parseInt($(this).val(), 10);
                        const idAnimBtn = $(this).attr("data-anim-btn");
                        $(idAnimBtn).removeClass(function (index, className) {
                            return (className.match(/(^|\s)grid-row_span\S+/g) || []).join(" ");
                        });

                        $(idAnimBtn).addClass(`grid-row_span-${numSpanH}`);
                    }
                });
                $('input[name="areaWidth"]').on("input", function () {
                    if ($("#modelAreas").is(":checked")) {
                        const numSpanW = parseInt($(this).val(), 10);
                        const idAnimBtn = $(this).attr("data-anim-btn");
                        $(idAnimBtn).removeClass(function (index, className) {
                            return (className.match(/(^|\s)grid-col_span\S+/g) || []).join(" ");
                        });

                        $(idAnimBtn).addClass(`grid-col_span-${numSpanW}`);
                    }
                });
                $(".play-anim-btn").click(function () {
                    let nameAnim = $(this).attr("data-animation");
                    playAnimation(nameAnim);
                });
                addAnimationsAnother();
            }
        }
    }
    function setModelGrid() {
        rows = $("#row_areas").val();
        columns = $("#col_areas").val();
        $("#model_areas").css({
            "--grid-row": rows || 3,
            "--grid-column": columns || 3,
        });
    }
    $("#num_areas").on("input", setAnimAreas);
    $("#row_areas, #col_areas").on("input", setModelGrid);

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

        setModelGrid();
        setAnimAreas();
        addAnimationsAnother();
    }, 500);
});
