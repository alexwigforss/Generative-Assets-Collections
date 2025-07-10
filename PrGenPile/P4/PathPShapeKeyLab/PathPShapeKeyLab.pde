// Todo SineFactory
PShape path;
int linelength;
int maxaim =80;
int target = 3;
PVector tvec;
PVector tpos;
ArrayList<PVector> pvec;

int X;
int x;
float y;
float Tlutning;
float Tvinkel;
int aim;
int spread;
float r = 1;
PVector[] sekant = new PVector[2];
int beg, end;
void setup() {
  size(1040, 360, P2D);
  frameRate(120);
  linelength = 0;
  Tlutning = 0.0;
  initPath();
  curveFactory();
  print("Entering Main Loop");
  X=10;
  beg = X - 10;
  end = x + 10;
  tvec = new PVector(0, 0);
}

void draw() {
  if (auto){
    autoRun();
  }
  background(0);
  pushMatrix();

  scale(2, -2);
  translate(0, -height*0.5);
  //scale(1, -1);
  //translate(0, -height);
  //stroke(255, 0, 0);
  //Draw the path
  //shape(path);
  updateX();
  drawVects();
  stroke(255);
  angleLine();
  popMatrix();
  fill(255);
  //text(X +" " + tvec + "Lutning:  "+Tlutning + "Vinkel:  "+Tvinkel+"Start "+beg+"Slut "+end, 10, 10 );
}
// Bug arrayOutofbounds fixat temprärt där jag anropar den men måste såklart fixas inuti i stället.
float lutning(int t) {
  sekant[0]=path.getVertex(t-1);
  sekant[1]=path.getVertex(t+1);
  float lutar =(sekant[1].y - sekant[0].y)/(sekant[1].x-sekant[0].x);
  return lutar;
}
float vinkel() {
  return 0.0;
}
void angleLine() {
  stroke(0);
  //(X, 0, X, height);
  Tlutning = lutning(target);
  Tvinkel = -1/Tlutning;
  stroke(0, 255, 0);

  // Ritar från markerad vektor till punkten före och efter
  //line(tvec.x, tvec.y, sekant[1].x, sekant[1].y);
  //line(tvec.x, tvec.y, sekant[0].x, sekant[0].y);
  //stroke(0, 0, 255);
  //line(tvec.x, tvec.y, sekant[1].x, sekant[1].y);
  //line(tvec.x, tvec.y, sekant[0].x, sekant[0].y);

  stroke(0, 0, 255);
  fill(0, 0);
  //circle(tvec.x, tvec.y, 15);
  // Ritar linje från punkten -1 & +1
  //line(sekant[0].x, sekant[0].y, sekant[1].x, sekant[1].y);
}

void drawAngle(PVector p, float lut) {
  float v = -1/lut;
  if (v>0) {
    line(p.x, p.y, p.x+1000, p.y+1000*v);
    line(p.x, p.y, p.x-1000, p.y-1000*v);
  } else if (v<0 && v>-1e10) {
    line(p.x, p.y, p.x-1000, p.y-1000*v);
    line(p.x, p.y, p.x+1000, p.y+1000*v);
  } else {
    //line(p.x, p.y, p.x, p.y+1000);
  }
}

void drawTangent(PVector p, float lut) {
  float v = lut;
  if (v>0) {
    line(p.x, p.y, p.x+1000, p.y+1000*v);
    line(p.x, p.y, p.x-1000, p.y-1000*v);
  } else if (v<0 && v>-1e10) {
    line(p.x, p.y, p.x-1000, p.y-1000*v);
    line(p.x, p.y, p.x+1000, p.y+1000*v);
  } else {
    //line(p.x, p.y, p.x, p.y+1000);
  }
}


void drawVects() {
  int index = 0;
  for (PVector pv : pvec) {
    if (pv.x == X) {
      //circle(pv.x, pv.y, 10);
      target = index;
      tvec = pv;
      //stroke(255, 0, 0);
      if (index >=3 && index <= pvec.size()-3) {
        float plut = lutning(index);
        drawAngle(pv, plut);
        drawTangent(pv, plut);
      }
    } else {
      //circle(pv.x, pv.y, 5);
      if ((index >=3 && index <= pvec.size()-3)&&(index>beg)&&(index < end)) {
        stroke(150);
        float plut = lutning(index);
        drawAngle(pv, plut);
        drawTangent(pv, plut);
      }
      //if (index >=3 && index <= pvec.size()-3) {
        //float plut = lutning(index);
        //drawAngle(pv, plut);
      //}
    }
    index++;
  }
}

void curveFactory() {
  x = 0;
  y = 0;
  pvec = new ArrayList<PVector>();
  while (x < width) {
    // Calculate the path
    aim = int(random(y, maxaim));
    //spread = int(random(1, 4));
    spread = 2;
    r=random(1.1, 6.0);
    for (; y < aim; y+=r) {
      path.vertex(x, f_av_x(y));
      pvec.add(new PVector(x, f_av_x(y)));
      x+= spread;
    }
    aim = int(random(0, y));
    //spread = int(random(1, 4));
    spread = 2;
    for (; y > aim; y-=r) {
      path.vertex(x, f_av_x(y));
      pvec.add(new PVector(x, f_av_x(y)));
      x+= spread;
    }
  }
  path.endShape();
}

float f_av_x(float in) {
  float ut = pow(in,2)/14;
  return ut;
}

float f_av_xx(float in) {
  float ut = pow(y, 2)/20;
  return ut;
}

void initPath() {
  // Create the shape
  path = createShape();
  path.beginShape();

  // Set fill and stroke
  path.noFill();
  path.stroke(255);
  path.strokeWeight(2);
}
