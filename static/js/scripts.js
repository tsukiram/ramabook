$(document).ready(function() {
    const socket = io();

    socket.on('new_comment', function(data) {
        const newComment = `
            <div class="comment" id="comment-${data.id}">
                <div class="comment-text">
                    <strong>${data.username}</strong>: ${data.text}
                </div>
                <button class="delete-btn" data-id="${data.id}">🗑️</button>
            </div>`;
        $('#comments-list').prepend(newComment);
    });

    socket.on('delete_comment', function(data) {
        $(`#comment-${data.id}`).remove();
    });

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
