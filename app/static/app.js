$(document).ready(function() {
    var trow = $('.article-table-row');

    trow.on('mouseenter', function() {
        $(this).addClass('hovered');
        $(this).find('.list-item')
    });

    trow.on('mouseleave', function() {
        $(this).removeClass('hovered');
    });

    trow.on('click', function() {
        $(this).toggleClass('selected');
    });

    $('#archive').on('click', function() {
        var articles = [];
        $('.selected').each(function() {
            articles.push($(this).children('.article-item').text()); //This won't be needed for the actual archive function. Should just be able to pass along the article id(s)
            console.log(articles);
        });
        $.ajax({
            type: 'POST',
            url: '/main/archive',
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            data: articles,
            success: alert('Articles archived successfully')
        });
    });
});
