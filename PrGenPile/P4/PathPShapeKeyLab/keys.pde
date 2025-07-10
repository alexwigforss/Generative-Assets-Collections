boolean left, right, auto=false;
int delay = 0;
void setBegEnd() {
  beg = X/2 - 10;
  //if(beg<0);
  //  beg=0;
  end = X/2 + 10;
  //if(end>pvec.size())
  //  end = pvec.size();
}

void autoRun() {
  if (millis()>delay) {
    delay = millis()+40;
    println(delay);
    X+=2;
    if (X>=width-3) {
      X=2;
      initPath();
      curveFactory();
    }
    setBegEnd();
  }
}

void updateX() {
  if (left) {
    X-=2;
    if (X<=0) {
      X=width;
    }
    setBegEnd();
    //left = !left;
  }
  if (right) {
    X+=2;
    if (X>=width-3) {
      X=2;
    }
    setBegEnd();
    //right = !right;
  }
}

void keyPressed() {
  switch(key) {
  case '-':
    X-=2;
    if (X<=0) {
      X=width;
    }
    break;
  case '+':
    X+=2;
    if (X>=width-3) {
      X=2;
    }
    break;
  }
  switch(keyCode) {
  case LEFT:
    left = true;
    break;
  case RIGHT:
    right = true;
    break;
  case ENTER:
    auto = !auto;
    break;
  case ' ':
    initPath();
    curveFactory();
    println("Anykey Pressed");
    break;
  }
}
void keyReleased() {
  switch(keyCode) {
  case LEFT:
    left = false;
    break;
  case RIGHT:
    right = false;
    break;
  }
}
