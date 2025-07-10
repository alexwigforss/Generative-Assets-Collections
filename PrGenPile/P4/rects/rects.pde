int nRects = 20;
Square[] rects;
IntList bases;
IntList heights;
int roof, index;
void setup() {
  size(800, 400);
  frameRate(2);
  print(bases);
  stroke(0);
  strokeWeight(2);
}

void draw() {
  //fill(0,20);
  fill(255);
  rect(0,0,width,height);
  fill(255,255);
  bases = randomBases();
  heights = randomHeights();
  roof = bases.size()-1;

  scale(1, -1);
  translate(0, -height);
  int x=0;
  index = 0;
  
  for (;index < roof;index++) {
    x = x + bases.get(index);
    rect(x,0,bases.get(index+1), heights.get(index));
    line(x,heights.get(index),x+bases.get(index+1), heights.get(index+1));
    //print(index);
  }
}

IntList randomBases() {
  IntList list = new IntList();
  list.append(0);
  int i = 0;
  while (i < width) {
    int rand = int(random(width/8));
    list.append(rand);
    i += rand;
  }
  return list;
}

IntList randomHeights() {
  IntList list = new IntList();
  //list.append(0);
  int i = 0;
  while (i < bases.size()) {
    int rand = int(random(height));
    list.append(rand);
    i ++;
  }
  return list;
}

class Square {
  int x, y, w, h;
  Square() {
    x = 0;
    y = 0;
    w = 0;
    h = 0;
  }

  void draw() {
    rect(x, y, w, h);
  }
}
