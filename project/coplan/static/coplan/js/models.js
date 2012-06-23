var Coplan = Coplan || {};

(function($, C) {
     
     C.Plan = Backbone.Model.extend(
	 {
	     urlRoot: C.planUrlRoot,
	     sync: function(method, plan, options) {
		 // Do not try to update the created_datetime and 
		 // updated_datetime; these are going to be taken care of
		 // automatically by Django.
		 if (method == 'update') {
		     plan.unset('created_datetime');
		     plan.unset('updated_datetime');
		     delete plan.attributes['url'];
		     delete plan.attributes['id'];
		 }

		 return Backbone.sync(method, plan, options);
	     }
	 });

 })(jQuery, Coplan);


/*************************************************************************
 * On each XMLHttpRequest, set a custom X-CSRFToken header to the value of 
 * the CSRF token.  This will ensure that AJAX POST requests that are made 
 * via jQuery will not be caught by the CSRF protection.
 */
jQuery(document).ajaxSend(
    function(event, xhr, settings) {
    
	function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
			cookieValue = decodeURIComponent(
			    cookie.substring(name.length + 1));
			break;
                    }
		}
            }
            return cookieValue;
	}

	function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;

            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || 
		    url.slice(0, origin.length + 1) == origin + '/') ||
		(url == sr_origin || 
		 url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
		
	    // or any other URL that isn't scheme relative or absolute 
	    // i.e relative.
		!(/^(\/\/|http:|https:).*/.test(url));
	}

	function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}

	if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
    });
