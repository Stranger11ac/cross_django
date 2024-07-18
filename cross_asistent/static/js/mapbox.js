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
    zoom: 17,
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
const url = document.querySelector("#map").getAttribute("data-mapa_edif");
fetch(url)
    .then((response) => response.json())
    .then((data) => {
        const geojsonEdificios = {
            type: "FeatureCollection",
            features: data.map((item) => ({
                type: "Feature",
                properties: {
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

            // if (!map.getLayer("stairs")) {
            //     map.addLayer({
            //         id: "stairs",
            //         type: "line",
            //         source: "places",
            //         filter: ["==", ["get", "type"], "stairs"],
            //         paint: {
            //             "line-color": "blue",
            //             "line-width": 4,
            //         },
            //     });
            // }

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
                const origenFeature = geojsonEdificios.features.find((feature) => feature.properties.nombre === origen);
                const destinoFeature = geojsonEdificios.features.find(
                    (feature) => feature.properties.nombre === destino
                );
                const hasStairs = checkForStairsAlongRoute(e.route[0]);

                if (origenFeature && destinoFeature) {
                    const origenCoords = origenFeature.properties.door;
                    const destinoCoords = destinoFeature.properties.door;

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

                    // Cambiar color del icono de ruta según la presencia de escaleras
                    const routeIcon = document.querySelector(".mapboxgl-ctrl-route .fa-solid");
                    if (hasStairs) {
                        routeIcon.style.color = "yellow";
                    } else {
                        routeIcon.style.color = "";
                    }

                    map.addControl(directions, "top-left");
                }
            } else {
                alertSToast("center", 5000, "warning", "Por favor, selecciona tanto origen como destino.");
            }
        }

        // Función para verificar si hay escaleras a lo largo de la ruta
        function checkForStairsAlongRoute(route) {
            // Implementar lógica para verificar si hay escaleras en la ruta
            // Retornar true si hay escaleras, false si no las hay
            return false; // Placeholder, implementar según tus datos y lógica
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
                const destinationFeature = currentRoute.features.find(
                    (feature) => feature.properties.id === "destination"
                );
                const routeFeature = currentRoute.features.find((feature) => feature.geometry.type === "LineString");

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
                            "text-field": destinationFeature.properties["marker-symbol"],
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

        map.on("click", function (e) {
            const lngLat = e.lngLat;
            createMarker(lngLat);
        });

        // Abrir camvas / informacion del edificio
        map.on("click", "places-layer", (e) => {
            const feature = e.features[0];
            const { nombre, informacion, imagen_url } = feature.properties;
            document.getElementById("lateralTitle").innerText = nombre;
            document.getElementById("imagen_actual").src = imagen_url;

            const offcanvasContent = document.getElementById("offcanvasContent");
            offcanvasContent.innerHTML = `<div class="feature-info"><p>${informacion}</p></div>`;
            setTimeout(() => {
                offcanvasElement.show();
            }, 100);
        });

        // Cambiar estilo del Mapa
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

                // Guardar las capas de la ruta antes de cambiar el estilo
                saveRouteLayers();

                map.setStyle("mapbox://styles/mapbox/" + layerId);

                map.on("style.load", function () {
                    createEdificios();
                    addRouteLayer(); // Restaurar las capas de la ruta
                });
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

        // Ejecutar calcularRuta
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
        alertSToast("top", 5000, "error", "Ocurrio un error inesperado. verifica la consola. #403");
        console.error("Error al obtener los datos del mapa:");
        console.error(error);
    });

map.getCanvas().style.cursor = "default";
function setCursor(cursorStyle) {
    map.getCanvas().style.cursor = cursorStyle;
}

map.on("dragstart", () => setCursor("move"));
map.on("dragend", () => setCursor("default"));
map.on("mousedown", () => setCursor("pointer"));
map.on("mouseup", () => setCursor("default"));
map.on("mouseover", () => setCursor("default"));
