mapboxgl.accessToken = 'pk.eyJ1Ijoic2FsdmFoZHotMTEiLCJhIjoiY2x3czBoYTJiMDI1OTJqb2VmZzVueG1ocCJ9.dDJweS7MAR5N2U3SF64_Xw';

const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [-100.93655, 25.55701],
  zoom: 16,
  maxZoom: 20,
  minZoom: 15,
  maxBounds: [
    [-100.9736, 25.5142],
    [-100.9117, 25.5735]
  ]
});

map.addControl(new mapboxgl.NavigationControl());

const universityBoundary = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {},
      geometry: {
        type: 'Polygon',
        coordinates: [
          [
            [-100.9736, 25.5142],
            [-100.9736, 25.5735],
            [-100.9736, 25.5142],
            [-100.9736, 25.5735],
          ]
        ]
      }
    }
  ]
};

const edificios = {
  type: 'FeatureCollection',
  features: [
    {
      type: 'Feature',
      properties: {
        nombre: 'Edificio 4',
        descripcion: 'Descripción del Edificio 4',
        imagen_url: 'img/Edificio_4.webp',
        fill: 'red',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93669, 25.55647],
        coordinates: [
          [
            [-100.93688, 25.55661],
            [-100.93647, 25.55633],
            [-100.93662, 25.55613],
            [-100.93703, 25.55642],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Centro de Idiomas',
        descripcion: 'Descripción del Centro de Idiomas',
        imagen_url: 'img/Centro_Idiomas.webp',
        fill: 'red',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93705, 25.55730],
        coordinates: [
          [
            [-100.93684, 25.55715],
            [-100.93724, 25.55742],
            [-100.93711, 25.55757],
            [-100.93670, 25.55731],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Laboratorio 7B',
        descripcion: 'Descripción del Laboratorio 7B',
        imagen_url: 'img/Laboratorio_7B.webp',
        fill: '#00FFFF',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93626, 25.55694],
        coordinates: [
          [
            [-100.93644, 25.55704],
            [-100.93631, 25.55718],
            [-100.93593, 25.55694],
            [-100.93606, 25.55679],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Vinculación',
        descripcion: 'Descripción de Vinculación',
        imagen_url: 'img/Vinculacion.webp',
        fill: 'yellow',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93639, 25.55773],
        coordinates: [
          [
            [-100.93653, 25.55813],
            [-100.93623, 25.55794],
            [-100.93646, 25.55765],
            [-100.93676, 25.55785],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Rectoria',
        descripcion: 'Descripcion de Rectoria',
        imagen_url: 'img/Rectoria.webp',
        fill: 'yellow',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93601, 25.55754],
        coordinates: [
          [
            [-100.93590, 25.55767],
            [-100.93559, 25.55748],
            [-100.93581, 25.55719],
            [-100.93612, 25.55741]
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Biblioteca',
        descripcion: 'Descripción de Biblioteca',
        imagen_url: 'img/Biblioteca.webp',
        fill: 'blue',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93604, 25.55646],
        coordinates: [
          [
            [-100.93613, 25.55651],
            [-100.93594, 25.55639],
            [-100.93616, 25.55615],
            [-100.93633, 25.55628],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Cafeteria UTC',
        descripcion: 'Descripción de Cafeteria UTC',
        imagen_url: 'img/Cafeteria_UTC.webp',
        fill: 'orange',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93606, 25.55613],
        coordinates: [
          [
            [-100.93610, 25.55616],
            [-100.93618, 25.55607],
            [-100.93608, 25.55599],
            [-100.93601, 25.55607],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Edificio 3',
        descripcion: 'Descripción de Edificio 3',
        imagen_url: 'img/Edificio_3.webp',
        fill: 'red',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93563, 25.55596],
        coordinates: [
          [
            [-100.93582, 25.55611],
            [-100.93547, 25.55583],
            [-100.93564, 25.55566],
            [-100.93600, 25.55594],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Domo',
        descripcion: 'Descripción de Domo',
        imagen_url: 'img/Domo.webp',
        fill: 'lime',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93495, 25.55520],
        coordinates: [
          [
            [-100.93498, 25.55552],
            [-100.93471, 25.55533],
            [-100.93486, 25.55515],
            [-100.93514, 25.55534],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Edificio Docente 2',
        descripcion: 'Tecnologias de la Informacion y Comunicacion',
        imagen_url: 'img/Edificio_2.webp',
        fill: 'red',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93474, 25.55485],
        coordinates: [
          [
            [-100.93495, 25.55495],
            [-100.93458, 25.55471],
            [-100.93471, 25.55455],
            [-100.93508, 25.55479],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Laboratorio 4-E',
        descripcion: 'Descripción del Laboratorio 4-E',
        imagen_url: 'img/Laboratorio_4-E.webp',
        fill: '#00FFFF',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93471, 25.55511],
        coordinates: [
          [
            [-100.93468, 25.55527],
            [-100.93479, 25.55515],
            [-100.93462, 25.55503],
            [-100.93451, 25.55515],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Cafeteria UTC 1',
        descripcion: 'Descripción de Cafeteria UTC 1',
        imagen_url: 'img/cafeteria1.webp',
        fill: 'orange',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93419, 25.55492],
        coordinates: [
          [
            [-100.93408, 25.55501],
            [-100.93430, 25.55482],
            [-100.93421, 25.55473],
            [-100.93399, 25.55491],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Edificio 1',
        descripcion: 'Descripción del Edificio 1',
        imagen_url: 'img/Edificio_1.webp',
        fill: 'red',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93386, 25.55541],
        coordinates: [
          [
            [-100.93369, 25.55527],
            [-100.93352, 25.55545],
            [-100.93393, 25.55575],
            [-100.93409, 25.55556],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Laboratorio de 7A',
        descripcion: 'Descripción del Laboratorio de PLC',
        imagen_url: 'img/Laboratorio_7A.webp',
        fill: '#00FFFF',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93444, 25.55588],
        coordinates: [
          [
            [-100.93424, 25.55573],
            [-100.93411, 25.55586],
            [-100.93447, 25.55615],
            [-100.93461, 25.55602],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Caceta 1',
        descripcion: 'Descripción de Caceta 1',
        imagen_url: 'img/Caseta_1.webp',
        fill: 'gray',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93680, 25.55812],
        coordinates: [
          [
            [-100.93682, 25.55821],
            [-100.93672, 25.55815],
            [-100.93682, 25.55805],
            [-100.93691, 25.55812],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Caceta 2',
        descripcion: 'Descripción de Caceta 2',
        imagen_url: 'img/Caseta_2.webp',
        fill: 'gray',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93470, 25.55613],
        coordinates: [
          [
            [-100.93464, 25.55606],
            [-100.93457, 25.55613],
            [-100.93470, 25.55624],
            [-100.93477, 25.55616],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Oxxo',
        descripcion: 'Descripción de Oxxo',
        imagen_url: 'img/Oxxo.webp',
        fill: 'white',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93613, 25.55775],
        coordinates: [
          [
            [-100.93619, 25.55777],
            [-100.93613, 25.55785],
            [-100.93602, 25.55776],
            [-100.93610, 25.55769],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Papeleria',
        descripcion: 'Descripción de Papeleria',
        imagen_url: 'img/papeleriautc.webp',
        fill: 'blue',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93706, 25.55702],
        coordinates: [
          [
            [-100.93713, 25.55700],
            [-100.93709, 25.55708],
            [-100.93701, 25.55704],
            [-100.93706, 25.55697],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Campo De Fútbol',
        descripcion: 'Descripción de Campo De Fútbol',
        imagen_url: 'img/futbol.webp',
        fill: 'lime',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93778, 25.55853],
        coordinates: [
          [
            [-100.93793, 25.55871],
            [-100.93763, 25.55835],
            [-100.93786, 25.55819],
            [-100.93816, 25.55855],
          ]
        ]
      }
    },
    {
      type: 'Feature',
      properties: {
        nombre: 'Campo de Softbol',
        descripcion: 'Descripción de Campo de Softbol',
        imagen_url: 'img/softbol.webp',
        fill: 'lime',
      },
      geometry: {
        type: 'Polygon',
        door: [-100.93840, 25.55849],
        coordinates: [
          [
            [-100.93881, 25.55886],
            [-100.93925, 25.55844],
            [-100.93869, 25.55796],
            [-100.93837, 25.55848],
          ]
        ]
      }
    }
  ]
};

// Agregar la fuente de datos y la capa al mapa
map.on('load', () => {

  map.addSource('places', {
    type: 'geojson',
    data: edificios
  });

  map.addLayer({
    id: 'places-layer',
    type: 'fill',
    source: 'places',
    paint: {
      'fill-color': ['get', 'fill'],
      'fill-opacity': 0.5,
    }
  });

  // Agregar el límite de la universidad como una fuente de datos
  map.addSource('university-boundary', {
    type: 'geojson',
    data: universityBoundary
  });

  // Llenar los selectores con los nombres de los polígonos
  edificios.features.forEach((feature, index) => {
    const option = new Option(feature.properties.nombre, index);
    document.getElementById('origen').add(option);
    document.getElementById('destino').add(option.cloneNode(true));
  });
});

// Mostrar información del edificio al hacer clic en el polígono
map.on('click', 'places-layer', (e) => {
  const feature = e.features[0];
  const { nombre, descripcion, imagen_url } = feature.properties;
  const offcanvasContent = document.getElementById('offcanvasContent');
  offcanvasContent.innerHTML = `
  <div class="feature-info">
    <h5>${nombre}</h5>
    <p>${descripcion}</p>
    <img src="${imagen_url}" alt="${nombre}" style="max-width: 100%;">
  </div>
`;

  // Mostrar el offcanvas
  const offcanvasElement = new bootstrap.Offcanvas(document.getElementById('offcanvasExample'));
  offcanvasElement.show();
});

// Función para cerrar el sidebar
function closeSidebar() {
  const sidebar = document.getElementById('sidebar');
  sidebar.style.display = 'none';
}

// Inicializar la herramienta de direcciones
const directions = new MapboxDirections({
  accessToken: mapboxgl.accessToken,
  unit: 'metric',
  profile: 'mapbox/walking',
  controls: {
    inputs: false,
    instructions: false, // Ocultar instrucciones
    profileSwitcher: false
  },
  interactive: false
});

// Calcular y mostrar la ruta más corta
document.getElementById('calcularRuta').addEventListener('click', () => {
  const origenIndex = document.getElementById('origen').value;
  const destinoIndex = document.getElementById('destino').value;

  if (origenIndex && destinoIndex && origenIndex !== destinoIndex) {
    const origenCoords = edificios.features[origenIndex].geometry.door;
    const destinoCoords = edificios.features[destinoIndex].geometry.door;

    directions.setOrigin(origenCoords);
    directions.setDestination(destinoCoords);

    map.addControl(directions, 'top-left');
  } else {
    alert('Por favor selecciona un origen y un destino válidos.');
  }
});

// Crear nuevo menu de botones personalizados 
class CustomControl {
  constructor() {
    this._container = null;
  }

  onAdd(map) {
    this._container = document.createElement('div');
    this._container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group';

    const createButton = (className, innerHTML, title, onClick) => {
      const button = document.createElement('button');
      button.className = 'mapboxgl-ctrl-icon ' + className;
      button.innerHTML = innerHTML;
      button.title = title;
      button.type = 'button';
      button.onclick = onClick;
      return button;
    };

    const tomaps = createButton('map-location', '<i class="fa-solid fa-map-location-dot"></i>', 'Google Maps', () => {
      alert('Alerta 1 activada');
    });

    const btn3d = createButton('cube', '<i class="fa-solid fa-cube"></i>', 'Recorrido Virtual', () => {
      alert('Alerta 1 activada');
    });

    const btnroute = createButton('location-dot', '<i class="fa-solid fa-location-dot"></i>', 'Ir a...', () => {
      alert('Alerta 2 activada');
    });

    // Agregar botones al contenedor personalizado
    this._container.appendChild(tomaps);
    this._container.appendChild(btn3d);
    this._container.appendChild(btnroute);

    return this._container;
  }
}

const customControl = new CustomControl();
map.addControl(customControl, 'top-right');
