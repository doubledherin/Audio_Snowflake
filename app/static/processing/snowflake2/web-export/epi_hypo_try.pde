Pattern hypotrochoid;
void setup() {

  size(window.innerWidth, window.innerHeight); 
  frameRate(24);
  stroke(#003300);
  fill(#0000FF);
  int a = 150;
  int b = 120;
  float t = 45;
  int h = 15;

  hypotrochoid = new Hypotrochoid(a, b, t, h, 0, 0);
}

void draw() {
  hypotrochoid.getXY(50, 20, 15);
//  background(#FFFFEE);
  hypotrochoid.draw();
  }


interface Pattern {
  void getXY(int a, int b, int h);
  void draw();
}

class Hypotrochoid implements Pattern
{
  int a, b, h;
  float t;
  float x;
  float y;
  
  Hypotrochoid(int a, int b, float t, int h, float x, float y) {
    this.a = a;
    this.b = b;
    this.h = h;
    this.t = t;
    this.x = x;
    this.y = y;
  };

  void getXY(int a, int b, int h) {
//    x = 150.0;
//    y = 150.0;
//print("a", a, "b", b, "t", t, "h", h, "x", x, "y", y);
      x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t));  
      y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t));
      print("XXXXX", x);
      print("YYYY", y);
      t = t + 0.1;
  };

  void draw() {
    print('x',  x, "y", y);
    ellipse(x+100,y+100,10,10);
  };
}






