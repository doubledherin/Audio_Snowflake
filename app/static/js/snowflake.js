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


// Bind Processing to JavaScript to get access to snowflake.pde script
$(document).ready(function() {
    setTimeout(function() {
        var patterns = $("#patterns").data().patterns;    
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


$( "#add_button" ).click(function(event) {
    event.preventDefault();
    var canvas = document.getElementById("snowflake");
    var song_id = $("#song_id:hidden").val();
    var artist_name = $("#artist_name:hidden").val();
    var title = $("#title:hidden").val();
    console.log(title);
    console.log(artist_name);


    // var image = convertCanvasToImage(canvas);
    // addSnowflake(image);

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
        }
    });
  });

// Converts canvas to an image
function convertCanvasToImage(canvas) {
  var image = new Image();
  image.onload = function() {
    console.log("image onload");
  }
  image.src = canvas.toDataURL('image/png');
  console.log(image);
  console.log(image.src);
  return image
}

// function addSnowflake(image) {
//   $.post(
//       "/add_snowflake",
//       {"image": image.src},
//       function (data) {
//           $("body").prepend(data);
//       }
// )};

  //   $.ajax({
  //     type: "POST",
  //     url: '/add_snowflake',
  //     data: {id: image.src}
  // })
  