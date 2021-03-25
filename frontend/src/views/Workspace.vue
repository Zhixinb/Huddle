<template>
    <v-app>
    
    <v-navigation-drawer app clipped>
        <v-list dense>
            <v-list-item v-for="s in slides" :key="s.id" link @click.stop="update_slide(s.id)" :style="curr_slide_id === s.id ? {'background-color': 'lightblue'} : {}">
                <v-list-item-content>
                    <slide :id="s.id" :focus="is_slide_focus(s.id)"> </slide>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer app clipped right v-if="can_share">
        <v-list>
            <v-list-item v-if="selected_widgets.length > 0">
                <v-list-item-content>
                    <Property :index="0" :c_id="selected_widgets[0]" :s_id="curr_slide_id" :type="slides[curr_slide_id]['components'][selected_widgets[0]].type_name"
                            :p="slides[curr_slide_id]['components'][selected_widgets[0]]" 
                            :items="signals"
                            :key="selected_widgets[0]"
                            @property_changed="property_changed"
                            @signal_changed="signal_changed"
                            @deselect_clicked="deselect_clicked"/>
                </v-list-item-content>
            </v-list-item>
            <v-btn v-if="selected_widgets.length > 1"
                color="success"
                plain
                small
                @click="swap_clicked"
            >
                <v-icon dark>
                    mdi-swap-vertical
                </v-icon>
            </v-btn>
            <v-list-item v-if="selected_widgets.length > 1">
                <v-list-item-content>
                    <Property :index="1" :c_id="selected_widgets[1]" :s_id="curr_slide_id" :type="slides[curr_slide_id]['components'][selected_widgets[1]].type_name"
                            :p="slides[curr_slide_id]['components'][selected_widgets[1]]" 
                            :items="slots"
                            :key="selected_widgets[1]"
                            @property_changed="property_changed"
                            @slot_changed="slot_changed"
                            @deselect_clicked="deselect_clicked"/>
                </v-list-item-content>
            </v-list-item>
            <v-list-item>
                <v-list-item-content v-if="valid()"> 
                    <v-text-field
                        v-model="expression"
                        label="Expression"
                        >
                        <v-tooltip slot="append" left> 
                            <template v-slot:activator="{ on, attrs }">
                                <v-icon v-on="on" color="primary" dark>
                                    mdi-information
                                </v-icon>
                            </template>
                            <span>An expression is a transformation applied from the signal to slot <br/>
                                Enter 1 or any constant for scaling<br/> 
                                Enter a function of x for more complex transformations
                            </span>
                        </v-tooltip>
                    </v-text-field>
                </v-list-item-content>
            </v-list-item>
        </v-list>
        <v-btn
            v-if="valid() && !connection_exist() && expression_valid() && selection_valid()"
            color="primary"
            @click="add_connection()"
            >
            Connect
        </v-btn>
        <v-btn
            v-if="valid() && connection_exist() && expression_valid() && selection_valid()"
            color="success"
            @click="add_connection()"
            >
            Update
        </v-btn>
        <v-btn
            v-if="valid() && connection_exist()"
            color="error"
            @click="remove_connection()"
            >
            Remove
        </v-btn>
    </v-navigation-drawer>
    
    <v-app-bar app clipped-left clipped-right permanent>
        <v-toolbar-title>Huddle (Slide:{{ curr_slide_id }}, Role: {{role}}) </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="rectangle" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd" :disabled='!can_share'>
                    <v-icon>mdi-square</v-icon>
                </v-btn>
            </template>
            <span>New Rectangle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="circle" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd" :disabled='!can_share'>
                    <v-icon>mdi-circle</v-icon>
                </v-btn>
             </template>
             <span>New Circle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="textbox" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd" :disabled='!can_share'>
                    <v-icon>mdi-format-textbox</v-icon>
                </v-btn>
             </template>
             <span>New Textbox</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="slider" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd" :disabled='!can_share'>
                    <v-icon>mdi-textbox</v-icon>
                </v-btn>
             </template>
             <span>New Slider</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="append_slide" :disabled='!can_share'>
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
             </template>
             <span>New Slide</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="toggle">
                    <v-icon>mdi-fullscreen</v-icon>
                </v-btn>
             </template>
             <span>Fullscreen</span>
        </v-tooltip>
        <permission-modal/>
        <user-dropdown></user-dropdown>
    </v-app-bar>
   
    <div class="pa-5">
        <v-fade-transition appear>
            <v-card id ="graph-wrapper" :width="w" :height="h" v-on:dragover="dragOver">
                <fullscreen ref="fullscreen" @change="fullscreenChange" background=#FFF>
                    <div id="test" :style="{'width': w + 'px' , 'height': h + 'px'}" v-on:click="widgetClicked($event, -1, -1)"></div>
                    <Textbox v-if="preview !== null && preview.type_name == 'Textbox'"
                        :x="w * preview.x" :y="h * preview.y" :text="preview.text" :style="style"/>
                    <MyCircle v-else-if="preview !== null && preview.type_name == 'Circle'" 
                        :x="w * preview.x" :y="h * preview.y" :radius="preview.radius" :rgba="preview.rgba" :style="style"/>
                    <MyRect v-else-if="preview !== null && preview.type_name == 'Rectangle'" 
                        :x="w * preview.x" :y="h * preview.y" :width="preview.width" :length="preview.length" :rgba="preview.rgba" :style="style"/>
                    <Slider v-else-if="preview !== null && preview.type_name == 'Slider'" 
                        :x="w * preview.x" :y="h * preview.y" :value="preview.value" :style="style"/>
                  <!-- TODO: fix empty list error, check slides.length before accessing component -->
                    <div v-for="(l, index) in lines" :key="-index-1">
                        <MyLine :x0="w * l[0]" :y0="h * l[1]" :x1="w * l[2]" :y1="h * l[3]" :style="style" :index="index"/>
                    </div>
                    <div v-for="c in slides[curr_slide_id].components" :key="c.c_id">
                        <div v-if="c.type_name === 'Textbox'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Textbox :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :text="c.text" 
                                :style="style" :glow="glow(c.c_id)" :glow_color="glow_color(c.c_id)" :focus="is_focus(c.c_id)"/>
                        </div>
                        <div v-else-if="c.type_name === 'Circle'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyCircle :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :radius="c.radius" :rgba="c.rgba"
                                :style="style" :glow="glow(c.c_id)" :glow_color="glow_color(c.c_id)" :focus="is_focus(c.c_id)"/>
                        </div>
                        <div v-else-if="c.type_name == 'Rectangle'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyRect :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :width="c.width" :length="c.length" :rgba="c.rgba"
                                :style="style" :glow="glow(c.c_id)" :glow_color="glow_color(c.c_id)" :focus="is_focus(c.c_id)"/>
                        </div>
                        <div v-else-if="c.type_name == 'Slider'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Slider :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :value="c.value" 
                                @value_changed="value_changed" :style="style" :glow="glow(c.c_id)" :glow_color="glow_color(c.c_id)"
                                :focus="is_focus(c.c_id)"/>
                        </div>
                    </div>
                </fullscreen>
            </v-card>
        </v-fade-transition>
    </div>

    </v-app>
</template>

<script>
import AppNav from '@/components/app/Nav'
import Slide from '@/components/app/Slide';
import PermissionModal from '@/components/app/PermissionModal';
import HotkeyMenu from '@/components/app/HotkeyMenu';
import UploadMenu from '@/components/app/UploadMenu';
import {mapState, mapMutations} from 'vuex';
import fullscreen from 'vue-fullscreen';
import Vue from 'vue';
import Property from '../components/properties/Property.vue';
import Textbox from '../components/widgets/Textbox.vue';
import Circle from '../components/widgets/Circle.vue';
import Rect from '../components/widgets/Rect.vue';
import Slider from '../components/widgets/Slider.vue';
import Line from '../components/widgets/Line.vue';
//import FileSaver from '../plugins/FileSaver.js'
import {Widget, Circle as CircleWidget, Rectangle as RectWidget, 
        Textbox as TextWidget, Slider as SliderWidget} from '../models/widget.js';
import { generate_lines } from '../utils/util.js'
import UserDropdown from '../components/app/UserDropdown.vue';
import dbHelper from '../db'
import sessionTracking from '@/mixins/sessionTracking'
var math = require('mathjs-expression-parser')


Vue.use(fullscreen);

export default {
    name: 'Workspace',    
    data: () => ({
        curr_room_id: '',
        fullscreen: false,
        show: false,
        scale: 1,
        fields: [],
        count: 0,

        expression: 'x',
        signal: '',
        slot: '',
        signals: [],
        slots: [],
        focus: '',
        default_color: {r: 0, g: 100, b: 255, a: 0.75},

        // Dragging elements state
        preview: null,
        w: screen.width * 0.7,
        h: screen.height * 0.7
        
    }),
    created() {
        window.addEventListener('keydown', (e) => {
            if (this.focus && (e.key === 'Delete')) {
                if (this.focus === 'slide') {
                    var keys = Object.keys(this.slides)
                    const found = keys.find(e => e !== this.curr_slide_id)
                    if (found) {
                        const params = {
                            uid: this.$store.getters.uid,
                            room: this.$store.getters.room,
                            s_id: this.curr_slide_id
                        }
                        this.$socket.emit('remove_slide', params)
                    }
                } else {
                    const params = {
                        uid: this.$store.getters.uid,
                        room: this.$store.getters.room,
                        s_id: this.curr_slide_id,
                        c_id: this.focus
                    }
                    this.$socket.emit('remove_component', params)
                }
            }
        });
        if (this.$store.getters.uid === null) {
            console.log("user not logged in")
            this.redirectToLogin();
        }

        dbHelper.logMetric(this.$options.name)
    },
    beforeMount () {
        const params = {
            uid: this.$store.getters.uid,
            room: this.$store.getters.room,
            sid: this.$store.getters.sid
        }
        
        this.$socket.emit('join', params)
        this.$socket.emit('get_share_state', params)
        this.set_selected_widgets([])
        this.set_lines([])
    },
    beforeDestroy () {
        const params = {
            uid: this.$store.getters.uid,
            room: this.workspace.workspace_id
        }
        this.$socket.emit('leave', params)
    },
    methods:
    {
        ...mapMutations(['set_room']),
        ...mapMutations('ws', ['set_lines', 'set_selected_widgets', 'set_curr_slide_id']),
        update_slide(id) {
            this.set_curr_slide_id(id);
            this.signal = ""
            this.slot = ""
            this.signals = []
            this.slots = []
            this.focus = 'slide'
            this.set_selected_widgets([])
            this.set_lines([])
        },
        append_slide() {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
            }
            this.$socket.emit('new_slide', params)
        },
        download_json() {
            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.slides));
            var downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href",     dataStr);
            downloadAnchorNode.setAttribute("download", "slides_data.json");
            document.body.appendChild(downloadAnchorNode); // required for firefox
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        },
        glow: function(c_id) {
            return this.selected_widgets[0] === c_id || this.selected_widgets[1] === c_id
        },
        glow_color: function(c_id) {
            if (c_id === this.selected_widgets[0]) {
                return 'steelblue'
            } else if (c_id === this.selected_widgets[1]) {
                return 'red'
            } else {
                return ''
            }
        },
        is_focus: function(c_id) {
            return this.focus === c_id
        },
        is_slide_focus: function(s_id) {
            return this.curr_slide_id === s_id && this.focus === 'slide'
        },
        generate_slot_changes: function(s_id, c_id, changes) {
            const connections = this.slides[s_id]["connections"]
            const components = this.slides[s_id]["components"]
            var value = {
            }
            if (!(c_id in components)) {
                return value
            }
            value[c_id] = {}
            var queue = []
            for (const signal in changes) {
                queue.push([c_id, signal])
                value[c_id][signal] = changes[signal]
            }
            while (queue.length > 0) {
                const [signal_c_id, signal_name] = queue.shift();
                const signal = signal_name + "_changed"
                const signal_value = value[signal_c_id][signal_name]
                const signal_type = components[signal_c_id].type_name
                if (signal in Widget.signals[signal_type] && signal_c_id in connections && signal in connections[signal_c_id]) {
                    const slots = connections[signal_c_id][signal];
                    for (const slot_c_id in slots) {
                        for (const slot in slots[slot_c_id]) {
                            const slot_type = components[slot_c_id].type_name
                            const expression = slots[slot_c_id][slot]
                            const slot_changes = Widget.map(signal_type, slot_type, signal, slot, signal_value, expression)
                            for (const key in slot_changes) {
                                if (!(slot_c_id in value)) {
                                    value[slot_c_id] = {}
                                }
                                value[slot_c_id][key] = slot_changes[key]
                                queue.push([slot_c_id, key])
                            }
                        }
                    }
                }
            }
            return value
        },
        generate_lines: function(s_id, c_id) {
            return generate_lines(s_id, c_id, this.slides)
        },
        compute_signals: function() {
            if (this.selected_widgets.length > 0) {
                return Object.keys(Widget.signals[this.slides[this.curr_slide_id]["components"][this.selected_widgets[0]].type_name])
            } else {
                return []
            }
        },
        compute_slots: function() {
            if (this.selected_widgets.length > 1) {
                const c_id = this.selected_widgets[1]
                const type_name = this.slides[this.curr_slide_id]["components"][c_id].type_name
                const bc = this.slides[this.curr_slide_id]["backward_connections"][c_id]
                if (bc === undefined) {
                    return Object.keys(Widget.slots[type_name])
                } else {
                    return Object.keys(Widget.slots[type_name]).map(item => {return {text: item, 
                        disabled: item in bc && !(bc[item][0] === this.selected_widgets[0] && bc[item][1] === this.signal)}})
                }
            } else {
                return []
            }
        },
        // Signals
        value_changed: function (value) {
            const s_id = value.s_id
            const c_id = value.c_id
            const v = value.value

            const changes = this.generate_slot_changes(s_id, c_id, {"value": v})
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: s_id,
                changes: changes
            }
            this.$socket.emit('update_component_id_batch', params)
        },
        text_changed: function (value) {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: value.s_id,
                c_id: value.c_id,
                changes: {"text": value.text}
            }
            this.$socket.emit('update_component_id', params)
        },
        property_changed: function (event) {
            const changes = {}
            changes[event.key] = event.value
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: event.s_id,
                c_id: event.c_id,
                changes: changes
            }
            this.$socket.emit('update_component_id', params)
        },
        signal_changed: function(value) {
            this.signal = value;
            this.slots = this.compute_slots()
        },
        slot_changed: function(value) {
            this.slot = value;
        },
        deselect_clicked: function(value) {
            this.set_selected_widgets(this.selected_widgets.filter((_, i) => i !== value))
            if (value === 0) {
                this.signal = ""
                this.signals = this.compute_signals()
            }
            if (this.selected_widgets.length > 0) {
                this.set_lines(this.generate_lines(this.curr_slide_id, this.selected_widgets[0]))
            } else {
                this.set_lines([])
            }
        },
        swap_clicked: function() {
            this.set_selected_widgets([this.selected_widgets[1], this.selected_widgets[0]])
            this.signal = ""
            this.signals = this.compute_signals()
            this.slot = ""
            this.slots = this.compute_slots()
        },    
        toggle() {
            this.$refs['fullscreen'].toggle()
        },
        fullscreenChange(full) {
            if (full) {
                this.w = screen.width;
                this.h = screen.height;
                this.scale = 10 / 7;
            } else {
                this.w = screen.width * 0.7;
                this.h = screen.height * 0.7;
                this.scale = 1
            }
            this.fullscreen = full
        },
        dragStart:function(event) {
            event.dataTransfer.setDragImage(document.createElement('div'), 0, 0);
            const widget = event.target.id;
            if (widget === 'textbox') {
                this.preview = new TextWidget(-1, this.curr_slide_id, 0, 0, "Text");
            } else if (widget === 'circle') {
                this.preview = new CircleWidget(-1, this.curr_slide_id, 0, 0, 25, this.default_color)
            } else if (widget === 'rectangle') {
                this.preview = new RectWidget(-1, this.curr_slide_id, 0, 0, 50, 50, this.default_color)
            } else if (widget === 'slider') {
                this.preview = new SliderWidget(-1, this.curr_slide_id, 0, 0, 50)
            } else {
                this.preview = null;
            }
        },
        dragOver:function(event) {
            event.preventDefault()
            if (this.fullscreen) {
                if (event.x >= 0 && event.x <= this.w && event.y >= 0 && event.y <= this.h) {
                    this.preview.x = event.x / this.w;
                    this.preview.y = event.y / this.h;
                }
            } else {
                const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
                if (event.x <= pos.right && event.y <= pos.bottom && event.x >= pos.left && event.y >= pos.top) {
                    this.preview.x = (event.x - pos.x) / this.w;
                    this.preview.y = (event.y - pos.y) / this.h;
                }
            }
        },
        dragEnd:function(event) {
            if (this.preview != null) {
                const params = {
                    uid: this.$store.getters.uid,
                    room: this.$store.getters.room,
                    component: this.preview
                }
                this.$socket.emit('new_component', params)
                dbHelper.logMetric("ComponentCreated")
            }
            this.preview = null;
        },
        widgetDragStart:function(event, widget) {
            event.dataTransfer.setDragImage(document.createElement('div'), 0, 0);
            this.preview = Widget.copy(widget);
        },
        widgetDragEnd:function(event, widget) {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: this.preview.s_id,
                c_id: this.preview.c_id,
                changes: {"x": this.preview.x, "y": this.preview.y}
            }
            this.$socket.emit('update_component_id', params)
            this.preview = null;
        },
        widgetClicked:function(event, s_id, c_id) {
            if (s_id === -1 && c_id === -1) {
                this.focus = ''
                this.set_selected_widgets([])
                this.set_lines([])
            } else if (s_id === this.curr_slide_id) {
                this.focus = c_id;
                if (this.selected_widgets.indexOf(c_id) === -1 && this.selected_widgets.length < 2) {
                    this.set_selected_widgets(this.selected_widgets.concat([c_id]))
                    if (this.selected_widgets.length === 1) {
                        this.signal = ""
                        this.signals = this.compute_signals()
                    } else if (this.selected_widgets.length === 2) {
                        this.slot = ""
                        this.slots = this.compute_slots()
                    }
                    this.set_lines(this.generate_lines(s_id, c_id).concat(this.lines))
                }
            }
        },
        add_connection() {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: this.curr_slide_id,
                c_id0: this.selected_widgets[0],
                c_id1: this.selected_widgets[1],
                signal: this.signal,
                slot: this.slot,
                expression: this.expression
            }
            this.$socket.emit('new_connection', params)
            dbHelper.logMetric("ConnectionCreated")
        },
        remove_connection() {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: this.curr_slide_id,
                c_id0: this.selected_widgets[0],
                c_id1: this.selected_widgets[1],
                signal: this.signal,
                slot: this.slot
            }
            this.$socket.emit('remove_connection', params)
        },
        valid() {
            return this.selected_widgets.length == 2 && this.signal !== "" && this.slot !== "";
        },
        expression_valid() {
            try {
                const value = math.eval(this.expression, {x: 1});
                if (value === undefined) {
                    return false
                }
            } catch (error) {
                return false
            }
            return true;
        },
        selection_valid() {
            const signal_c_id = this.selected_widgets[0]
            const slot_c_id = this.selected_widgets[1]
            const bc = this.slides[this.curr_slide_id]["backward_connections"][slot_c_id]
            return bc === undefined || !(this.slot in bc) || (bc[this.slot][0] === signal_c_id && bc[this.slot][1] === this.signal)
        },
        connection_exist() {
            const signal_c_id = this.selected_widgets[0]
            const slot_c_id = this.selected_widgets[1]
            const bc = this.slides[this.curr_slide_id]["backward_connections"][slot_c_id]
            return bc !== undefined && this.slot in bc && (bc[this.slot][0] === signal_c_id && bc[this.slot][1] === this.signal)
        },
        async redirectToLogin() {
            this.$router.push({ name: 'Login'})
        }
    },
    components: {
        Slide,
        Textbox,
        'MyCircle': Circle,
        'MyRect': Rect,
        Slider,
        'MyLine': Line,
        PermissionModal,
        Property,
        AppNav,
        UserDropdown,
        HotkeyMenu,
        UploadMenu
    },
    computed: {
        ...mapState(['workspace']),
        ...mapState('ws', ['role', 'slides', 'can_share', 'lines', 'selected_widgets', 'curr_slide_id']),
        style () {
            return {
                transform: 'scale(' + this.scale + ')',
                transformOrigin: 'top left'
            }
        }
    },
    watch: {
        role (newState) {
            if (newState === 'PERM_DENIED') {
                console.log("User doesn't have permission, redirected to home")
                this.$router.push({ name: 'Home'})
            }
        }
    },
    mixins: [sessionTracking]
}
</script>
