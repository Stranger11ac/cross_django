var mapToken = "pk.eyJ1Ijoic2FsdmFoZHotMTEiLCJhIjoiY2x3czBoYTJiMDI1OTJqb2VmZzVueG1ocCJ9.dDJweS7MAR5N2U3SF64_Xw";
var mapElement = document.getElementById("map");
const savedTheme = localStorage.getItem("data-mdb-theme");
const savedLastLayerMap = localStorage.getItem("mapbox-last_layer");
const inputsLayer = document.querySelectorAll("#offcanvasbody input[type='radio']");
const labelsLayer = document.querySelectorAll("#offcanvasbody label");
const formRoute = document.querySelector("#form_route");
const selectOrigin = formRoute.querySelector("#origen");
const selectDestiny = formRoute.querySelector("#destino");
const resetRoutBtn = formRoute.querySelector("[data-reset_form]");
const delRoutBtn = formRoute.querySelector("[data-del_route]");
let colorlabels = "#000";
var currentMarker;
let currentRoute;

mapboxgl.accessToken = mapToken;

const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v12",
    center: [-100.93655, 25.55701],
    zoom: 17,
    maxZoom: 20,
    minZoom: 15,
    maxBounds: [
        [-100.9736, 25.5142],
        [-100.9117, 25.5735],
    ],
});

// Desactivar zoom con scroll para el programador ################################
// if (mapElement.classList.contains("map_editing")) {
//     map.scrollZoom.disable();
// }

// Crear nuevo menu de botones personalizados ########################################
map.addControl(new mapboxgl.NavigationControl());
class CustomControl {
    constructor() {
        this._container = null;
    }

    onAdd(map) {
        this._container = document.createElement("div");
        this._container.className = "mapboxgl-ctrl mapboxgl-ctrl-group";

        const createButton = (className, innerHTML, title, onClick) => {
            const button = document.createElement("button");
            button.className = "mapboxgl-ctrl-" + className;
            button.innerHTML = innerHTML;
            button.title = title;
            button.type = "button";
            button.onclick = onClick;
            return button;
        };

        const linkmaps = createButton(
            "gmaps",
            `<div class="mapboxgl-ctrl-icon"><i class="fa-solid fa-map-location-dot"></i></div>`,
            "Google Maps",
            () => {
                document.querySelectorAll(".offcanvas.show").forEach((openOffcanvasElement) => {
                    const openOffcanvasInstance = bootstrap.Offcanvas.getInstance(openOffcanvasElement);
                    if (openOffcanvasInstance) {
                        openOffcanvasInstance.hide();
                    }
                });
                var myModal = new mdb.Modal(document.getElementById("beforeSend"));
                myModal.show();
            }
        );

        const btn3d = createButton("virtual", '<i class="fa-solid fa-cube"></i>', "Recorrido Virtual", () => {
            console.log("Alerta 1 activada");
        });

        const layers = createButton("styles", '<i class="fa-solid fa-layer-group"></i>', "Cambiar Aspecto", () => {
            document.querySelectorAll(".offcanvas.show").forEach((openOffcanvasElement) => {
                const openOffcanvasInstance = bootstrap.Offcanvas.getInstance(openOffcanvasElement);
                if (openOffcanvasInstance) {
                    openOffcanvasInstance.hide();
                }
            });
            const offcanvasElement = new bootstrap.Offcanvas(document.querySelector("#offcanvasBottom"));
            offcanvasElement.show();
        });

        const btnroute = createButton(
            "route",
            '<div class="mapboxgl-ctrl-icon" data-btn_closed="controls_route"><i class="fa-solid fa-route"></i></div>',
            "Como ir a..."
        );

        // Agregar botones al contenedor personalizado
        this._container.appendChild(linkmaps);

        if (mapElement.classList.contains("map_user")) {
            this._container.appendChild(btn3d);
        }
        this._container.appendChild(layers);
        this._container.appendChild(btnroute);

        if (mapElement.classList.contains("map_editing")) {
            const newBuild = createButton(
                "newBuild",
                `<i class="fa-solid fa-building-flag"></i>`,
                "Crear Nuevo Edificio",
                () => {
                    initPolygonDrawing();
                    document.querySelectorAll(".offcanvas.show").forEach((openOffcanvasElement) => {
                        const openOffcanvasInstance = bootstrap.Offcanvas.getInstance(openOffcanvasElement);
                        if (openOffcanvasInstance) {
                            openOffcanvasInstance.hide();
                        }
                    });

                    const offcanvasContent = document.getElementById("offcanvasContent");
                    document.getElementById("imagen_actual").src = "/static/img/default_image.webp";
                    offcanvasContent.querySelector("#isNewEdif").checked = true;

                    const newUID = $("#muid").data("new-uid");
                    $("#muid").removeClass("active").val(newUID);
                    $("#nombreEdificio").removeClass("active").val("");
                    $("#colorEdificio").removeClass("active").val("");
                    $("#puertaCordsEdificio").removeClass("active").val("");

                    $("#esquina1").removeClass("active").val("");
                    $("#esquina2").removeClass("active").val("");
                    $("#esquina3").removeClass("active").val("");
                    $("#esquina4").removeClass("active").val("");

                    tinymce.get("textTiny").setContent("");

                    const offcanvasElement = document.querySelector("#infoLateral");
                    const offcanvasInstance =
                        bootstrap.Offcanvas.getInstance(offcanvasElement) || new bootstrap.Offcanvas(offcanvasElement);

                    if (offcanvasElement.classList.contains("show")) {
                        offcanvasInstance.hide();
                    } else {
                        offcanvasInstance.show();
                    }
                }
            );

            this._container.appendChild(newBuild);
        }

        return this._container;
    }
}

map.addControl(new CustomControl(), "top-right");

// Estilo guardado ########################################
function updateLabelsAndInputs(varLayer) {
    if (varLayer) {
        labelsLayer.forEach((label) => label.classList.remove("btn_detail", "text-white", "cursor-not"));
        inputsLayer.forEach((input) => input.removeAttribute("disabled"));

        const label = document.querySelector(`label[for='${varLayer}']`);
        label.classList.add("btn_detail", "text-white", "cursor-not");

        const input = document.querySelector(`input#${varLayer}`);
        input.setAttribute("disabled", "disabled");

        if (varLayer === "dark-v11") {
            colorlabels = "#fff";
        } else {
            colorlabels = "#000";
        }
        localStorage.setItem("mapbox-last_layer", varLayer);
    }
}

function setMapStyle(style) {
    map.setStyle("mapbox://styles/mapbox/" + style);
}

if (savedLastLayerMap) {
    updateLabelsAndInputs(savedLastLayerMap);
    setMapStyle(savedLastLayerMap);
}

// Controles de Ruta
const directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
    unit: "metric",
    profile: "mapbox/walking",
    controls: {
        inputs: false,
        instructions: false,
        profileSwitcher: false,
    },
    alternatives: true,
    interactive: false,
});

// Cargar datos ##################################################################
const url = document.querySelector("#map").getAttribute("data-mapa_edif");
fetch(url)
    .then((response) => response.json())
    .then((data) => {
        const geojsonEdificios = {
            type: "FeatureCollection",
            features: data.map((item) => ({
                type: "Feature",
                properties: {
                    muid: item.muid,
                    color: item.color,
                    imagen_url: item.imagen_url,
                    nombre: item.nombre,
                    informacion: item.informacion,
                    door: item.door_coords,
                },
                geometry: {
                    type: "Polygon",
                    coordinates: [
                        [item.polygons[0], item.polygons[1], item.polygons[2], item.polygons[3], item.polygons[0]],
                    ],
                },
            })),
        };

        function createEdificios() {
            if (!map.getSource("places")) {
                map.addSource("places", {
                    type: "geojson",
                    data: geojsonEdificios,
                });
            }

            if (!map.getLayer("places-layer")) {
                map.addLayer({
                    id: "places-layer",
                    type: "fill",
                    source: "places",
                    paint: {
                        "fill-color": ["get", "color"],
                        "fill-opacity": 0.4,
                    },
                });
            }

            // Agregar capa para las etiquetas
            if (!map.getLayer("places-label")) {
                map.addLayer({
                    id: "places-label",
                    type: "symbol",
                    source: "places",
                    layout: {
                        "text-field": ["get", "nombre"],
                        "text-size": 12,
                        "text-offset": [0, -0.6],
                        "text-anchor": "top",
                    },
                    paint: {
                        "text-color": colorlabels,
                    },
                });
                map.moveLayer("places-label");
            }

            // Crear capas para cada tipo de camino
            if (!map.getLayer("smooth-path")) {
                map.addLayer({
                    id: "smooth-path",
                    type: "line",
                    source: "places",
                    filter: ["==", ["get", "type"], "smooth_path"],
                    paint: {
                        "line-color": "green",
                        "line-width": 4,
                    },
                });
            }

            // Capa para mostrar las escaleras
            if (!map.getLayer("stairs")) {
                map.addLayer({
                    id: "stairs",
                    type: "symbol",
                    source: "places",
                    filter: ["==", ["get", "hasStairs"], true], // Mostrar solo edificios con escaleras
                    layout: {
                        "icon-image": "stairs-icon", // Imagen del ícono de escaleras
                        "icon-size": 0.5,
                        "icon-allow-overlap": true,
                    },
                    paint: {
                        "icon-color": "yellow", // Color del ícono de escaleras
                    },
                });
            }

            if (!map.getLayer("streets")) {
                map.addLayer({
                    id: "streets",
                    type: "line",
                    source: "places",
                    filter: ["==", ["get", "type"], "street"],
                    paint: {
                        "line-color": "darkgray",
                        "line-width": 4,
                    },
                });
            }
        }

        function createMarker(lngLat) {
            if (currentMarker) {
                currentMarker.remove();
            }
            let savedColor = localStorage.getItem("data-color_rgb");
            currentMarker = new mapboxgl.Marker({
                draggable: false,
                color: savedColor || "#3b71ca",
            })
                .setLngLat(lngLat)
                .addTo(map);
        }

        function calcularRuta() {
            const origen = selectOrigin.value;
            const destino = selectDestiny.value;

            if (origen && destino && origen !== destino) {
                const origenFeature = geojsonEdificios.features.find((feature) => feature.properties.nombre === origen);
                const destiFeature = geojsonEdificios.features.find((feature) => feature.properties.nombre === destino);

                if (origenFeature && destiFeature) {
                    const origenCoords = origenFeature.properties.door;
                    const destinoCoords = destiFeature.properties.door;

                    directions.setOrigin(origenCoords);
                    directions.setDestination(destinoCoords);
                    $("#buttons_route").slideDown("slow");

                    directions.on("route", (e) => {
                        const routeGeoJSON = {
                            type: "FeatureCollection",
                            features: e.route.map((r) => ({
                                type: "Feature",
                                geometry: r.geometry,
                                properties: {},
                            })),
                        };
                        currentRoute = routeGeoJSON;

                        const distance = e.route[0].distance / 1000;
                        const duration = e.route[0].duration / 60;
                        $("#route-info").html(`
                            <div class="row mb-2">
                                <div class="col-1"><i class="fa-solid fa-shoe-prints me-1"></i></div>
                                <div class="col">Distancia: <strong>${distance.toFixed(2)} km</strong></div>
                            </div>
                            <div class="row">
                                <div class="col-1"><i class="fa-solid fa-hourglass-half me-1"></i></div>
                                <div class="col">Duración: <strong>${duration.toFixed(2)} minutos aprox.</strong></div>
                            </div>`);
                        $("#route-info").slideDown();
                    });

                    setTimeout(() => {
                        $("#controls_route").removeClass("show");
                    }, 4000);

                    map.addControl(directions, "top-left");
                    map.moveLayer("places-label");
                    addRouteLayer();
                }
            } else {
                alertSToast("center", 5000, "warning", "Por favor, selecciona tanto origen como destino.");
            }
        }

        function addRouteLayer() {
            if (currentRoute && currentRoute.features && currentRoute.features.length > 0) {
                if (!map.getSource("directions")) {
                    map.addSource("directions", {
                        type: "geojson",
                        data: currentRoute,
                    });
                }

                const originFeature = currentRoute.features.find((feature) => feature.properties.id === "origin");
                const destFeature = currentRoute.features.find((feature) => feature.properties.id === "destination");

                // Agregar capa de línea de ruta
                if (!map.getLayer("directions-route-line")) {
                    map.addLayer({
                        id: "directions-route-line",
                        type: "line",
                        source: "directions",
                        layout: {
                            "line-cap": "round",
                            "line-join": "round",
                        },
                        paint: {
                            "line-color": "#2d5f99",
                            "line-width": 12,
                        },
                        filter: ["==", "$type", "LineString"],
                    });
                }

                // Agregar capa de línea de ruta
                if (!map.getLayer("directions-route-line-alt")) {
                    map.addLayer({
                        id: "directions-route-line-alt",
                        type: "line",
                        source: "directions",
                        layout: {
                            "line-cap": "round",
                            "line-join": "round",
                        },
                        paint: {
                            "line-color": "#4882c5",
                            "line-width": 6,
                        },
                        filter: ["==", "$type", "LineString"],
                    });
                }

                // Agregar capa de punto de origen
                if (!map.getLayer("directions-origin-point")) {
                    map.addLayer({
                        id: "directions-origin-point",
                        type: "circle",
                        source: "directions",
                        paint: {
                            "circle-color": "#3bb2d0",
                            "circle-radius": 20,
                        },
                        filter: ["==", ["get", "id"], "origin"],
                    });
                }

                // Agregar capa de punto de destino
                if (!map.getLayer("directions-destination-point")) {
                    map.addLayer({
                        id: "directions-destination-point",
                        type: "circle",
                        source: "directions",
                        paint: {
                            "circle-color": "#8a8bc9",
                            "circle-radius": 20,
                        },
                        filter: ["==", ["get", "id"], "destination"],
                    });
                }

                // Agregar etiqueta de punto de origen
                if (!map.getLayer("directions-origin-label")) {
                    console.log(originFeature.properties["marker-symbol"]);
                    map.addLayer({
                        id: "directions-origin-label",
                        type: "symbol",
                        source: "directions",
                        layout: {
                            "text-field": originFeature.properties["marker-symbol"],
                            "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                            "text-size": 18,
                        },
                        paint: {
                            "text-color": "#fff",
                        },
                        filter: ["==", ["get", "id"], "origin"],
                    });
                }

                // Agregar etiqueta de punto de destino
                if (!map.getLayer("directions-destination-label")) {
                    map.addLayer({
                        id: "directions-destination-label",
                        type: "symbol",
                        source: "directions",
                        layout: {
                            "text-field": destFeature.properties["marker-symbol"],
                            "text-font": ["Open Sans Bold", "Arial Unicode MS Bold"],
                            "text-size": 18,
                        },
                        paint: {
                            "text-color": "#fff",
                        },
                        filter: ["==", ["get", "id"], "destination"],
                    });
                }

                map.moveLayer("places-label");
            }
        }

        function saveRouteLayers() {
            if (map.getSource("directions")) {
                currentRoute = map.getSource("directions")._data;
            }
        }

        map.on("load", function () {
            createEdificios();
        });

        map.on("style.load", function () {
            createEdificios();
            addRouteLayer();
        });

        if (mapElement.classList.contains("map_user")) {
            map.on("contextmenu", function (e) {
                const lngLat = e.lngLat;
                createMarker(lngLat);
            });
        }

        // Abrir offcanvas: Informacion del edificio
        map.on("click", "places-layer", (e) => {
            document.querySelectorAll(".offcanvas.show").forEach((openOffcanvasElement) => {
                const openOffcanvasInstance = bootstrap.Offcanvas.getInstance(openOffcanvasElement);
                if (openOffcanvasInstance) {
                    openOffcanvasInstance.hide();
                }
            });

            const feature = e.features[0];
            const { nombre, informacion, imagen_url, color, door, muid } = feature.properties;
            const { coordinates } = feature.geometry;

            const offcanvasContent = document.getElementById("offcanvasContent");
            document.getElementById("imagen_actual").src = imagen_url;

            if (mapElement.classList.contains("map_user")) {
                document.getElementById("lateralTitle").innerText = nombre;
                offcanvasContent.innerHTML = `<div class="feature-info"><p>${informacion}</p></div>`;
            }

            if (mapElement.classList.contains("map_editing")) {
                offcanvasContent.querySelector("#isNewEdif").checked = false;

                $("#muid").addClass("active").val(muid);
                $("#nombreEdificio").addClass("active").val(nombre);
                $("#colorEdificio").addClass("active").val(color);

                const numeros = door.slice(1, -1).split(",");
                $("#puertaCordsEdificio").addClass("active").val(`${numeros[0]},${numeros[1]}`);

                $("#esquina1").addClass("active").val(coordinates[0][0]);
                $("#esquina2").addClass("active").val(coordinates[0][1]);
                $("#esquina3").addClass("active").val(coordinates[0][2]);
                $("#esquina4").addClass("active").val(coordinates[0][3]);

                tinymce.get("textTiny").setContent(informacion);
            }

            const offcanvasElement = document.getElementById("infoLateral");
            const offcanvasInstance =
                bootstrap.Offcanvas.getInstance(offcanvasElement) || new bootstrap.Offcanvas(offcanvasElement);

            offcanvasInstance.show();
        });

        // Cambiar estilo del Mapa ##########################################
        inputsLayer.forEach((input) => {
            input.addEventListener("click", function (layer) {
                const layerId = layer.target.id;
                updateLabelsAndInputs(layerId);
                saveRouteLayers();

                setMapStyle(layerId);
            });
        });

        // Obtener nombres de los edificios y ordenar alfabéticamente
        const nombresEdificios = geojsonEdificios.features.map((feature) => feature.properties.nombre).sort();
        nombresEdificios.forEach((nombre) => {
            const option = new Option(nombre, nombre);
            document.getElementById("origen").add(option);
            document.getElementById("destino").add(option.cloneNode(true));
        });

        // Ejecutar calcularRuta
        selectOrigin.addEventListener("change", function () {
            const seleccionOrigen = this.value;
            selectDestiny.querySelectorAll("option").forEach((option) => {
                if (option.value === seleccionOrigen) {
                    option.disabled = true;
                } else {
                    option.disabled = false;
                }
            });

            if (document.getElementById("destino").value) {
                calcularRuta();
            }
        });
        selectDestiny.addEventListener("change", function () {
            const seleccionDestino = this.value;
            selectOrigin.querySelectorAll("option").forEach((option) => {
                if (option.value === seleccionDestino) {
                    option.disabled = true;
                } else {
                    option.disabled = false;
                }
            });

            if (document.getElementById("origen").value) {
                calcularRuta();
            }
        });

        // Resetear ruta
        document.querySelector("[data-reset_form]").addEventListener("click", function () {
            formRoute.querySelectorAll("option").forEach((option) => {
                option.disabled = false;
            });

            // Verificar si las capas de la ruta existen y removerlas
            const routeLayers = [
                "directions-route-line",
                "directions-route-line-alt",
                "directions-route-line-casing",
                "directions-hover-point-casing",
                "directions-hover-point",
                "directions-waypoint-point-casing",
                "directions-waypoint-point",
                "directions-origin-point",
                "directions-origin-label",
                "directions-destination-point",
                "directions-destination-label",
            ];
            routeLayers.forEach((layer) => {
                if (map.getLayer(layer)) {
                    map.removeLayer(layer);
                }
            });

            // Verificar si la fuente de la ruta existe y removerla
            if (map.getSource("directions")) {
                map.removeSource("directions");
            }

            $("#buttons_route").slideUp("slow");
            $("#route-info").slideUp("slow", () => {
                $("#route-info").empty();
            });
        });
    })
    .catch((error) => {
        console.error("Error al obtener los datos del mapa:");
        console.error(error);
        alertSToast("top", 5000, "error", "Ocurrio un error inesperado. verifica la consola. #403");
    });

// Cursor segun el evento ###########################################
map.getCanvas().style.cursor = "default";
function setCursor(cursorStyle) {
    map.getCanvas().style.cursor = cursorStyle;
}

map.on("dragstart", () => setCursor("move"));
map.on("dragend", () => setCursor("default"));
map.on("mousedown", () => setCursor("pointer"));
map.on("mouseup", () => setCursor("default"));
map.on("mouseover", () => setCursor("default"));

// Cambiar Estilo con switch de tema ######################################
$("#switchTheme").on("click", function () {
    if ($("#switchTheme").is(":checked")) {
        colorlabels = "#000";
        setMapStyle("streets-v12");
        updateLabelsAndInputs("streets-v12");
    } else {
        colorlabels = "#fff";
        setMapStyle("dark-v11");
        updateLabelsAndInputs("dark-v11");
    }
});

if (mapElement.classList.contains("map_editing")) {
    // Hacer visible los campos de las esquinas
    // $("#btnPoligon").on("click", function () {
    //     $(this).hide();
    //     $("#esquinasPoligono").slideDown("slow");
    // });

    const drawPolygonButton = document.getElementById("btnPoligon");
    const coordInputs = ["esquina1", "esquina2", "esquina3", "esquina4"];
    const colors = ["red", "#3b71ca", "lime", "#d29c15"];
    let markers = [];
    let coords = [];
    let polygonLayer = null;
    let createNew = false;

    drawPolygonButton.addEventListener("click", () => {
        createNew = true;
        initPolygonDrawing();
        map.on("click", addMarker);
    });

    function addMarker(e) {
        if (coords.length < 4) {
            const color = colors[coords.length];
            const marker = new mapboxgl.Marker({ color: color, draggable: true })
                .setLngLat(e.lngLat)
                .addTo(map)
                .on("dragend", updatePolygon);

            markers.push(marker);
            coords.push(e.lngLat);

            document.getElementById(coordInputs[coords.length - 1]).classList.add("active");
            document.getElementById(coordInputs[coords.length - 1]).value = `${e.lngLat.lng}, ${e.lngLat.lat}`;
        }

        if (coords.length === 4) {
            map.off("click", addMarker);
            drawPolygon();
            drawPolygonButton.classList.add("bg_red-blue");
            drawPolygonButton.classList.remove("bg_purple-blue");
            drawPolygonButton.innerHTML = 'Borrar Poligono <i class="fa-solid fa-trash-can ms-1"></i>';
            createNew = true;
        }
    }

    function initPolygonDrawing() {
        markers.forEach((marker) => marker.remove());
        markers = [];
        coords = [];
        if (createNew) {
            drawPolygonButton.classList.remove("btn_detail", "bg_red-blue");
            drawPolygonButton.classList.add("bg_purple-blue", "text-white");
            drawPolygonButton.innerHTML = 'Borrar marcadores <i class="fa-solid fa-trash-can ms-1"></i>';
            createNew = false;
        }

        if (polygonLayer) {
            if (map.getLayer(polygonLayer.id + "_label")) {
                map.removeLayer(polygonLayer.id + "_label");
            }
            if (map.getLayer(polygonLayer.id)) {
                map.removeLayer(polygonLayer.id);
            }
            if (map.getSource(polygonLayer.id)) {
                map.removeSource(polygonLayer.id);
            }
        }

        coordInputs.forEach((id) => {
            document.getElementById(id).classList.remove("active");
            document.getElementById(id).value = "";
        });

        // createNew = true;
    }

    function drawPolygon() {
        const polygonText = document.getElementById("nombreEdificio").value || "Nuevo Lugar";
        const polygonColor = document.getElementById("colorEdificio").value || "#808080";

        const coordinates = [
            coords[0].toArray(),
            coords[1].toArray(),
            coords[2].toArray(),
            coords[3].toArray(),
            coords[0].toArray(),
        ];

        if (map.getLayer("polygon_label")) {
            map.removeLayer("polygon_label");
        }
        if (map.getLayer("polygon")) {
            map.removeLayer("polygon");
        }
        if (map.getSource("polygon")) {
            map.removeSource("polygon");
        }

        const polygonId = "polygon";

        map.addSource(polygonId, {
            type: "geojson",
            data: {
                type: "Feature",
                geometry: {
                    type: "Polygon",
                    coordinates: [coordinates],
                },
            },
        });

        map.addLayer({
            id: polygonId,
            type: "fill",
            source: polygonId,
            layout: {},
            paint: {
                "fill-color": polygonColor,
                "fill-opacity": 0.5,
            },
        });

        map.addLayer({
            id: polygonId + "_label",
            type: "symbol",
            source: polygonId,
            layout: {
                "text-field": polygonText,
                "text-size": 14,
                "text-anchor": "center",
            },
            paint: {
                "text-color": colorlabels,
            },
        });

        polygonLayer = { id: polygonId };
    }

    function updatePolygon() {
        coords = markers.map((marker) => marker.getLngLat());
        coordInputs.forEach((id, index) => {
            document.getElementById(id).value = `${coords[index].lng}, ${coords[index].lat}`;
        });

        drawPolygon();
    }
}
