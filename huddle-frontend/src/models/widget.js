function Widget(c_id, s_id, x, y, type_name) {
    this.c_id = c_id;
    this.s_id = s_id;
    this.x = x;
    this.y = y;
    this.type_name = type_name;
}

Widget.prototype.slots = [
]

Widget.prototype.copy = function() {
    return new Widget(this.c_id, this.s_id, this.x, this.y, this.type_name)
}

function Circle(c_id, s_id, x, y, r, type_name) {
    Widget.call(this, c_id, s_id, x, y, type_name);
    this.r = r;
}

//TODO: make the type a default
Circle.prototype = Object.create(Widget.prototype)
Circle.prototype.constructor = Circle;
Circle.prototype.copy = function() {
    return new Circle(this.c_id, this.s_id, this.x, this.y, this.r, this.type_name)
}

function Rectangle(c_id, s_id, x, y, w, l, type_name) {
    Widget.call(this, c_id, s_id, x, y, type_name);
    this.w = w;
    this.l = l;
}

Rectangle.prototype = Object.create(Widget.prototype)
Rectangle.prototype.constructor = Rectangle;
Rectangle.prototype.copy = function() {
    return new Rectangle(this.c_id, this.s_id, this.x, this.y, this.w, this.l, this.type_name)
}

function Textbox(c_id, s_id, x, y, text, type_name) {
    Widget.call(this, c_id, s_id, x, y, type_name);
    this.text = text;
}

Textbox.prototype = Object.create(Widget.prototype)
Textbox.prototype.constructor = Textbox;
Textbox.prototype.copy = function() {
    return new Textbox(this.c_id, this.s_id, this.x, this.y, this.w, this.text, this.type_name)
}

export {Widget, Circle, Rectangle, Textbox};
