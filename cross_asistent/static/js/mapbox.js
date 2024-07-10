var mapToken = "pk.eyJ1Ijoic2FsdmFoZHotMTEiLCJhIjoiY2x3czBoYTJiMDI1OTJqb2VmZzVueG1ocCJ9.dDJweS7MAR5N2U3SF64_Xw";
const inputs = document.querySelectorAll("#offcanvasbody input[type='radio']");
const formRoute = document.querySelector("#form_route");
const selectOrigin = formRoute.querySelector("#origen");
const selectDestiny = formRoute.querySelector("#destino");
const resetRoutBtn = formRoute.querySelector("[data-reset_form]");
const delRoutBtn = formRoute.querySelector("[data-del_route]");
var offcanvas = document.getElementById("infoLateral");
var offcanvasElement = new bootstrap.Offcanvas(offcanvas);
let colorlabels = "#000";
var currentMarker;
let currentRoute;

mapboxgl.accessToken = mapToken;

const map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/streets-v12",
    center: [-100.93655, 25.55701],
    zoom: 16,
    maxZoom: 20,
    minZoom: 15,
    maxBounds: [
        [-100.9736, 25.5142],
        [-100.9117, 25.5735],
    ],
});

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
                var myModal = new mdb.Modal(document.getElementById("beforeSend"));
                myModal.show();
            }
        );

        const btn3d = createButton("virtual", '<i class="fa-solid fa-cube"></i>', "Recorrido Virtual", () => {
            console.log("Alerta 1 activada");
        });

        const layers = createButton("styles", '<i class="fa-solid fa-layer-group"></i>', "Cambiar Aspecto", () => {
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
        this._container.appendChild(btn3d);
        this._container.appendChild(layers);
        this._container.appendChild(btnroute);

        return this._container;
    }
}
const customControl = new CustomControl();
map.addControl(customControl, "top-right");

// Cargar datos ##################################################################
document.addEventListener("DOMContentLoaded", function () {
    const url = document.querySelector("#map").getAttribute("data-mapa_edif");
    fetch(url)
        .then((response) => response.json())
        .then((geojsonEdificios) => {
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

                if (!map.getLayer("stairs")) {
                    map.addLayer({
                        id: "stairs",
                        type: "line",
                        source: "places",
                        filter: ["==", ["get", "type"], "stairs"],
                        paint: {
                            "line-color": "blue",
                            "line-width": 4,
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

                currentMarker = new mapboxgl.Marker({
                    draggable: false,
                    color: "#3b71ca",
                })
                    .setLngLat(lngLat)
                    .addTo(map);
            }

            function calcularRuta() {
                const origen = selectOrigin.value;
                const destino = selectDestiny.value;

                if (origen && destino && origen !== destino) {
                    const origenFeature = geojsonEdificios.features.find(
                        (feature) => feature.properties.nombre === origen
                    );
                    const destinoFeature = geojsonEdificios.features.find(
                        (feature) => feature.properties.nombre === destino
                    );

                    if (origenFeature && destinoFeature) {
                        const origenCoords = origenFeature.properties.door;
                        const destinoCoords = destinoFeature.properties.door;

                        directions.setOrigin(origenCoords);
                        directions.setDestination(destinoCoords);
                        $("#buttons_route").slideDown("fast");

                        directions.on("route", (e) => {
                            currentRoute = e.route[0].geometry;
                        });
                        map.addControl(directions, "top-left");
                    }
                } else {
                    alertSToast("center", 5000, "warning", "Por favor, selecciona tanto origen como destino.");
                }
            }

            function resetRout() {
                formRoute.querySelectorAll("option").forEach((option) => {
                    option.disabled = false;
                });
            }

            function addRouteLayer() {
                map.addSource("directions", {
                    type: "geojson",
                    data: currentRoute,
                });

                map.addLayer({
                    id: "directions-route-line",
                    type: "line",
                    source: "directions",
                    layout: {
                        "line-join": "round",
                        "line-cap": "round",
                    },
                    paint: {
                        "line-color": "#3b9ddd",
                        "line-width": 8,
                    },
                });
                map.moveLayer("places-label");
            }

            function deleteLabels() {
                map.getStyle().layers.forEach(function (layer) {
                    if (layer.type === "symbol" && layer.layout["text-field"]) {
                        map.setLayoutProperty(layer.id, "visibility", "none");
                    }
                });
            }

            map.on("load", function () {
                deleteLabels();
                createEdificios();
            });

            map.on("style.load", function () {
                deleteLabels();
                createEdificios();
                addRouteLayer();
            });

            map.on("click", function (e) {
                const lngLat = e.lngLat;
                createMarker(lngLat);
                // console.log("Nuevo LngLat:", lngLat.lng, lngLat.lat);
            });

            map.on("click", "places-layer", (e) => {
                const feature = e.features[0];
                const { nombre, informacion, imagen_url } = feature.properties;
                document.getElementById("lateralTitle").innerText = nombre;
                document.getElementById("imagen_actual").src = imagen_url;

                const offcanvasContent = document.getElementById("offcanvasContent");
                offcanvasContent.innerHTML = `<div class="feature-info"><p>${informacion}</p></div>`;
                offcanvasElement.show();
            });

            inputs.forEach((input) => {
                input.addEventListener("click", function (layer) {
                    const layerId = layer.target.id;
                    const label = document.querySelector(`label[for='${layerId}']`);

                    document.querySelectorAll("#offcanvasbody label").forEach((label) => {
                        label.classList.remove("btn_detail", "text-white");
                    });

                    inputs.forEach((input) => {
                        input.removeAttribute("disabled");
                    });

                    label.classList.add("btn_detail", "text-white");
                    this.setAttribute("disabled", "disabled");

                    if (layerId === "dark-v11") {
                        colorlabels = "#fff";
                    } else {
                        colorlabels = "#000";
                    }
                    if (map.getLayer("directions-route-line")) {
                        currentRoute = map.getSource("directions")._data;
                    }

                    map.setStyle("mapbox://styles/mapbox/" + layerId);
                });
            });

            // Obtener nombres de los edificios y ordenar alfabéticamente
            const nombresEdificios = geojsonEdificios.features.map((feature) => feature.properties.nombre).sort();
            nombresEdificios.forEach((nombre) => {
                const option = new Option(nombre, nombre);
                document.getElementById("origen").add(option);
                document.getElementById("destino").add(option.cloneNode(true));
            });

            // Sincronizar opciones entre selectores
            selectOrigin.addEventListener("change", function () {
                const seleccionOrigen = this.value;
                selectDestiny.querySelectorAll("option").forEach((option) => {
                    if (option.value === seleccionOrigen) {
                        option.disabled = true;
                    } else {
                        option.disabled = false;
                    }
                });
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
            });

            // Ejecutar calcularRuta cuando se seleccionen opciones en ambos selectores
            selectOrigin.addEventListener("change", function () {
                if (document.getElementById("destino").value) {
                    calcularRuta();
                }
            });

            selectDestiny.addEventListener("change", function () {
                if (document.getElementById("origen").value) {
                    calcularRuta();
                }
            });

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

            resetRoutBtn.addEventListener("click", resetRout);
            delRoutBtn.addEventListener("click", function () {
                if (map.getLayer("directions-route-line")) {
                    map.removeLayer("directions-route-line");
                }
                if (directions) {
                    map.removeControl(directions);
                }
                resetRout();
                addRouteLayer();
            });
        })
        .catch((error) => console.error("Error al obtener los datos del mapa:", error));
});

map.getCanvas().style.cursor = "default";
map.on("dragstart", () => {
    map.getCanvas().style.cursor = "move";
});
map.on("dragend", () => {
    map.getCanvas().style.cursor = "default";
});
map.on("mousedown", () => {
    map.getCanvas().style.cursor = "pointer";
});
map.on("mouseup", () => {
    map.getCanvas().style.cursor = "default";
});
map.on("mouseover", () => {
    map.getCanvas().style.cursor = "default";
});
