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

function($) {jQuery.fn.extend({
slimScroll: function(o) {

    var ops = o;
    //do it for every element that matches selector
    this.each(function(){

    var isOverPanel, isOverBar, isDragg, queueHide, barHeight,
        divS = '<div></div>',
        minBarHeight = 30,
        wheelStep = 30,
        o = ops || {},
        cwidth = o.width || 'auto',
        cheight = o.height || '250px',
        size = o.size || '7px',
        color = o.color || '#000',
        position = o.position || 'right',
        opacity = o.opacity || .4,
        alwaysVisible = o.alwaysVisible === true;
    
        //used in event handlers and for better minification
        var me = $(this);

        //wrap content
        var wrapper = $(divS).css({
            position: 'relative',
            overflow: 'hidden',
            width: cwidth,
            height: cheight
        }).attr({ 'class': 'slimScrollDiv' });

        //update style for the div
        me.css({
            overflow: 'hidden',
            width: cwidth,
            height: cheight
        });

        //create scrollbar rail
        var rail  = $(divS).css({
            width: '15px',
            height: '100%',
            position: 'absolute',
            top: 0
        });

        //create scrollbar
        var bar = $(divS).attr({ 
            'class': 'slimScrollBar ', 
            style: 'border-radius: ' + size 
            }).css({
                background: color,
                width: size,
                position: 'absolute',
                top: 0,
                opacity: opacity,
                display: alwaysVisible ? 'block' : 'none',
                BorderRadius: size,
                MozBorderRadius: size,
                WebkitBorderRadius: size,
                zIndex: 99
        });

        //set position
        var posCss = (position == 'right') ? { right: '1px' } : { left: '1px' };
        rail.css(posCss);
        bar.css(posCss);

        //wrap it
        me.wrap(wrapper);

        //append to parent div
        me.parent().append(bar);
        me.parent().append(rail);

        //make it draggable
        bar.draggable({ 
            axis: 'y', 
            containment: 'parent',
            start: function() { isDragg = true; },
            stop: function() { isDragg = false; hideBar(); },
            drag: function(e) 
            { 
                //scroll content
                scrollContent(0, $(this).position().top, false);
            }
        });

        //on rail over
        rail.hover(function(){
            showBar();
        }, function(){
            hideBar();
        });

        //on bar over
        bar.hover(function(){
            isOverBar = true;
        }, function(){
            isOverBar = false;
        });

        //show on parent mouseover
        me.hover(function(){
            isOverPanel = true;
            showBar();
            hideBar();
        }, function(){
            isOverPanel = false;
            hideBar();
        });

        var _onWheel = function(e)
        {
            //use mouse wheel only when mouse is over
            if (!isOverPanel) { return; }

            var e = e || window.event;

            var delta = 0;
            if (e.wheelDelta) { delta = -e.wheelDelta/120; }
            if (e.detail) { delta = e.detail / 3; }

            //scroll content
            scrollContent(0, delta, true);

            //stop window scroll
            if (e.preventDefault) { e.preventDefault(); }
            e.returnValue = false;
        }

        var scrollContent = function(x, y, isWheel)
        {
            var delta = y;

            if (isWheel)
            {
                //move bar with mouse wheel
                delta = bar.position().top + y * wheelStep;

                //move bar, make sure it doesn't go out
                delta = Math.max(delta, 0);
                var maxTop = me.outerHeight() - bar.outerHeight();
                delta = Math.min(delta, maxTop);

                //scroll the scrollbar
                bar.css({ top: delta + 'px' });
            }

            //calculate actual scroll amount
            percentScroll = parseInt(bar.position().top) / (me.outerHeight() - bar.outerHeight());
            delta = percentScroll * (me[0].scrollHeight - me.outerHeight());

            //scroll content
            me.scrollTop(delta);

            //ensure bar is visible
            showBar();
        }

        var attachWheel = function()
        {
            if (window.addEventListener)
            {
                this.addEventListener('DOMMouseScroll', _onWheel, false );
                this.addEventListener('mousewheel', _onWheel, false );
            } 
            else
            {
                document.attachEvent("onmousewheel", _onWheel)
            }
        }

        //attach scroll events
        attachWheel();

        var getBarHeight = function()
        {
            //calculate scrollbar height and make sure it is not too small
            barHeight = Math.max((me.outerHeight() / me[0].scrollHeight) * me.outerHeight(), minBarHeight);
            bar.css({ height: barHeight + 'px' });
        }

        //set up initial height
        getBarHeight();

        var showBar = function()
        {
            //recalculate bar height
            getBarHeight();
            clearTimeout(queueHide);
            
            //show only when required
            if(barHeight >= me.outerHeight()) {
                return;
            }
            bar.fadeIn('fast');
        }

        var hideBar = function()
        {
            //only hide when options allow it
            if (!alwaysVisible)
            {
                queueHide = setTimeout(function(){
                    if (!isOverBar && !isDragg) { bar.fadeOut('slow'); }
                }, 1000);
            }
        }

    });
    
    //maintain chainability
    return this;
}
});


jQuery.fn.extend({
slimscroll: jQuery.fn.slimScroll
});

})(jQuery);


//invalid name call
      $('#chatlist').slimscroll({
          color: '#00f',
          size: '10px',
          width: '50px',
          height: '150px'                  
      });

function $(document).ready(function(){
alert("Hello World");
});