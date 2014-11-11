Pattern hypotrochoid;

int[] h_values = {19, 140, 175, 50, 
90};

Hypotrochoid[] hypotrochoids = new Hypotrochoid[h_values.length];

void setup() {

  size(window.innerWidth, window.innerHeight); 
  frameRate(100);
  background(0);
  smooth();
  float a = 640.0;
  float b = 260.0;
  float t = 45.0;
//  int h = 258;
  
  for (int i = 0; i < h_values.length; i++) {
    hypotrochoids[i] = new Hypotrochoid(a, b, t, h_values[i]);
//  print(h_values[i]);  
  }
}
void draw() {  
  for (int i = 0; i < hypotrochoids.length; i++) {
    hypotrochoids[i].draw();
  }
}


interface Pattern {
  void draw();
}

class Hypotrochoid implements Pattern
{
  float a, b, h;
  float t;
  Hypotrochoid(float a, float b, float t, int h) {

    this.a = a;
    this.b = b;
    this.h = h;
    this.t = t;
  };

  void draw() {
          stroke(#F5E69C, 100);
      float x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
      float y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
      ellipse(x,y,1,1);
      t += 0.1;
//      print("!a", a, "b", b, "t", t, "h", h, "x", x, "y", y);
  };
}






