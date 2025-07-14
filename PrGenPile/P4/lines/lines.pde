PVector sv, ev;
float a = 0.0;
float inc = TWO_PI/20.0;
float b = 0.0;
int rndwall, rndval, lineX, lineY, delej, itt = 0;

void setup()  {
  size(640, 480); 
  fill(0,50);stroke(155);
  frameRate(8);
  sv = new PVector(width/100, height/100);
  ev = new PVector(0, 0);
}

void draw()  {
  if (delej == 0)  {
  rect(0,0,width,height);
  strokeWeight(1);
  float x=random(width),y=random(height);
    for (int i = 0; i < 10; i=i+2) {
      newseed();
      //stroke(map(i,0,500,0,255));
      line(ev.x,ev.y,lineX,lineY);
      }}
  delej++;
  if (delej >= 2)  {  delej=0;  }
  //ellipse(ev.x, ev.y, 12, 12);
  ev.add(sv);
  itt++;
  if (itt >= 100)  {  itt = 0;  }
  println(itt); 
}

void newseed()  {
  rndwall = int(random(4));
  switch(rndwall) {
    case 0:  lineX=int(random(width)); lineY=height;  break;
    case 1:  lineX=width; lineY=int(random(height));  break;
    case 2:  lineX=int(random(width)); lineY=0;       break;
    case 3:  lineX=0; lineY=int(random(height));      break;
  }
}
