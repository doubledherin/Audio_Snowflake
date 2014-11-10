
    /* A hypotrochoid is a roulette traced by a point P 
    attached to a circle of radius b rolling around the 
    inside of a fixed circle of radius a, where P is a 
    distance h from the center of the interior circle. 
    The parametric equations for a hypotrochoid are

    x  =  ((a-b) * cos(t)) + (h * cos(((a-b)/b) * t))  
    y  =  ((a-b) * sin(t)) - (h * sin(((a-b)/b) * t))
    */

    float a = 640;
    float b = 260;
    float t = 45;
    float h = 258;
  

    void setup() {
          size(displayWidth, displayHeight);
          background(0);
          smooth();
    }


    void draw(){


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

      t += .1;

}


