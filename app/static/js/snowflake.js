function jsUpdateSize(){
    // Get the dimensions of the viewport
    var width = window.innerWidth ||
                document.documentElement.clientWidth ||
                document.body.clientWidth;
    var height = window.innerHeight ||
                 document.documentElement.clientHeight ||
                 document.body.clientHeight;

};
window.onload = jsUpdateSize;       // When the page first loads
window.onresize = jsUpdateSize;     // When the browser changes size


$(document).ready(function() {

    var artist_name = $()
    $.get(
        "/get_random_patterns",
        function(data) { 
            bindDataToProcessing(data); 
        });



    $("#get_snowflake").submit(function(e) {
        e.preventDefault();
        var data = $(this).serialize();
        console.log(data);

        $.get(
            "/get_patterns",
            data,
            function(data) { 
                bindDataToProcessing(data); 
            });
    });
});

function bindDataToProcessing(data) {
    var pjs = Processing.getInstanceById('snowflake');
    console.log(data);
    var arr_from_json = JSON.parse(data);

    // console.log(pjs);

    pjs.setup();
    for (var i=0; i < arr_from_json.length; i++) {
        pattern = arr_from_json[i];
        // console.log(pattern);
        pjs.setUpHypotrochoid(pattern.a, pattern.b, pattern.h, pattern.hue, pattern.saturation, pattern.brightness, pattern.transparency);
    }
}