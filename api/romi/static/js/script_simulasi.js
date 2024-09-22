// let movingRight = false;
// let movingLeft = false;
// let movingUp = false;
// let movingDown = false;

// let xpos = 400;
// let ypos = 300;
// let speed = 1;

// // var hasil = "Kiri";
// var Mi = "Lurus";
// var Emosi = "{{ hasil_emosi }}"";
var robot;

function preload() {  
  if(Emosi == "Senang"){
    if (Mi == "Lurus") {
      robot = loadImage('static/images/giphy.gif');
      movingDown = true;
    }
    if (Mi == "Kanan") {
      robot = loadAnimation(
        '../static/assets/images/robot-kanan.png'
      );
      movingRight = true;
    }

    if (Mi == "Kiri") {
      robot = loadAnimation(
        '../static/assets/images/robot-kiri.png'
      );
      movingLeft = true;
    }

    else {
      robot = loadAnimation(
        '../static/assets/images/robot-diam.png'
      );
    }
  } else {
    if (Mi == "Lurus") {
      robot = loadAnimation(
        '../static/assets/images/robot-maju.png'
      ); 
      movingDown = true;
    }

    if (Mi == "Kanan") {
      robot = loadAnimation(
        '../static/assets/images/robot-kanan.png'
      );
      movingRight = true;
    }

    if (Mi == "Kiri") {
      robot = loadAnimation(
        '../static/assets/images/robot-kiri.png'
      );
      movingLeft = true;
    }

    else {
      robot = loadAnimation(
        '../static/assets/images/robot-diam.png'
      );
    }
  }
}

function draw() {
  // background(51);

  // draw moving character
  // fill(255, 0, 0);

  image(robot, 50, 50);

  // update moving character
  // if (movingRight) {
  //   current_animation = robot;
  //   xpos += speed;
  // }
  // if (xpos == 700){
  //   movingRight = false;
  // }

  // if (movingLeft) {
  //   current_animation = robot;
  //   xpos -= speed;
  // }
  // if (xpos == 70) {
  //   movingLeft = false;
  // }


  // if (movingDown) {
  //   current_animation = robot;
  //   ypos -= speed;
  // }
  // if (ypos == 100){
  //   movingDown = false;
  // }

  // animation(current_animation, xpos, ypos);
  
  // // show boolean values onscreen for clarity
  // textSize(20);
  // // text("Aksi Saat ini : " + hasil, 10, 10, width/2, height/2);
  
  // current_animation = robot;
}