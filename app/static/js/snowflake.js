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

// TO DO-- figure out how to get around the two window.online lines (above and below)
window.onload = function() {
    $.get(
        "/get_patterns", {"title": "Waltz #2 (XO)", "artist_name": "Elliott Smith"},
        function (data) {
            var pjs = Processing.getInstanceById('snowflake');
            // var patternValues = [{a: 640, b: 260, h: 19}, {a: 300, b: 140, h: 175}, {a: 100, b: 175, h: 175}, {a: 475, b: 50, h: 50}, {a: 490, b: 190, h: 90}];
            var arr_from_json = JSON.parse(data);

            for (var i=0; i < arr_from_json.length; i++) {
                pattern = arr_from_json[i];
                console.log(pattern);
                pjs.setUpHypotrochoid(pattern.a, pattern.b, pattern.h);
            }
        });
}

