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

    // Cambiar HDRI #########################################
    listHDRIs = ["rainforest_trail_1k", "symmetrical_garden_02_1k", "rogland_clear_night_1k", ""];
    currentIndex = 0;

    $("#changeScene").click(function () {
        localStorage.setItem("model_hdr", listHDRIs[currentIndex]);
        if (listHDRIs[currentIndex] == "") {
            modelViewer.attr("environment-image", "");
            modelViewer.attr("skybox-image", "");
        } else {
            modelViewer.attr("environment-image", `/media/hdri/${listHDRIs[currentIndex]}.hdr`);
            modelViewer.attr("skybox-image", `/media/hdri/${listHDRIs[currentIndex]}.hdr`);
        }
        currentIndex++;
        if (currentIndex >= listHDRIs.length) {
            currentIndex = 0;
        }
    });

    const hdrSaved = localStorage.getItem("model_hdr");
    if (hdrSaved != "") {
        modelViewer.attr("environment-image", `/media/hdri/${hdrSaved}.hdr`);
        modelViewer.attr("skybox-image", `/media/hdri/${hdrSaved}.hdr`);
    } else {
        modelViewer.attr("environment-image", "");
        modelViewer.attr("skybox-image", "");
    }

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

    // Ejecutar Animacion del boton #########################################
    function playAnimation(setAnimationName, animationTime = 2) {
        clearTimeout(window.animTimer);
        modelViewer[0].animationName = setAnimationName;
        modelViewer[0].play();

        window.animTimer = setTimeout(() => {
            const defaultAnimation = $("#animationsSelect").val();
            modelViewer[0].animationName = defaultAnimation || originalAnim;
            modelViewer[0].play();
            isPaused = false;
            pauseAnim.attr("title", "Pausar Animacion").html('<i class="fa-regular fa-circle-pause fs-20"></i>');
        }, animationTime * 1000);
    }

    // Areas y animaciones #########################################
    function setAnimAreas(setNumAreas) {
        const numAreas = parseInt(setNumAreas, 10);
        if (numAreas != null || numAreas != "" || numAreas != 0) {
            modelAreasContainer.empty();
            areasAnimations.empty();
            for (let i = 1; i <= numAreas; i++) {
                areasAnimations.append(
                    `<div class="col-12"><fieldset class="p-2" id="sectionAnim${i}"><legend class="px-2 mb-0">Boton #${i}:</legend><select class="form-select animationsSelect selectList" data-add-action="#actionAnim${i}" name="areaAnim"><option selected hidden disabled>Animacion:</option></select><div class="row mt-4"><div class="col-4 col-md-4 mb-4 mb-md-0"><div data-mdb-input-init class="form-outline"><input type="number" id="areaTime${i}" data-anim-btn="#actionAnim${i}" name="areaTime" max="10" min="1" value="2" class="form-control text-end" /><label class="form-label" for="areaTime${i}">Duracion: (s)</label></div></div><div class="col-4 col-md-4"><div data-mdb-input-init class="form-outline"><input type="number" id="areaHeight${i}" data-anim-btn="#actionAnim${i}" name="areaHeight" min="1" max="${rows}" value="1" class="form-control text-end" /><label class="form-label" for="areaHeight${i}">Alto:</label></div></div><div class="col-4 col-md-4"><div data-mdb-input-init class="form-outline"><input type="number" id="areaWidth${i}" data-anim-btn="#actionAnim${i}" name="areaWidth" min="1" max="${columns}" value="1" class="form-control text-end" /><label class="form-label" for="areaWidth${i}">Largo:</label></div></div></div></fieldset></div>`
                );
                modelAreasContainer.append(`<button type="button" id="actionAnim${i}" class="item play-anim-btn d-flex justify-content-center align-items-center fs-20" disabled>${i}</button>`);
                $("[data-mdb-input-init]").each(function () {
                    new mdb.Input(this);
                });
            }
            $(".animationsSelect").on("change", function () {
                const dataAction = $(this).attr("data-add-action");
                const thisVal = $(this).val();
                $(dataAction).attr("data-animation", thisVal);
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
                let timeAnim = $(this).attr("data-duration");
                playAnimation(nameAnim, timeAnim);
            });
            addAnimationsAnother();
        }
    }
    function setModelGrid(setRow = 3, setCol = 3) {
        rows = $("#row_areas").val();
        columns = $("#col_areas").val();
        $("#model_areas").css({
            "--grid-row": rows || setRow,
            "--grid-column": columns || setCol,
        });
    }
    $("#num_areas").on("input", function () {
        const thisNumAreas = $("#num_areas").val();
        if ($("#modelAreas").is(":checked")) {
            setAnimAreas(thisNumAreas);
        }
    });
    $("#row_areas, #col_areas").on("input", setModelGrid);

    function getModelSettings() {
        const urlSettings = modelViewer.attr("data-settings-model");
        const timerOut = 5000;
        const modelData = new FormData();
        modelData.append("idSetings", "2");

        fetch(urlSettings, {
            method: "POST",
            body: modelData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": formToken,
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success == false) {
                    alertSToast("center", timerOut, "warning", data.message);
                    return;
                }

                $("[data-range-val='#cameraHorizontal']").text(data.cameraOrbit[0]);
                $("[data-range-val='#cameraVertical']").text(data.cameraOrbit[1]);
                $("[data-range-val='#cameraDistance']").text(data.cameraOrbit[2]);

                $("#cameraHorizontal").attr("value", data.cameraOrbit[0]);
                $("#cameraVertical").attr("value", data.cameraOrbit[1]);
                $("#cameraDistance").attr("value", data.cameraOrbit[2]);

                function changeAnim() {
                    if (data.animations) {
                        const animations = data.animations;
                        for (let i = 0; i < animations[0].length; i++) {
                            const name = animations[0][i];

                            $(`#sectionAnim${i + 1} option[value="${name}"]`).attr("selected", true);
                            $(`#actionAnim${i + 1}`)
                                .removeAttr("disabled")
                                .attr({ "data-animation": name, "data-duration": animations[1][i] })
                                .addClass(`grid-row_span-${animations[2][i]} grid-col_span-${animations[3][i]}`);
                            $(`#sectionAnim${i + 1} #areaTime${i + 1}`).attr("value", animations[1][i]);
                            $(`#sectionAnim${i + 1} #areaHeight${i + 1}`).attr("value", animations[2][i]);
                            $(`#sectionAnim${i + 1} #areaWidth${i + 1}`).attr("value", animations[3][i]);
                        }
                    }
                }

                modelViewer.attr("camera-orbit", `${data.cameraOrbit[0]}deg ${data.cameraOrbit[1]}deg ${data.cameraOrbit[2]}m`);

                if (data.gridAreas) {
                    $("#num_areas").attr("value", data.gridAreas[0]);
                    $("#row_areas").attr("value", data.gridAreas[1]);
                    $("#col_areas").attr("value", data.gridAreas[2]);
                    setModelGrid(data.gridAreas[1], data.gridAreas[2]);
                }

                setTimeout(() => {
                    if (data.gridAreas) {
                        setAnimAreas(data.gridAreas[0]);
                    }
                    setTimeout(() => {
                        changeAnim();
                    }, 500);
                }, 1000);
            })
            .catch((error) => {
                console.error("😥 Error inesperado:", error);
                errorMessage = error.message || "Ocurrió un error. Intente nuevamente. 😥";
                alertSToast("center", timerOut + 8000, "error", errorMessage);
            });
    }
    getModelSettings();
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
