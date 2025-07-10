IntList clicked;
ArrayList<PVector> Vectors = new ArrayList<PVector>();
PVector pvec = new PVector();
PVector mus = new PVector();
float a;
String Msg;
ArrayList<Dott> Dots = new ArrayList<Dott>();
ArrayList<Triangle> Tris = new ArrayList<Triangle>();

void setup() {
  size(600, 600);
  stroke(255);
  SetText();
  Msg = "Hejhej";
  handleradius = 20;
}

void draw() {
  mus = new PVector(mouseX, mouseY);
  background(175);
  for (Dott dott : Dots) {
    dott.drawDott();
    dott.update();
  }
  for (Triangle tri : Tris) {
    tri.drawTri();
  }
  fill(255);
  DrawText(Msg);
}

float distVecMouse(PVector vec) {
  float d= sqrt((vec.x-mouseX)+(vec.y-mouseY));
  return d;
}

float distVecVec(PVector v1,PVector v2) {
  float d= sqrt((v1.x-v2.x)+(v1.y-v2.y));
  print(d);
  return d;
}

void mouseMoved() {
  Msg = mouseX + " " + mouseY;
  if (Dots.size() > 0) {
    Dott d = Dots.get(Dots.size()-1);
    Msg += " " + d.pos.dist(mus);
  }
  for (int i = 0; i <Vectors.size(); i++) {
    PVector vect = Vectors.get(i);
    if (distVecMouse(vect)<5);
    continue;
  }
}
void SetText(){textAlign(CENTER, CENTER);textSize(16);}

void DrawText(String debugString){text(debugString, width/2, 20);}
int globalIndex;
int handleradius;
class Dott {
  int index;
  PVector pos;
  PVector fwd;
  Dott (int x, int y) {
    // Om tredje punkten Skapa en triangel
    // Annars skapa punkt
    index = globalIndex++;
    pos = new PVector(x, y);
    fwd = new PVector(mouseX, mouseY);
  }
  void drawDott() {
    stroke(255);
    fill(255);
    ellipse(pos.x, pos.y, 30, 30);
    stroke(0);
    line(pos.x, pos.y, pos.x+fwd.x, pos.y+fwd.y);
    fill(0);
  }
  void update() {
    if (index == Dots.size()-1) {
      // Om det är den sista punkten i listan
      // Peka mot musen
      fwd = new PVector(mouseX, mouseY);
      fwd.sub(pos);
      fwd.normalize();
      fwd.mult(pos.dist(mus));
    } else if (index < Dots.size()-1)
      // För alla andra punkter i listan
      // Peka mot nästa punkt
    {
      Dott d = Dots.get(index+1);
      fwd = new PVector(d.pos.x, d.pos.y);
      fwd.sub(pos);
    }
  }
}

class Triangle {
  Dott[] dotts = new Dott[3];
  float[] sides = new float[3];

  PVector[] mpv = new PVector[3];

  Triangle (Dott a, Dott b, Dott c) {
    dotts[0] = a;
    dotts[1] = b;
    dotts[2] = c;

    update();
  }

  void update() {
    for (int i=0; i<=2; i++) {
      if (i == 0 || i == 1) {
        mpv[i] = PVector.lerp(dotts[i].pos, dotts[i+1].pos, 0.5);
      } else {
        mpv[i] = PVector.lerp(dotts[i].pos, dotts[0].pos, 0.5);
      }
      sides[0] = dotts[0].pos.dist(dotts[1].pos);
      sides[1] = dotts[1].pos.dist(dotts[2].pos);
      sides[2] = dotts[2].pos.dist(dotts[0].pos);
      printArray(sides);
    }
  }

  void moveHandle(int who) {
    dotts[who].pos=mus;
    update();
  }

  void drawTri() {
    float[] ang = new float[2];
    fill(255);
    triangle(dotts[0].pos.x, dotts[0].pos.y, dotts[1].pos.x, dotts[1].pos.y, dotts[2].pos.x, dotts[2].pos.y);
    int i = 4;
    for (Dott d : dotts) {
      fill(255);
      circle(d.pos.x, d.pos.y, handleradius*2);
      fill(0);
      text(degreeFromSides(sides[(i-1)%3],sides[i%3],sides[(i+1)%3]), d.pos.x, d.pos.y);
      fill(255, 0, 0);
      i++;
    }
    // Print distances
    i=0;
    for (PVector mv : mpv) {
      if (i < 2)
      {
        text(sides[i], mv.x, mv.y);
        //text(dotts[i].pos.dist(dotts[i+1].pos), mv.x, mv.y);
      } else if (i == 2) {
        text(sides[i], mv.x, mv.y);
        //text(dotts[0].pos.dist(dotts[2].pos), mv.x, mv.y);
        //println();
      }
      i++;
    }
    circle(center(mpv).x, center(mpv).y, 10);
  }
  PVector center(PVector[] cvps) {
    PVector rvps = new PVector((cvps[0].x+cvps[1].x+cvps[2].x)/3, (cvps[0].y+cvps[1].y+cvps[2].y)/3);
    return rvps;
  }
  void yield() {
    //println("Jag är en triangel.");
  }
}
int[] mouseOverHandle() {
  int[] ret = new int[]{-1, -1};
  int i = 0;
  for (Triangle tri : Tris) {
    for (Dott d : tri.dotts) {
      if (d.pos.dist(mus)<handleradius) {
        ret[0] = i;
        ret[1] = d.index;
        return ret;
      }
    }
    i++;
  }
  return ret;
}
int K = 0;
int k = 0;
int[] wHandleHold = new int[2];
boolean holding = false;
void mousePressed() {
  wHandleHold = mouseOverHandle();
  if (Tris.size()>0 && wHandleHold[0] >= 0) {
    holding = true;
  } else if (Dots.size()==2) {
    // Om tre punkter skapa triangel och rensa punkter
    Dots.add(new Dott(mouseX, mouseY));
    Vectors.add(new PVector(mouseX, mouseY));

    Tris.add(new Triangle(Dots.get(0), Dots.get(1), Dots.get(2)));
    Dots.removeAll(Dots);
    globalIndex = 0;
  } else {
    // Om INTE tre punkter skapa punkt.
    Dots.add(new Dott(mouseX, mouseY));
    Vectors.add(new PVector(mouseX, mouseY));
  }
  //println(Dots.size());
}
void mouseDragged() 
{
  if (holding) {
    Triangle tri = Tris.get(wHandleHold[0]);
    tri.moveHandle(wHandleHold[1]);
  }
}
void mouseReleased() 
{
  holding = false;
}
void keyPressed() {
  if (key == '+') {
    K++;
  } else if (key == '-') {
    K--;
  }
  k=K%3;
  //println(K + " " + k);
}
float radFromSides(float a, float b, float c) {
  //float sidea = a;
  //float sideb = b;
  //float sidec = c;
  float divider = 2*a*c;
  float B = acos((pow(a,2)+pow(c,2)-pow(b,2))/divider);
  return B;
}

float degreeFromSides(float a, float b, float c) {
  //float sidea = a;
  //float sideb = b;
  //float sidec = c;
  float divider = 2*a*c;
  float ac = acos((pow(a,2)+pow(c,2)-pow(b,2))/divider);
  float B = degrees(ac);
  return B;
}
