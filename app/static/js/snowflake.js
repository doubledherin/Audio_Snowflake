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
    setTimeout(function() {
        var patterns = $("#patterns").data().patterns;    
        console.log(patterns)
        bindDataToProcessing(patterns); 
    }, 1000);
});



function bindDataToProcessing(patterns) {
    var pjs = Processing.getInstanceById('snowflake');
    pjs.setup();
    for (var i=0; i < patterns.length; i++) {
        pattern = patterns[i];
        pjs.setUpHypotrochoid(pattern.a, pattern.b, pattern.h, pattern.hue, pattern.saturation, pattern.brightness, pattern.transparency);
    }
}