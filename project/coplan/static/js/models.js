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
