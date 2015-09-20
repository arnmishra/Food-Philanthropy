
	function Map_create() {
		//Creating new google.maps.Map object (google.maps.Map(mapDiv, options))
		var mapOptions = {
			center: new google.maps.LatLng(20.68177501, -103.3514794),
			zoom: 6
		};
		var map = new google.maps.Map(document.getElementById("map"), mapOptions);

		//Creating an InfoWindow object (params = which map to put it on)
		var locationBlock = new google.maps.InfoWindow({map: map});
		
		if (navigator.geolocation) {
			//"returns" a Position object, which has a Coordinates object within it
			navigator.geolocation.getCurrentPosition(function(position) {
      			var pos = {
        			lat: position.coords.latitude,
        			lng: position.coords.longitude
      			};

      		locationBlock.setPosition(pos);
      		locationBlock.setContent('You are Here!.');
      		map.setCenter(pos);
    	}, function() {
      		handleLocationError(true, infoWindow, map.getCenter());
    	});
  		} else {
    	// Browser doesn't support Geolocation
   			 handleLocationError(false, infoWindow, map.getCenter());
  		}
	}	

	function handleLocationError(allowedGeolocation, marker, position) {
		marker.setPosition(position);
		if (allowedGeolocation) {
			marker.setContent("Browser didn't allow access to geolocation.");
		}
		else {
			marker.setContent("Geolocation error occurred.");
		}
	}
