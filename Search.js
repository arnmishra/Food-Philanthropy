

 //need to input json 
//need to declare local variables that take in lat and long from saketh/arnavs file

<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDeVKkP8bFgOPMDFH8XDoUGRFMOkgYNpXI&libraries=places"></script>

var map;
var deliver;
var data;

function init() {

  var place = new google.maps.LatLng()

  map = new google.maps.Map(document.getElementById('map'), {
      center: place,
      zoom: 15
    });

  var request = {
    location: place, //value from html form
    radius: '500', //value from html form
    types: ['food pantries'], ['shelters']
  };

  deliver = new google.maps.places.PlacesService(map);

  deliver.nearbySearch(request, callback); 
}

function callback(results, status) { 
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
     	 var place = results[i];
        createMarker(results[i]);
        data = new google.maps.InfoWindow();
    }
  }
}
  
  deliver = new google.maps.places.PlacesService(map);

  map.addListener('idle', performSearch); //so we can query without throwing too much at the server
}

function performSearch() {
  var request = {
    bounds: map.getBounds(),
    keyword: 'food pantries', 'shelters' //insert keyword
  };

  deliver.radarSearch(request, callback);
};

function addMarker(place, map) {
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location,
    icon: {
      url: 'http://maps.gstatic.com/mapfiles/circle.png',
      anchor: new google.maps.Point(10, 10),
      scaledSize: new google.maps.Size(10, 17)
    }
  });

  google.maps.event.addListener(marker, 'click', function() {
    deliver.getDetails(place, function(result, status) {
      if (status !== google.maps.places.PlacesServiceStatus.OK) {
        console.error(status);
        return;
      }
      data.setContent(result.name);
      data.open(map, marker);
    });
  });
}