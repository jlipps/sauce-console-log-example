$(function() {
    console.log("Page loaded!");
    $('#doItNau').click(window.doTheNaminating);
});

window.doTheNaminating = function() {
    console.log("Doing the naminating");
    $.ajax({
        url: '/naminatorize'
        , type: "POST"
        , data: {text: $('#names').val()}
        , success: function(res) {
            $('#naminated').html('');
            $('#naminated').css('font-size', '30px');
            $('#naminated').css('color', '#111');
            $.each(res, function(i, name) {
                var div = $('<div class="inator">' + name + '</div>');
                $('#naminated').append(div);
            })
        }
    });
}
