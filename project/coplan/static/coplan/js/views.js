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
	     el: $('#discussion'),

	     initialize: function() {
		 var comments = this.collection;
		 comments.on("reset", this.render, this);
		 comments.on("add", this.addComment, this);
	     },

	     events: {
		 'click #id_comment-submit': 'onSubmitNewComment',
		 'keyup #id_comment-text': 'onCommentTextChange',
		 'change #id_comment-text': 'onCommentTextChange'
	     },

	     onCommentTextChange: function() {
		 if ($('#id_comment-text').val().trim() === '') {
		     $('#id_comment-submit').attr('disabled', 'disabled');
		 } else {
		     $('#id_comment-submit').removeAttr('disabled');
		 }		     
	     },

	     onSubmitNewComment: function() {
		 var comments = this.collection;
		 var comment = comments.create(
		     {
			 text: $('#id_comment-text').val(),
			 type: $('#id_comment-type option:selected').val()
		     }, 

		     {
			 // Wait for success from the server; we need a full 
			 // comment instance before we render.
			 wait: true,
			 success: this.clearCommentFields
		     });
	     },

	     clearCommentFields: function() {
		 $('#id_comment-text').val('').change();
		 $('#id_comment-type option:selected').removeAttr('selected');
	     },

	     addComment: function(comment) {
		 var commentTypes = {
		     '-1': 'dislikes',
		     '0': 'has a question about',
		     '1': 'likes'
		 };

		 /* Clone the comment "template" element, and manually
		  * fill in the value.
		  * 
		  * TODO: This would be much cleaner with a js template.
		  * Underscore templates are available, but I like mustache
		  * or handlebars better.
		  */
		 var $commentEl = $('#comment-template').clone();
		 $commentEl.attr('id', 'comment-' + comment.get('id'));
		 $commentEl.find('.comment-meta a')
		     .attr('href', '#comment-' + comment.get('id'));
		 $commentEl.find('.comment-author a')
		     .html(comment.get('commenter')['name'])
		     .attr('href', comment.get('commenter')['profile_url']);
		 $commentEl.find('.comment-body p')
		     .html(comment.get('text'));
		 $commentEl.find('.comment-type')
		     .html(commentTypes[comment.get('type')]);
		 $commentEl.find('time')
		     .html(comment.get('created_datetime'));
		 $commentEl.find('time')
		     .attr('datetime', comment.get('created_datetime'));
		 $commentEl.removeClass('hidden');

		 $('ol.comments-list').append($commentEl);
	     },

	     render: function() {
		 this.collection.forEach(this.addComment);
	     }
	 });

 })(jQuery, Coplan);
