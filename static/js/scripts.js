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

    $('#comment-form').on('submit', function(event) {
        event.preventDefault();
        const formData = $(this).serialize();
        $.ajax({
            url: '/add_comment',
            type: 'POST',
            data: formData,
            success: function(response) {
                if (!response.error) {
                    const newComment = `
                        <div class="comment" id="comment-${response.id}">
                            <div class="comment-text">
                                <strong>${response.username}</strong>: ${response.text}
                            </div>
                            <button class="delete-btn" data-id="${response.id}">🗑️</button>
                        </div>`;
                    $('#comments-list').prepend(newComment);
                    $('input[name="username"]').val(response.username);
                    $('textarea[name="comment"]').val('');
                }
            },
            error: function(response) {
                alert(response.responseJSON.error);
            }
        });
    });
});
