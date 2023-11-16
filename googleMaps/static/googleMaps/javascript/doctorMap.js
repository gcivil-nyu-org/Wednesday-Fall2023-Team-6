let map;
let directionsService;
let directionsRenderer;
let originMarker, destinationMarker;

function initMap() {
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 40.7167, lng: -74.0000},
        zoom: 12
    });
    directionsRenderer.setMap(map);

    let originInput = document.getElementById('origin');
    let destinationInput = document.getElementById('destination');

    let autocompleteOrigin = new google.maps.places.Autocomplete(originInput);
    let autocompleteDestination = new google.maps.places.Autocomplete(destinationInput);
}

function calculateRoute() {
    let origin = document.getElementById('origin').value;
    let destination = document.getElementById('destination').value;

    directionsService.route({
        origin: origin,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING
    }, function(response, status) {
        if (status === 'OK') {
            directionsRenderer.setDirections(response);

            // Set origin and destination markers
            const route = response.routes[0];
            setMarker(route.legs[0].start_location, 'Origin');
            setMarker(route.legs[0].end_location, 'Destination');
        } else {
            window.alert('Directions request failed due to ' + status);
        }
    });
}

function setMarker(position, title) {
    // Create a marker and set its position
    let marker = new google.maps.Marker({
        map: map,
        position: position,
        title: title
    });

    if (title === 'Origin') {
        if (originMarker) originMarker.setMap(null); // Remove previous origin marker
        originMarker = marker;
    } else {
        if (destinationMarker) destinationMarker.setMap(null); // Remove previous destination marker
        destinationMarker = marker;
    }
}

window.onload = initMap;