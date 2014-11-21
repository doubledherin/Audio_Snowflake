// Get the dimensions of the viewport
function jsUpdateSize(){
    var width = window.innerWidth ||
                document.documentElement.clientWidth ||
                document.body.clientWidth;
    var height = window.innerHeight ||
                 document.documentElement.clientHeight ||
                 document.body.clientHeight;

    width = Math.min(width, height)
    height = Math.min(width, height)
    $("#snowflake").width = width;
    $("#snowflake").height = height;
    // console.log(sized, typeof sized)

};

// $("canvas").height(sized);
// $("canvas").width(sized);


// Bind Processing to JavaScript to get access to snowflake.pde script
$(document).ready(function() {
    window.onload = jsUpdateSize();       // When the page first loads
    window.onresize = jsUpdateSize();     // When the browser changes size

    setTimeout(function() {
        var patterns = $("#patterns").data().patterns;    
        bindDataToProcessing(patterns); 
    }, 1000);

});

function bindDataToProcessing(patterns) {
    $("#snowflake").width = sized;
    $("#snowflake").height = sized;
    var pjs = Processing.getInstanceById('snowflake');
    pjs.setup();
    for (var i=0; i < patterns.length; i++) {
        pattern = patterns[i];
        pjs.setUpHypotrochoid(pattern.a, pattern.b, pattern.h, pattern.hue, pattern.saturation, pattern.brightness, pattern.transparency);
    }

    console.log($("#snowflake").width(), $("#snowflake").height());
}

// Adds snapshot of current canvas state to gallery
$( "#add_button" ).click(function(event) {
    event.preventDefault();
    var canvas = document.getElementById("snowflake");
    var song_id = $("#song_id").val();
    var artist_name = $("#artist_name2").val();
    var title = $("#title").val();

    $.ajax({
        type: "POST", 
        url: "/add_snowflake",
        data: { img : canvas.toDataURL("image/png"),
                song_id : song_id,
                artist_name : artist_name,
                title: title
              },
        success: function() {
            alert("Image saved.");

        // console.log($("#snowflake").width(), $("#snowflake").height());
        }
    });
  });

// Convert canvas to an image
function convertCanvasToImage(canvas) {
  var image = new Image();
  image.src = canvas.toDataURL('image/png');
  return image
}
