var Coplan = Coplan || {};

(function($, C) {

     C.PlanView = Backbone.View.extend(
	 {
	     el: $('#id_plan-form'),

	     initialize: function() {
		 this.commentsListView = new C.CommentsListView(
		     {collection: this.model.comments}
		 );
		 this.commentsListView.render();
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
     C.CommentsListView = Backbone.View.extend(
	 {
	     el: $('ol.comments-list'),

	     initialize: function() {
		 var comments = this.collection;
		 comments.on("reset", this.render, this);
		 comments.on("add", this.addComment, this);
	     },

	     render: function() {
		 var commentTypes = {
		     '-1': 'dislikes',
		     '0': 'has a question about',
		     '1': 'likes'
		 };
		 this.collection.forEach(
		     function (comment) {
			 var $commentEl = $('#comment-template').clone();
			 $commentEl.attr('id', 'comment-' + comment.get('id'));
			 $commentEl.find('.comment-meta a')
			     .attr('href', '#comment-' + comment.get('id'));
			 $commentEl.find('.comment-author a')
			     .html(comment.get('commenter')['name']);
			 $commentEl.find('.comment-body p').html(comment.get('text'));
			 $commentEl.find('.comment-type').html(commentTypes[comment.get('type')]);
			 $commentEl.find('time').html(comment.get('created_datetime'));
			 $commentEl.find('time').attr('datetime', comment.get('created_datetime'));
			 $commentEl.removeClass('hidden');
			 $('ol.comments-list').append($commentEl);
			 }
		 );
	     }
	 });

 })(jQuery, Coplan);
