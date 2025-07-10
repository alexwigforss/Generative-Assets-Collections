let clicked = []; // Vi kan använda en vanlig array
let Vectors = [];
let pvec;
let mus;
let a;
let Msg;
let Dots = [];
let Tris = [];
let wHandleHold = [-1, -1];
let holding = false;
let globalIndex = 0;
let handleradius = 20;

function setup() {
  createCanvas(600, 600);
  stroke(255);
  textAlign(CENTER, CENTER);
  textSize(16);
  Msg = "Hejhej";
  handleradius = 20;
}



function draw() {
  mus = createVector(mouseX, mouseY);
  background(175);

  for (let dott of Dots) {
    dott.drawDott();
    dott.update();
  }

  for (let tri of Tris) {
    tri.drawTri();
  }

  fill(255);
  text(Msg, width / 2, 20);
}

function distVecMouse(vec) {
  let d = dist(vec.x, vec.y, mouseX, mouseY);
  return d;
}

function distVecVec(v1, v2) {
  let d = dist(v1.x, v1.y, v2.x, v2.y);
  console.log(d);
  return d;
}

function mouseMoved() {
  Msg = mouseX + " " + mouseY;

  if (Dots.length > 0) {
    let d = Dots[Dots.length - 1];
    Msg += " " + d.pos.dist(mus);
  }

  for (let i = 0; i < Vectors.length; i++) {
    let vect = Vectors[i];
    if (distVecMouse(vect) < 5) {
      // Just nu gör vi inget när musen är nära
      // Du kan t.ex. highlighta vektorer här!
    }
  }
}

function mousePressed() {
  wHandleHold = mouseOverHandle();

  if (Tris.length > 0 && wHandleHold[0] >= 0) {
    holding = true;

  } else if (Dots.length === 2) {
    Dots.push(new Dott(mouseX, mouseY));
    Vectors.push(createVector(mouseX, mouseY));

    Tris.push(new Triangle(Dots[0], Dots[1], Dots[2]));

    Dots = [];
    globalIndex = 0;

  } else {
    Dots.push(new Dott(mouseX, mouseY));
    Vectors.push(createVector(mouseX, mouseY));
  }
}

function mouseDragged() {
  if (holding) {
    let tri = Tris[wHandleHold[0]];
    tri.moveHandle(wHandleHold[1]);
  }
}

function mouseReleased() {
  holding = false;
}





function mouseOverHandle() {
  let ret = [-1, -1];
  for (let i = 0; i < Tris.length; i++) {
    let tri = Tris[i];
    for (let d of tri.dotts) {
      if (d.pos.dist(mus) < handleradius) {
        ret[0] = i;         // triangel-index
        ret[1] = d.index;   // punkt-index
        return ret;
      }
    }
  }
  return ret;
}

function keyPressed() {
  if (key === 'Delete' || key === 'Backspace') {
    Tris = [];
    console.log("Alla trianglar raderade.");
  }
}
