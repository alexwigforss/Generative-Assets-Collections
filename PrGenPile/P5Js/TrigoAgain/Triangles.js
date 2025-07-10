class Dott {
  constructor(x, y) {
    this.index = globalIndex++;
    this.pos = createVector(x, y);
    this.fwd = createVector(mouseX, mouseY);
  }

  drawDott() {
    stroke(255);
    fill(255);
    ellipse(this.pos.x, this.pos.y, 30, 30);
    stroke(0);
    line(this.pos.x, this.pos.y, this.pos.x + this.fwd.x, this.pos.y + this.fwd.y);
    fill(0);
  }

  update() {
    if (this.index === Dots.length - 1) {
      this.fwd = createVector(mouseX, mouseY);
      this.fwd.sub(this.pos);
      this.fwd.normalize();
      this.fwd.mult(this.pos.dist(mus));
    } else if (this.index < Dots.length - 1) {
      let d = Dots[this.index + 1];
      this.fwd = createVector(d.pos.x, d.pos.y);
      this.fwd.sub(this.pos);
    }
  }
}
  
class Triangle {
  constructor(a, b, c) {
    this.dotts = [a, b, c];
    this.sides = [0, 0, 0];
    this.mpv = [createVector(), createVector(), createVector()];
    this.update();
  }

  update() {
    for (let i = 0; i < 3; i++) {
      if (i === 0 || i === 1) {
        this.mpv[i] = p5.Vector.lerp(this.dotts[i].pos, this.dotts[i + 1].pos, 0.5);
      } else {
        this.mpv[i] = p5.Vector.lerp(this.dotts[i].pos, this.dotts[0].pos, 0.5);
      }
    }

    this.sides[0] = this.dotts[0].pos.dist(this.dotts[1].pos);
    this.sides[1] = this.dotts[1].pos.dist(this.dotts[2].pos);
    this.sides[2] = this.dotts[2].pos.dist(this.dotts[0].pos);
  }
  
    moveHandle(who) {
    this.dotts[who].pos = mus.copy();
    this.update();
  }
  
    drawTri() {
    fill(255);
    stroke(0);
    triangle(
      this.dotts[0].pos.x, this.dotts[0].pos.y,
      this.dotts[1].pos.x, this.dotts[1].pos.y,
      this.dotts[2].pos.x, this.dotts[2].pos.y
    );

    let i = 4;
    for (let d of this.dotts) {
      fill(255);
      circle(d.pos.x, d.pos.y, handleradius * 2);
      fill(0);
      let angle = degreeFromSides(
        this.sides[(i - 1) % 3],
        this.sides[i % 3],
        this.sides[(i + 1) % 3]
      );
      text(nf(angle, 1, 1), d.pos.x, d.pos.y);
      i++;
    }

    for (let j = 0; j < 3; j++) {
      let mv = this.mpv[j];
      text(nf(this.sides[j], 1, 1), mv.x, mv.y);
    }

    let c = this.center(this.mpv);
    fill(200, 0, 0);
    circle(c.x, c.y, 10);
  }
  
    center(cvps) {
    return createVector(
      (cvps[0].x + cvps[1].x + cvps[2].x) / 3,
      (cvps[0].y + cvps[1].y + cvps[2].y) / 3
    );
  }

  yield() {
    console.log("Jag är en triangel.");
  }
}

function radFromSides(a, b, c) {
  let divider = 2 * a * c;
  let B = acos((pow(a, 2) + pow(c, 2) - pow(b, 2)) / divider);
  return B;
}

function degreeFromSides(a, b, c) {
  let divider = 2 * a * c;
  let angleRad = acos((pow(a, 2) + pow(c, 2) - pow(b, 2)) / divider);
  return degrees(angleRad);
}
