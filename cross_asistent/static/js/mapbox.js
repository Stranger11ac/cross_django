var mapToken = "pk.eyJ1Ijoic2FsdmFoZHotMTEiLCJhIjoiY2x3czBoYTJiMDI1OTJqb2VmZzVueG1ocCJ9.dDJweS7MAR5N2U3SF64_Xw";
mapboxgl.accessToken = mapToken;
var offcanvas = document.getElementById("infoLateral");
var offcanvasElement = new bootstrap.Offcanvas(offcanvas);
let colorlabels = "#000";
let currentRoute;

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

map.addControl(new mapboxgl.NavigationControl());

const universityBoundary = {
    type: "FeatureCollection",
    features: [
        {
            type: "Feature",
            properties: {},
            geometry: {
                type: "Polygon",
                coordinates: [
                    [
                        [-100.9736, 25.5142],
                        [-100.9736, 25.5735],
                        [-100.9736, 25.5142],
                        [-100.9736, 25.5735],
                        [-100.9736, 25.5142],
                    ],
                ],
            },
        },
    ],
};

// Crear nuevo menu de botones personalizados
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

        const url =
            "https://www.google.com.mx/maps/dir//Universidad+Tecnol%C3%B3gica+de+Coahuila,+Boulevard+del+Parque+Industrial+Francisco+R.+Alanis,+Zona+Industrial,+Ramos+Arizpe,+Coahuila+de+Zaragoza/@25.5584689,-100.9780617,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x868814c0002295ff:0x5c622cc711957b03!2m2!1d-100.9368619!2d25.5583972!3e2?entry=ttu";

        const linkmaps = createButton(
            "gmaps",
            `<a target="_blank" href="${url}" class="mapboxgl-ctrl-icon"><i class="fa-solid fa-map-location-dot"></i></a>`,
            "Google Maps"
        );

        const btn3d = createButton("virtual", '<i class="fa-solid fa-cube"></i>', "Recorrido Virtual", () => {
            console.log("Alerta 1 activada");
        });

        const layers = createButton("styles", '<i class="fa-solid fa-layer-group"></i>', "Cambiar Aspecto", () => {
            const offcanvasElement = new bootstrap.Offcanvas(document.querySelector("#offcanvasBottom"));
            offcanvasElement.show();
        });

        const btnroute = createButton("route", '<i class="fa-solid fa-route"></i>', "Ir a...", () => {
            document.querySelector("#controls_route").classList.toggle("show");
        });

        // Agregar botones al contenedor personalizado
        this._container.appendChild(linkmaps);
        this._container.appendChild(btn3d);
        this._container.appendChild(layers);
        this._container.appendChild(btnroute);

        return this._container;
    }
}
document.querySelector("#closeControlsRoute").addEventListener("click", function () {
    document.querySelector(".controls_route").classList.toggle("show");
});
const customControl = new CustomControl();
map.addControl(customControl, "top-right");

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

                if (!map.getSource("university-boundary")) {
                    map.addSource("university-boundary", {
                        type: "geojson",
                        data: universityBoundary,
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
                }

                // Crear marcador
                let currentMarker;
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

                    currentMarker.getElement().addEventListener("mouseenter", function () {
                        map.getCanvas().style.cursor = "pointer";
                    });

                    currentMarker.getElement().addEventListener("mouseleave", function () {
                        map.getCanvas().style.cursor = "default";
                    });
                }

                map.on("click", (e) => {
                    const lngLat = e.lngLat;
                    createMarker(lngLat);
                    console.log("Nuevo LngLat:", lngLat.lng, lngLat.lat);
                });
            }

            geojsonEdificios.features.forEach((feature, index) => {
                const option = new Option(feature.properties.nombre, index);
                document.getElementById("origen").add(option);
                document.getElementById("destino").add(option.cloneNode(true));
            });

            map.on("load", function () {
                deleteLabels();
                createEdificios();
            });

            // Mostrar información del edificio al hacer clic en el polígono
            map.on("click", "places-layer", (e) => {
                const feature = e.features[0];
                const { nombre, informacion, imagen_url } = feature.properties;
                document.getElementById("lateralTitle").innerText = nombre;
                document.getElementById("imagen_actual").src = imagen_url;

                const offcanvasContent = document.getElementById("offcanvasContent");
                offcanvasContent.innerHTML = `<div class="feature-info"><p>${informacion}</p></div>`;
                offcanvasElement.show();
            });

            // Calcular y mostrar la ruta más corta
            document.getElementById("calcularRuta").addEventListener("click", () => {
                const origenIndex = document.getElementById("origen").value;
                const destinoIndex = document.getElementById("destino").value;

                if (origenIndex && destinoIndex && origenIndex !== destinoIndex) {
                    const origenCoords = geojsonEdificios.features[origenIndex].properties.door;
                    const destinoCoords = geojsonEdificios.features[destinoIndex].properties.door;

                    directions.setOrigin(origenCoords);
                    directions.setDestination(destinoCoords);

                    // Agregar la capa de la ruta al mapa
                    directions.on("route", (e) => {
                        currentRoute = e.route[0].properties;
                    });

                    map.addControl(directions, "top-left");
                } else {
                    alertSToast("center", 5000, "warning", "Por favor, llena ambos campos. 🧐😬🤔");
                }
            });

            const inputsw = document.querySelectorAll("#offcanvasbody input[type='radio']");

            inputsw.forEach((input) => {
                input.addEventListener("click", function (layer) {
                    const layerId = layer.target.id;
                    const label = document.querySelector(`label[for='${layerId}']`);

                    document.querySelectorAll("#offcanvasbody label").forEach((label) => {
                        label.classList.remove("btn_detail", "text-white");
                    });

                    label.classList.add("btn_detail", "text-white");

                    inputsw.forEach((input) => {
                        input.removeAttribute("disabled");
                    });
                    this.setAttribute("disabled", "disabled");

                    if (layerId === "dark-v11") {
                        colorlabels = "#fff";
                    } else {
                        colorlabels = "#000";
                    }

                    map.setStyle("mapbox://styles/mapbox/" + layerId);
                });
            });

            // Escuchar el evento style.load
            map.on("style.load", () => {
                deleteLabels();
                createEdificios();

                // Volver a agregar la ruta si existe
                if (currentRoute) {
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
                            "line-width": 6,
                        },
                    });
                }
            });
        })
        .catch((error) => console.error("Error al obtener los datos del mapa:", error));
});

// Inicializar la herramienta de direcciones
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

function deleteLabels() {
    map.getStyle().layers.forEach(function (layer) {
        if (layer.type === "symbol" && layer.layout["text-field"]) {
            map.setLayoutProperty(layer.id, "visibility", "none");
        }
    });
}
