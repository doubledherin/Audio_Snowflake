ArrayList<Hypotrochoid> hypotrochoids ;

Pattern hypotrochoid;



// float[] a_values = {640, 300, 100, 475, 
// 490};
// float[] b_values = {260.0, 140.0, 175.0, 50.0, 
// 190.0};
// float[] h_values = {19, 140, 175, 50, 
// 90};

  
//Hypotrochoid[] hypotrochoids = new Hypotrochoid[h_values.length];
Hypotrochoid[] hypotrochoids = new Hypotrochoid[5]; //Array();

void setup() {
  hypotrochoids = new ArrayList<Hypotrochoid>();

  size(window.innerWidth, window.innerHeight); 
  frameRate(100);
  background(0);
  smooth();
  // void patternSetUp(float a, float b, float h, float hue, float sat, float bright) {

  // }
  
  // for (int i = 0; i < h_values.length; i++) {
  //   hypotrochoids[i] = new Hypotrochoid(a_values[i], b_values[i], t, h_values[i]);
  // }
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


interface Pattern {
  void draw();
}

class Hypotrochoid implements Pattern
{
  float a, b, h;
  float t = 10.0;
  Hypotrochoid(float a, float b, int h) {

    this.a = a;
    this.b = b;
    this.h = h;

  };

  void draw() {
//      translate(width/2, height/2);
//      pushMatrix();

      stroke(#F5E69C, 100);
      float x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t))+1200;  
      float y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t))+700;
      scale(.5);
      ellipse(x ,y,1,1);
      scale(2);
//      popMatrix():
//      translate(width, height);
//      rotate(PI/12);

      t += 0.01;

  };
}





