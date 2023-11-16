let map;
let directionsService;
let directionsRenderer;
let originMarker, destinationMarker;
let destinationInfoWindow;

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    const mapDiv = document.getElementById('map');
    const lat = parseFloat(mapDiv.getAttribute('data-latitude'));
    const lng = parseFloat(mapDiv.getAttribute('data-longitude'));
    const address = mapDiv.getAttribute('data-address');

    map = new google.maps.Map(mapDiv, {
        center: {lat: lat, lng: lng},
        zoom: 20
    });
    directionsRenderer.setMap(map);

    let originInput = document.getElementById('origin');
    new google.maps.places.Autocomplete(originInput);

    // Set a marker at the destination
    const destinationPosition = {lat: parseFloat(mapDiv.getAttribute('data-latitude')), lng: parseFloat(mapDiv.getAttribute('data-longitude'))};
    setMarker(destinationPosition, 'Destination', address);
}

function calculateRoute() {
    let origin = document.getElementById('origin').value;
    const mapDiv = document.getElementById('map');
    const lat = parseFloat(mapDiv.getAttribute('data-latitude'));
    const lng = parseFloat(mapDiv.getAttribute('data-longitude'));
    let destination = {lat: lat, lng: lng};

    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING
    }, function(response, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);

            // Set the origin marker
            const route = response.routes[0];
            setMarker(route.legs[0].start_location, 'Origin');
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

function setMarker(position, title, address = null) {
    // Create a marker and set its position
    let marker = new google.maps.Marker({
        map: map,
        position: position,
        title: title
    });

    if (title === 'Destination' && address) {
        destinationInfoWindow = new google.maps.InfoWindow({
            content: address
        });

        marker.addListener('mouseover', function() {
            destinationInfoWindow.open(map, marker);
        });

        marker.addListener('mouseout', function() {
            destinationInfoWindow.close();
        });
    }

    if (title === 'Origin') {
        if (originMarker) originMarker.setMap(null); // Remove previous origin marker
        originMarker = marker;
    } else {
        // Destination marker is set once in initMap, no need to reset it here
    }
}

window.onload = initMap;