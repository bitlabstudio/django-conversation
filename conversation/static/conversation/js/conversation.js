$(document).ready(function() {
    $('[data-class="conversation-link"]').click(function (e) {
        e.preventDefault();
        var link = $(this);
        $.get(link.attr('href'), function(data) {
            if (data == 'success') {
                link.parents('[data-class="conversation-link-parent"]').hide();
            }
        });
    });
});
