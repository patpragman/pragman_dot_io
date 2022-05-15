// Physics Gravity simulator!
// Pat Pragman
// Ciego Services
// 20APR22

// global variables for drawing everything
var SCREEN = document.getElementById('screen');
var CONTEXT = SCREEN.getContext("2d");

// global variable for tick rate
const dt = 0.000001

class Vector {
    constructor(x=0, y=0) {
        this.x = x;
        this.y = y;
    }

    vector_add(other_vector:Vector) {
        this.x = this.x + other_vector.x;
        this.y = this.y + other_vector.y;
    }

    multiply_by_number(real_number:number){
        this.x *= real_number
        this.y *= real_number
    }


}

class Object {
    constructor(r:Vector=Vector(0,0),
                v:Vector=Vector(0, 0),
                a:Vector=Vector(0,0),
                m=1){
        this.r = r;
        this.v = v;
        this.a = a;
        this.m = m;
    }

    update() {
        // scale the acceleration, then add that to the velocity vector
        var delta_v = this.a.multiply_by_number(dt)
        this.v = this.v.vector_add(delta_v)
        var delta_r = this.v.multiply_by_number(dt)
        this.r = this.r.vector_add(delta_r)
    }

    draw() {
        // draws circle of radius m at the vector r
        CONTEXT.beginPath();
        CONTEXT.arc(
            this.r.x,
            this.r.y,
            this.m,
            0, 2 * Math.PI,
            false)
        CONTEXT.stroke()
    }

}

function draw(objects){
    CONTEXT.globalCompositeOperation = 'desination-over';
    // clear everything
    CONTEXT.clearRect(0, 0, SCREEN.width, SCREEN.height);
    CONTEXT.save()

    for (let i = 0; i < length(objects); i++) {
        o = objects[i]
        o.update()
        o.draw()
        CONTEXT.save()
    }

}

o = Object()
o.v = Vector(1, 1)
var objects = [o]

window.requestAnimationFrame(draw)

ctx.fillStyle = "#FF0000";
ctx.fillRect(0, 0, 150, 75);