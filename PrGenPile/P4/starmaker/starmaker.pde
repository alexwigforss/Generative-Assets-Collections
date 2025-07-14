float innerRadius = 40;
float outerRadius = 180;

int numSpikes = 2;
PVector[] points = new PVector[ numSpikes * 2 ];
float angle = TWO_PI / points.length;
float rot = 0.0, negrot = TWO_PI;
boolean stardir = true;

void setup()
{
  frameRate(4);
  size( 640, 480 );
  makestar();
}

void draw() {
  //background(0,0);stroke(155,100);fill(0,0);
  //rect(width/4,height/4,width/2,height/2);

  translate( width/2, height/2 );rotate(rot);
  starmath();  makestar();  drawthing();
  rotate(negrot*2);  drawthing();rotate(rot);
}

void starmath()  {
  if (stardir == true) {
  numSpikes=numSpikes+1;
  if (numSpikes > 16) {stardir = false;}
  } else if (stardir == false)  {
  numSpikes=numSpikes-1;
  if (numSpikes <= 4) {stardir = true;}
  }
  points = new PVector[ numSpikes * 2 ];
  angle = TWO_PI / points.length;

  rot = rot + 0.1;  negrot = negrot - 0.1;
  if (rot >= TWO_PI)  {  rot = 0.0;  }  
  if (negrot >= TWO_PI)  {  negrot = 0.0;  }  
}

void makestar() {
  for ( int i = 0; i < points.length; i++ ) {

    float x, y;

    if ( i % 2 == 0 ) {
      x = cos( angle * i ) * outerRadius;
      y = sin( angle * i ) * outerRadius;
    } 
    else {
      x = cos( angle * i ) * innerRadius;
      y = sin( angle * i ) * innerRadius;
    }
    points[i] = new PVector( x, y );
  }
}

void drawthing() {
  beginShape();
  for (int i = 0; i < points.length; i++) {
    vertex( points[i].x, points[i].y );
  }
  endShape(CLOSE);
}

