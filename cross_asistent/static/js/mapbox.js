mapboxgl.accessToken = "pk.eyJ1Ijoic2FsdmFoZHotMTEiLCJhIjoiY2x3czBoYTJiMDI1OTJqb2VmZzVueG1ocCJ9.dDJweS7MAR5N2U3SF64_Xw";

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

const edificios = {
    type: "FeatureCollection",
    features: [
        {
            type: "Feature",
            properties: {
                nombre: "Edificio 4",
                descripcion: "Descripción del Edificio 4",
                imagen_url: "/static/img/Edificio_4.webp",
                fill: "red",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93669, 25.55647],
                coordinates: [
                    [
                        [-100.93688, 25.55661],
                        [-100.93647, 25.55633],
                        [-100.93662, 25.55613],
                        [-100.93703, 25.55642],
                        [-100.93688, 25.55661],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Centro de Idiomas",
                descripcion: "Descripción del Centro de Idiomas",
                imagen_url: "/static/img/Centro_Idiomas.webp",
                fill: "red",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93705, 25.5573],
                coordinates: [
                    [
                        [-100.93684, 25.55715],
                        [-100.93724, 25.55742],
                        [-100.93711, 25.55757],
                        [-100.9367, 25.55731],
                        [-100.93684, 25.55715],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Laboratorio 7B",
                descripcion: "Descripción del Laboratorio 7B",
                imagen_url: "/static/img/Laboratorio_7B.webp",
                fill: "#00FFFF",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93626, 25.55694],
                coordinates: [
                    [
                        [-100.93644, 25.55704],
                        [-100.93631, 25.55718],
                        [-100.93593, 25.55694],
                        [-100.93606, 25.55679],
                        [-100.93644, 25.55704],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Vinculación",
                descripcion: "Descripción de Vinculación",
                imagen_url: "/static/img/Vinculacion.webp",
                fill: "yellow",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93639, 25.55773],
                coordinates: [
                    [
                        [-100.93653, 25.55813],
                        [-100.93623, 25.55794],
                        [-100.93646, 25.55765],
                        [-100.93676, 25.55785],
                        [-100.93653, 25.55813],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Rectoria",
                descripcion: "Descripcion de Rectoria",
                imagen_url: "/static/img/Rectoria.webp",
                fill: "yellow",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93601, 25.55754],
                coordinates: [
                    [
                        [-100.9359, 25.55767],
                        [-100.93559, 25.55748],
                        [-100.93581, 25.55719],
                        [-100.93612, 25.55741],
                        [-100.9359, 25.55767],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Biblioteca",
                descripcion: "Descripción de Biblioteca",
                imagen_url: "/static/img/Biblioteca.webp",
                fill: "blue",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93604, 25.55646],
                coordinates: [
                    [
                        [-100.93613, 25.55651],
                        [-100.93594, 25.55639],
                        [-100.93616, 25.55615],
                        [-100.93633, 25.55628],
                        [-100.93613, 25.55651],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Cafeteria UTC",
                descripcion: "Descripción de Cafeteria UTC",
                imagen_url: "/static/img/Cafeteria_UTC.webp",
                fill: "orange",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93606, 25.55613],
                coordinates: [
                    [
                        [-100.9361, 25.55616],
                        [-100.93618, 25.55607],
                        [-100.93608, 25.55599],
                        [-100.93601, 25.55607],
                        [-100.9361, 25.55616],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Edificio 3",
                descripcion: "Descripción de Edificio 3",
                imagen_url: "/static/img/Edificio_3.webp",
                fill: "red",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93563, 25.55596],
                coordinates: [
                    [
                        [-100.93582, 25.55611],
                        [-100.93547, 25.55583],
                        [-100.93564, 25.55566],
                        [-100.936, 25.55594],
                        [-100.93582, 25.55611],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Domo",
                descripcion: "Descripción de Domo",
                imagen_url: "/static/img/Domo.webp",
                fill: "lime",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93495, 25.5552],
                coordinates: [
                    [
                        [-100.93498, 25.55552],
                        [-100.93471, 25.55533],
                        [-100.93486, 25.55515],
                        [-100.93514, 25.55534],
                        [-100.93498, 25.55552],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Edificio Docente 2",
                descripcion:
                    "<h6>Carreras:</h6> <ul>Desarrollo y Gestion de Software Multiplataforma<br>Entornos Virtuales y Negocios Digitales<br>Diseño y Gestion de Redes Logisticas</ul> ",
                imagen_url: "/static/img/Edificio_2.webp",
                fill: "red",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93474, 25.55485],
                coordinates: [
                    [
                        [-100.93495, 25.55495],
                        [-100.93458, 25.55471],
                        [-100.93471, 25.55455],
                        [-100.93508, 25.55479],
                        [-100.93495, 25.55495],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Laboratorio 4-E",
                descripcion: "Descripción del Laboratorio 4-E",
                imagen_url: "/static/img/Laboratorio_4-E.webp",
                fill: "#00FFFF",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93471, 25.55511],
                coordinates: [
                    [
                        [-100.93468, 25.55527],
                        [-100.93479, 25.55515],
                        [-100.93462, 25.55503],
                        [-100.93451, 25.55515],
                        [-100.93468, 25.55527],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Cafeteria UTC 1",
                descripcion: "Descripción de Cafeteria UTC 1",
                imagen_url: "/static/img/cafeteria1.webp",
                fill: "orange",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93415, 25.55486],
                coordinates: [
                    [
                        [-100.93408, 25.55501],
                        [-100.9343, 25.55482],
                        [-100.93421, 25.55473],
                        [-100.93399, 25.55491],
                        [-100.93408, 25.55501],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Edificio 1",
                descripcion: "Descripción del Edificio 1",
                imagen_url: "/static/img/Edificio_1.webp",
                fill: "red",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93386, 25.55541],
                coordinates: [
                    [
                        [-100.93369, 25.55527],
                        [-100.93352, 25.55545],
                        [-100.93393, 25.55575],
                        [-100.93409, 25.55556],
                        [-100.93369, 25.55527],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Laboratorio de 7A",
                descripcion: "Descripción del Laboratorio de PLC",
                imagen_url: "/static/img/Laboratorio_7A.webp",
                fill: "#00FFFF",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93444, 25.55588],
                coordinates: [
                    [
                        [-100.93424, 25.55573],
                        [-100.93411, 25.55586],
                        [-100.93447, 25.55615],
                        [-100.93461, 25.55602],
                        [-100.93424, 25.55573],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Caceta 1",
                descripcion: "Descripción de Caceta 1",
                imagen_url: "/static/img/Caseta_1.webp",
                fill: "gray",
            },
            geometry: {
                type: "Polygon",
                door: [-100.9368, 25.55812],
                coordinates: [
                    [
                        [-100.93682, 25.55821],
                        [-100.93672, 25.55815],
                        [-100.93682, 25.55805],
                        [-100.93691, 25.55812],
                        [-100.93682, 25.55821],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Caceta 2",
                descripcion: "Descripción de Caceta 2",
                imagen_url: "/static/img/Caseta_2.webp",
                fill: "gray",
            },
            geometry: {
                type: "Polygon",
                door: [-100.9347, 25.55613],
                coordinates: [
                    [
                        [-100.93464, 25.55606],
                        [-100.93457, 25.55613],
                        [-100.9347, 25.55624],
                        [-100.93477, 25.55616],
                        [-100.93464, 25.55606],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Oxxo",
                descripcion: "Descripción de Oxxo",
                imagen_url: "/static/img/Oxxo.webp",
                fill: "white",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93613, 25.55775],
                coordinates: [
                    [
                        [-100.93619, 25.55777],
                        [-100.93613, 25.55785],
                        [-100.93602, 25.55776],
                        [-100.9361, 25.55769],
                        [-100.93619, 25.55777],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Papeleria",
                descripcion: "Descripción de Papeleria",
                imagen_url: "/static/img/papeleriautc.webp",
                fill: "blue",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93706, 25.55702],
                coordinates: [
                    [
                        [-100.93713, 25.557],
                        [-100.93709, 25.55708],
                        [-100.93701, 25.55704],
                        [-100.93706, 25.55697],
                        [-100.93713, 25.557],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Campo De Fútbol",
                descripcion: "Descripción de Campo De Fútbol",
                imagen_url: "/static/img/futbol.webp",
                fill: "lime",
            },
            geometry: {
                type: "Polygon",
                door: [-100.93778, 25.55853],
                coordinates: [
                    [
                        [-100.93793, 25.55871],
                        [-100.93763, 25.55835],
                        [-100.93786, 25.55819],
                        [-100.93816, 25.55855],
                        [-100.93793, 25.55871],
                    ],
                ],
            },
        },
        {
            type: "Feature",
            properties: {
                nombre: "Campo de Softbol",
                descripcion: "Descripción de Campo de Softbol",
                imagen_url: "/static/img/softbol.webp",
                fill: "lime",
            },
            geometry: {
                type: "Polygon",
                door: [-100.9384, 25.55849],
                coordinates: [
                    [
                        [-100.93881, 25.55886],
                        [-100.93925, 25.55844],
                        [-100.93869, 25.55796],
                        [-100.93837, 25.55848],
                        [-100.93881, 25.55886],
                    ],
                ],
            },
        },
    ],
};

// Agregar la fuente de datos y la capa al mapa
function createEdificios() {
    // Verificar si la fuente "places" ya existe
    if (!map.getSource("places")) {
        map.addSource("places", {
            type: "geojson",
            data: edificios,
        });
    }

    // Verificar si la capa "places-layer" ya existe
    if (!map.getLayer("places-layer")) {
        map.addLayer({
            id: "places-layer",
            type: "fill",
            source: "places",
            paint: {
                "fill-color": ["get", "fill"],
                "fill-opacity": 0.5,
            },
        });
    }

    // Verificar si la fuente "university-boundary" ya existe
    if (!map.getSource("university-boundary")) {
        map.addSource("university-boundary", {
            type: "geojson",
            data: universityBoundary,
        });
    }
    
    // Llenar los selectores con los nombres de los polígonos
    edificios.features.forEach((feature, index) => {
        const option = new Option(feature.properties.nombre, index);
        document.getElementById("origen").add(option);
        document.getElementById("destino").add(option.cloneNode(true));
    });
}

map.on("load", createEdificios);

// Mostrar información del edificio al hacer clic en el polígono
map.on("click", "places-layer", (e) => {
    const feature = e.features[0];
    const { nombre, descripcion, imagen_url } = feature.properties;
    const offcanvas = document.getElementById("infoLateral");
    document.getElementById("lateralTitle").innerText = nombre;
    document.getElementById("imagen_actual").src = imagen_url;

    const offcanvasContent = document.getElementById("offcanvasContent");
    offcanvasContent.innerHTML = `
  <div class="feature-info">
    <p>${descripcion}</p>
  </div>
`;

    // Mostrar el offcanvas
    const offcanvasElement = new bootstrap.Offcanvas(offcanvas);
    offcanvasElement.show();
});


// Modificar el código que cambia el estilo del mapa
const inputs = document.querySelectorAll("#offcanvasbody input");
for (const input of inputs) {
    input.onclick = (layer) => {
        // Guardar la ruta actual antes de cambiar el estilo
        if (map.getLayer("directions-route-line")) {
            currentRoute = map.getSource("directions")._data;
        }

        layerId = layer.target.id;
        map.setStyle("mapbox://styles/mapbox/" + layerId);
    };
}

// Escuchar el evento style.load y llamar a createEdificios
map.on("style.load", () => {
    createEdificios();

    // Volver a agregar la ruta si existe
    if (currentRoute) {
        map.addSource('directions', {
            type: 'geojson',
            data: currentRoute
        });

        map.addLayer({
            id: 'directions-route-line',
            type: 'line',
            source: 'directions',
            layout: {
                'line-join': 'round',
                'line-cap': 'round'
            },
            paint: {
                'line-color': '#3b9ddd',
                'line-width': 6
            }
        });
    }
});

// Inicializar la herramienta de direcciones
const directions = new MapboxDirections({
    accessToken: mapboxgl.accessToken,
    unit: "metric",
    profile: "mapbox/walking",
    controls: {
        inputs: false,
        instructions: false, // Ocultar instrucciones
        profileSwitcher: false,
    },
    interactive: false,
});

// Calcular y mostrar la ruta más corta
document.getElementById("calcularRuta").addEventListener("click", () => {
    const origenIndex = document.getElementById("origen").value;
    const destinoIndex = document.getElementById("destino").value;

    if (origenIndex && destinoIndex && origenIndex !== destinoIndex) {
        const origenCoords = edificios.features[origenIndex].geometry.door;
        const destinoCoords = edificios.features[destinoIndex].geometry.door;

        directions.setOrigin(origenCoords);
        directions.setDestination(destinoCoords);

        // Agregar la capa de la ruta al mapa
        directions.on('route', (e) => {
            currentRoute = e.route[0].geometry;
        });

        map.addControl(directions, "top-left");
    } else {
        alertSToast("center", 5000, "warning", "Por favor, llena ambos campos. 🧐😬🤔");
    }
});

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
            button.className = "mapboxgl-ctrl-icon " + className;
            button.innerHTML = innerHTML;
            button.title = title;
            button.type = "button";
            button.onclick = onClick;
            return button;
        };

        const tomaps = createButton(
            "map-location",
            '<i class="fa-solid fa-map-location-dot"></i>',
            "Google Maps",
            () => {
                window.location.href = "https://www.google.com.mx/maps";
                const url =
                    "https://www.google.com.mx/maps/dir//Universidad+Tecnol%C3%B3gica+de+Coahuila,+Boulevard+del+Parque+Industrial+Francisco+R.+Alanis,+Zona+Industrial,+Ramos+Arizpe,+Coahuila+de+Zaragoza/@25.5584689,-100.9780617,13z/data=!3m1!4b1!4m9!4m8!1m0!1m5!1m1!1s0x868814c0002295ff:0x5c622cc711957b03!2m2!1d-100.9368619!2d25.5583972!3e2?entry=ttu";
                window.open(url, "_blank");
            }
        );

        const btn3d = createButton("cube", '<i class="fa-solid fa-cube"></i>', "Recorrido Virtual", () => {
            console.log("Alerta 1 activada");
        });

        const layers = createButton("style-map", '<i class="fa-solid fa-layer-group"></i>', "Cambiar Aspecto", () => {
            const offcanvasElement = new bootstrap.Offcanvas(document.querySelector("#offcanvasBottom"));
            offcanvasElement.show();
        });

        const btnroute = createButton("location-dot", '<i class="fa-solid fa-route"></i>', "Ir a...", () => {
            document.querySelector("#controls_route").classList.toggle("show");
        });

        // Agregar botones al contenedor personalizado
        this._container.appendChild(tomaps);
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
