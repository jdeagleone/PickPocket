$(document).ready(function() {
    $(".article-table-row").on('mouseenter', function() {
        $(this).addClass('hovered');
    });

    $(".article-table-row").on('mouseleave', function() {
        $(this).removeClass('hovered');
    });

    $(document).on('click', function() {
        alert("it worked!");
    })
});
