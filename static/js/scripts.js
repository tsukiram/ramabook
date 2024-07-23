$(document).ready(function() {
    $('.delete-btn').on('click', function() {
        const commentId = $(this).data('id');
        $.ajax({
            url: `/delete_comment/${commentId}`,
            type: 'POST',
            success: function(response) {
                if (response.result === 'success') {
                    $(`#comment-${commentId}`).remove();
                }
            }
        });
    });
});
