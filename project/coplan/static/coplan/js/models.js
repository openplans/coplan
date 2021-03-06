var Coplan = Coplan || {};

(function($, C) {
     var getValue = function(object, prop) {
	 if (!(object && object[prop])) return null;
	 return _.isFunction(object[prop]) ? object[prop]() : object[prop];
     };
 
     Backbone.Model.prototype.url = function() {
	 var base = getValue(this, 'urlRoot') 
	     || getValue(this.collection, 'url') 
	     || urlError();
	 if (this.isNew()) return base;

	 return base + (base.charAt(base.length - 1) == '/' ? '' : '/') 
	     + encodeURIComponent(this.id) + '/';
     };
     
     C.Plan = Backbone.Model.extend(
	 {
	     urlRoot: C.planUrlRoot,
	     initialize: function(attributes) {
		 var self = this;

		 this.comments = new C.PlanComments(attributes.comments || []);
		 this.comments.plan = this;
		 // The comments base URL should be relative to the plan's URL;
		 // make it so.
		 this.comments.url = function() {
		     return self.url() + 'comments/';
		 };

		 this.links = new C.PlanLinks(attributes.links || []);
		 this.links.plan = this;
		 this.links.url = function() {
		     return self.url() + 'links/';
		 };

		 this.support = new C.PlanSupports(attributes.support || []);
		 this.support.plan = this;
		 this.support.url = function() {
		     return self.url() + 'support/';
		 };

		 this.currentUserSupport = this.support.find(
		     function(support) {
			 return (support.get('supporter').id ===
				 C.currentUserId);
		     });
		 if (this.currentUserSupport === undefined) {
		     this.currentUserSupport = new C.PlanSupport({});
		     this.support.add(this.currentUserSupport);
		 }
	     },

	     sync: function(method, plan, options) {
		 if (method == 'update' || method == 'create') {
		     var data = plan.attributes;
		     options.contentType = 'application/json';

		     // Do not try to update the created_datetime and 
		     // updated_datetime; these are going to be taken care of
		     // automatically by Django.
		     delete data['created_datetime'];
		     delete data['updated_datetime'];

		     // The id and url will never change, at least not by
		     // any happening on the client.
		     delete data['url'];
		     delete data['id'];

		     // Comments will be added and updated individually
		     // through their own model.
		     delete data['comments'];

		     options.data = JSON.stringify(data);
		 }

		 return Backbone.sync(method, plan, options);
	     }
	 });

     C.PlanComment = Backbone.Model.extend({});
     C.PlanComments = Backbone.Collection.extend(
	 {
	     model: C.PlanComment
	 });

     C.PlanLink = Backbone.Model.extend({});
     C.PlanLinks = Backbone.Collection.extend(
         {
	     model: C.PlanLink
	 });

     C.PlanSupport = Backbone.Model.extend({});
     C.PlanSupports = Backbone.Collection.extend(
	 {
	     model: C.PlanSupport
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
