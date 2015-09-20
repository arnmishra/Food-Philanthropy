
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
					lon: position.coords.longitude
				};

				locationBlock.setPosition(pos);
				locationBlock.setContent("You are here!");

				map.setCenter(pos);
				return pos;
			}, function() {
				errorHappened(true, locationBlock, map.getCenter());
			});
		}
		else {
			errorHappened(false, locationBlock, map.getCenter());
		}
	}	

	function errorHappened(allowedGeolocation, marker, position) {
		marker.setPosition(position);
		if (allowedGeolocation) {
			marker.setContent("Browser didn't allow access to geolocation.");
		}
		else {
			marker.setContent("Geolocation error occurred.");
		}
	}
