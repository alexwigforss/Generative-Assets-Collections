/**
 * PathPShape
 *
 * A simple path using PShape
 */

// A PShape object
PShape path,pathb;
int linelength;
int maxaim =80;

  int x = 0;
  int y = 0;
  int aim;
  float a,spread;
  
void setup() {
  size(640, 360, P2D);
  linelength = 0;
  // Create the shape
  path = createShape();
  path.beginShape();
  //pathb = createShape();
  //pathb.beginShape();

  // Set fill and stroke
  path.noFill();
  path.stroke(255);
  path.strokeWeight(2);

  //pathb.noFill();
  //pathb.stroke(255);
  //pathb.strokeWeight(2);


  curveFactory();

  // The path is complete
  path.endShape();
  // pathb.endShape();
  print("Entering Main Loop");
}

void draw() {
  background(51);
  // Draw the path
  scale(1, -1);
  translate(0, -height);
  shape(path);
  println(mouseY);
  circle(mouseX, -mouseY+height, 50);
  // shape(pathb);
  fill(255);
  scale(1, 1);
  translate(0, 0);
  DrawText("Blablablabla");
  //DrawText(" " + path.getVertexCount() + " ");
}

void curveFactory(){
  while (x < width) {
    // Calculate the path
    a = random(1.1,2.9);
    aim = int(random(y,maxaim));
    //spread = random(1.0,4.0);
    spread = 2;
    print("up "+aim);

    for (; y < aim; y++) {
      path.vertex(x, pow(y, 2)/20);
      // pathb.vertex(x, pow(y, a)/40);
      x+= spread;
      y++;
    }
    a = random(1.1,2.9);
    aim = int(random(0,y));
    //spread = random(1.0,4.0);
    spread = 2;
    print("dn "+aim);

    for (; y > aim; y--) {
      path.vertex(x, pow(y, 2)/20);
      // pathb.vertex(x, pow(y, a)/40);
      // path.vertex(x, pow(y, a)/20);
      x+= spread;
      y--;
    }
  }
}
