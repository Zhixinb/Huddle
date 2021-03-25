var math = require('mathjs-expression-parser')


function Widget(c_id, s_id, x, y, type_name) {
    this.c_id = c_id;
    this.s_id = s_id;
    this.x = x;
    this.y = y;
    this.type_name = type_name;
}


Widget.signals = {
    "Circle": {
        "radius_changed": function(radius) {
            return radius;
        }
    },
    "Rectangle": {
        "width_changed": function(width) {
            return width;
        },
        "length_changed": function(length) {
            return length;
        }
    },
    "Image": {
        "width_changed": function(width) {
            return width;
        },
        "length_changed": function(length) {
            return length;
        }
    },
    "Textbox": {
    },
    "Slider": {
        "value_changed": function (value) {
            return value
        }
    }

}

Widget.slots = {
    "Circle": {
        "update_radius": function(value) {
            return {"radius": value}
        }
    },
    "Rectangle": {
        "update_width":  function(value) {
            return {"width": value}
        },
        "update_length": function(value) {
            return {"length": value}
        }
    },
    "Image": {
        "update_width":  function(value) {
            return {"width": value}
        },
        "update_length": function(value) {
            return {"length": value}
        }
    },
    "Textbox": {
    },
    "Slider": {

    }
}

Widget.map_signal = function(type, signal, arg) {
    return Widget.signals[type][signal](arg)
}


Widget.map_slot = function(type, slot, arg) {
    return Widget.slots[type][slot](arg)
}

Widget.map = function(signal_type, slot_type, signal, slot, arg, expression) {
    try {
        const value = math.eval(expression);
        return Widget.map_slot(slot_type, slot, value * Widget.map_signal(signal_type, signal, arg))
    } catch (error) {
        return Widget.map_slot(slot_type, slot, math.eval(expression, {x: Widget.map_signal(signal_type, signal, arg)}))
    }
    return Widget.map_slot(slot_type, slot, Widget.map_signal(signal_type, signal, arg))
}

Widget.copy = function(widget) {
    if (widget.type_name === "Textbox") {
        return new Textbox(widget.c_id, widget.s_id, widget.x, widget.y, widget.text, widget.type_name)
    } else if (widget.type_name === "Circle") {
        return new Circle(widget.c_id, widget.s_id, widget.x, widget.y, widget.radius, widget.type_name)
    } else if (widget.type_name === "Rectangle") {
        return new Rectangle(widget.c_id, widget.s_id, widget.x, widget.y, widget.width, widget.length, widget.type_name)
    } else if (widget.type_name === "Image") {
        return new Image(widget.c_id, widget.s_id, widget.x, widget.y, widget.src, widget.width, widget.length, widget.type_name)
    } else if (widget.type_name === "Slider") {
        return new Slider(widget.c_id, widget.s_id, widget.x, widget.y, widget.value, widget.type_name)
    }
    return null;
}

function Circle(c_id, s_id, x, y, radius) {
    Widget.call(this, c_id, s_id, x, y, "Circle");
    this.radius = radius;
}

//TODO: make the type a default
Circle.prototype = Object.create(Widget.prototype)
Circle.prototype.constructor = Circle;

function Rectangle(c_id, s_id, x, y, width, length) {
    Widget.call(this, c_id, s_id, x, y, "Rectangle");
    this.width = width;
    this.length = length;
}

Rectangle.prototype = Object.create(Widget.prototype)
Rectangle.prototype.constructor = Rectangle;

function Image(c_id, s_id, x, y, src, width, length) {
    Widget.call(this, c_id, s_id, x, y, "Image");
    this.src = src;
    this.width = width;
    this.length = length;
}

Image.prototype = Object.create(Widget.prototype)
Image.prototype.constructor = Image;

function Textbox(c_id, s_id, x, y, text) {
    Widget.call(this, c_id, s_id, x, y, "Textbox");
    this.text = text;
}

Textbox.prototype = Object.create(Widget.prototype)
Textbox.prototype.constructor = Textbox;

function Slider(c_id, s_id, x, y, value) {
    Widget.call(this, c_id, s_id, x, y, "Slider");
    this.value = value;
}

Slider.prototype = Object.create(Widget.prototype)
Slider.prototype.constructor = Slider;

export {Widget, Circle, Rectangle, Image, Textbox, Slider};
