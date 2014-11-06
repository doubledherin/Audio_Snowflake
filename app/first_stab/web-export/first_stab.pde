/* A hypotrochoid is a roulette traced by a point P 
attached to a circle of radius b rolling around the 
inside of a fixed circle of radius a, where P is a 
distance h from the center of the interior circle. 
The parametric equations for a hypotrochoid are

x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t))  
y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t))
*/

float a = 150;
float b = 110;
float t = 45;
float h = 95;

void setup() {
  size(600, 600);
  background(0);
  smooth();
}
void draw() {
  //rotate(PI/8);
  
  stroke(#F5E69C, 100);
  float x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  float y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);

  stroke(#EDAB54, 60);
  h -= 20;
  x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);
  h += 20;

  stroke(#115BF5, 100);
  h -= 60;
  x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);
  h += 60;

  stroke(#2BFA75, 100);
  h += 60;
  x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);
  h -= 60;
  
  stroke(#FF2727, 40);
  h -= 160;
  x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);
  h += 160;
 
  stroke(#272FFF, 70);
  h += 170;
  x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
  y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
  ellipse(x, y, 1, 1);
  h -= 170;
/*
    stroke(#FFFFFF, 60);
    h += 100;
    a -= 100;
    b -= 100;
    x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t)) + 300;  
    y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t)) + 300;
    line(x, y, x + 5, 5);
    h -= 100;
    b += 100;
    a += 100;  */
  t += .1;

}


