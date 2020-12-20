function Widget(c_id, s_id, x, y) {
    this.c_id = c_id;
    this.s_id = s_id;
    this.x = x;
    this.y = y;
}

Widget.prototype.signals = [
]

Widget.prototype.slots = [
]

Widget.prototype.copy = function() {
    return new Widget(this.c_id, this.s_id, this.x, this.y)
}

function Circle(c_id, s_id, x, y, r) {
    Widget.call(this, c_id, s_id, x, y);
    this.r = r;
}

Circle.prototype = Object.create(Widget.prototype)
Circle.prototype.constructor = Circle;
Circle.prototype.copy = function() {
    return new Circle(this.c_id, this.s_id, this.x, this.y, this.r)
}

function Rectangle(c_id, s_id, x, y, w, l) {
    Widget.call(this, c_id, s_id, x, y);
    this.w = w;
    this.l = l;
}

Rectangle.prototype = Object.create(Widget.prototype)
Rectangle.prototype.constructor = Rectangle;
Rectangle.prototype.copy = function() {
    return new Rectangle(this.c_id, this.s_id, this.x, this.y, this.w, this.l)
}

function Textbox(c_id, s_id, x, y, text) {
    Widget.call(this, c_id, s_id, x, y);
    this.text = text;
}

Textbox.prototype = Object.create(Widget.prototype)
Textbox.prototype.constructor = Textbox;
Textbox.prototype.copy = function() {
    return new Textbox(this.c_id, this.s_id, this.x, this.y, this.text)
}

export {Widget, Circle, Rectangle, Textbox};
