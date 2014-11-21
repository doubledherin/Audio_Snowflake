// DECLARATIONS
ArrayList<Hypotrochoid> hypotrochoids ;
Pattern hypotrochoid;
Hypotrochoid[] hypotrochoids = new Hypotrochoid[5]; 

// FUNCTION CALLS
void setup() {
  hypotrochoids = new ArrayList<Hypotrochoid>();
  size(document.documentElement.clientWidth, document.documentElement.clientHeight);
  width = min(width, height) - 50
  size(width, width)
  translate(width/2.0, width/2.0) 
  frameRate(100);
  ellipseMode(CENTER);
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  smooth();
}

void draw() {
  for (int i = 0; i < hypotrochoids.size(); i++) {
      Hypotrochoid h = hypotrochoids.get(i);
      h.draw();
  }
}

void setUpHypotrochoid(float a, float b, float h, float hue, float saturation, float brightness, float transparency) {
  Hypotrochoid hypotrochoid = new Hypotrochoid(a, b, h, hue, saturation, brightness, transparency);
  hypotrochoids.add(hypotrochoid);
}



// CLASS AND METHOD DEFINITIONS
interface Pattern {  
  void draw();
}


class Hypotrochoid implements Pattern {
  float a, b, h, hue, saturation, brightness, transparency;
  float t = 10.0;
  Hypotrochoid(float a, float b, float h, float hue, float saturation, float brightness, float transparency) {
    this.a = a;
    this.b = b;
    this.h = h;
    this.hue = hue;
    this.saturation = saturation;
    this.brightness = brightness; 
    this.transparency = transparency;
  };
  void draw() {
    stroke(hue, saturation, brightness, transparency);
    float x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t));//+1200;  
    float y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t));//+1000;
    scale(.5);
    ellipse(x ,y,1,1);
    scale(2);
    t += 0.01;
  };
}