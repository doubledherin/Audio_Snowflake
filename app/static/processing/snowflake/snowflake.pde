// DECLARATIONS
ArrayList<Hypotrochoid> hypotrochoids ;
Pattern hypotrochoid;
Hypotrochoid[] hypotrochoids = new Hypotrochoid[5]; 



// FUNCTION CALLS
void setup() {
  hypotrochoids = new ArrayList<Hypotrochoid>();
  size(window.innerWidth, window.innerHeight); 
  frameRate(100);
  background(0);
  scale(.5);
  smooth();
}


void draw() {
  for (int i = 0; i < hypotrochoids.size(); i++) {
      Hypotrochoid h = hypotrochoids.get(i);
      h.draw();
  }
}


void setUpHypotrochoid(float a, float b, float h) {
  Hypotrochoid hypotrochoid = new Hypotrochoid(a, b, h);
  hypotrochoids.add(hypotrochoid);
}



// CLASS AND METHOD DEFINITIONS
interface Pattern {  
  void draw();
}


class Hypotrochoid implements Pattern {
  float a, b, h;
  float t = 10.0;
  Hypotrochoid(float a, float b, int h) {
    this.a = a;
    this.b = b;
    this.h = h;
  };
  void draw() {
    stroke(#F5E69C, 100);
    float x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t))+600;  
    float y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t))+350;
    // scale(2);
    // scale(.5);
    ellipse(x ,y,1,1);
    // scale(2);
    // scale(.5);
    t += 0.01;
  };
}