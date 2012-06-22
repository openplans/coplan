var Coplan = Coplan || {};

(function($, C) {

     C.PlanView = Backbone.View.extend(
	 {
	     el: $('#id_plan-form'),

	     initialize: function() {
	     },

	     events: {
		 'change #id_title': 'onFormChange',
		 'change #id_motivation': 'onFormChange',
		 'change #id_details': 'onFormChange'
	     },

	     onFormChange: function() {
		 this.model.save(
		     {
			 title: $('#id_title').val(),
			 motivation: $('#id_motivation').val(),
			 details: $('#id_details').val()
		     });
	     }
	 });

 })(jQuery, Coplan);
