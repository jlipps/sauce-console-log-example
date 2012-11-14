$(function() {
    console.log("Page loaded!");

    $('#doItNau').click(doTheNaminating);
});

var doTheNaminating = function() {
    console.log("Doing the naminating");
    $.ajax({
        url: 'localhost:5050/naminatorize'
        , type: "POST"
        , data: {text: $('#names').val()}
        , success: function(res) {
            $('#naminated').html('');
            $.each(res, function(name) {
                var div = $('<div>' + name + '</div>');
                $('#naminated').appendChild(div);
            }
        }
    });
}
