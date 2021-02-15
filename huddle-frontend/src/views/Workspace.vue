<template>
    <v-app>
    
    <v-navigation-drawer app clipped>
        <v-list dense>
            <v-list-item v-for="s in slides" :key="s.id" link @click.stop="update_slide(s.id)">
                <v-list-item-content>
                    <slide :id="s.id"> </slide>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer app clipped right>
        <v-list>
            <v-list-item v-for="(c_id, index) in this.selected_widgets" :key="c_id" link>
                <v-list-item-content>
                    <div v-if="slides[curr_slide_id]['components'][c_id].type_name === 'Textbox'">
                        <Property :index="index" :c_id="c_id" :s_id="curr_slide_id" :type="'Textbox'"
                            :t="slides[curr_slide_id]['components'][c_id].text" 
                            @text_changed="text_changed"
                            @slot_changed="slot_changed"
                            @signal_changed="signal_changed" />
                    </div>
                    <div v-if="slides[curr_slide_id]['components'][c_id].type_name === 'Circle'">
                        <Property :index="index" :c_id="c_id" :s_id="curr_slide_id" :type="'Circle'"
                            @slot_changed="slot_changed"
                            @signal_changed="signal_changed" />
                    </div>
                    <div v-if="slides[curr_slide_id]['components'][c_id].type_name === 'Rectangle'">
                        <Property :index="index" :c_id="c_id" :s_id="curr_slide_id" :type="'Rectangle'"
                            @slot_changed="slot_changed"
                            @signal_changed="signal_changed" />
                    </div>
                    <div v-if="slides[curr_slide_id]['components'][c_id].type_name === 'Slider'">
                        <Property :index="index" :c_id="c_id" :s_id="curr_slide_id" :type="'Slider'"
                            @slot_changed="slot_changed"
                            @signal_changed="signal_changed" />
                    </div>
                </v-list-item-content>
            </v-list-item>
        </v-list>
        <v-btn
            v-if="validSlotsSignals()"
            color="primary"
            @click="addConnection()"
            >
            Connect
        </v-btn>
    </v-navigation-drawer>

    <v-app-bar app clipped-left clipped-right permanent>

        <v-toolbar-title>Huddle (Slide:{{ curr_slide_id }}, Role: {{role}}) </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="rectangle" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd">
                    <v-icon>mdi-square</v-icon>
                </v-btn>
            </template>
            <span>New Rectangle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="circle" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd">
                    <v-icon>mdi-circle</v-icon>
                </v-btn>
             </template>
             <span>New Circle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="textbox" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd">
                    <v-icon>mdi-format-textbox</v-icon>
                </v-btn>
             </template>
             <span>New Textbox</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="slider" draggable v-on:dragstart="dragStart" v-on:dragend="dragEnd">
                    <v-icon>mdi-textbox</v-icon>
                </v-btn>
             </template>
             <span>New Slider</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="append_slide">
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
    </v-app-bar>

    <div class="pa-5">
        <v-fade-transition appear>
            <v-card id ="graph-wrapper" :width="w" :height="h" v-on:dragover="dragOver">
                <fullscreen ref="fullscreen" @change="fullscreenChange" background=#FFF>
                    <Textbox v-if="preview !== null && preview.constructor.name == 'Textbox'"
                        :x="w * preview.x" :y="h * preview.y" :text="preview.text" :style="style"/>
                    <MyCircle v-else-if="preview !== null && preview.constructor.name == 'Circle'" 
                        :x="w * preview.x" :y="h * preview.y" :r="preview.r" :style="style"/>
                    <MyRect v-else-if="preview !== null && preview.constructor.name == 'Rectangle'" 
                        :x="w * preview.x" :y="h * preview.y" :w="preview.w" :l="preview.l" :style="style"/>
                    <Slider v-else-if="preview !== null && preview.constructor.name == 'Slider'" 
                        :x="w * preview.x" :y="h * preview.y" :value="preview.value" :style="style"/>
                  <!-- TODO: fix empty list error, check slides.length before accessing component -->
                    <div v-for="c in slides[curr_slide_id].components" :key="c.c_id">
                        <div v-if="c.type_name === 'Textbox'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Textbox :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :text="c.text" 
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name === 'Circle'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyCircle :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :r="c.r" 
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name == 'Rectangle'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyRect :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :w="c.w" :l="c.l" 
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name == 'Slider'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Slider :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :value="c.value" 
                                @value_changed="value_changed" :style="style"/>
                        </div>
                    </div>
                </fullscreen>
            </v-card>
        </v-fade-transition>
    </div>

    </v-app>
</template>

<script>
import Slide from '@/components/app/Slide';
import PermissionModal from '@/components/app/PermissionModal';
import {mapState, mapMutations} from 'vuex';
import fullscreen from 'vue-fullscreen';
import Vue from 'vue';
import Property from '../components/properties/Property.vue';
import Textbox from '../components/widgets/Textbox.vue';
import Circle from '../components/widgets/Circle.vue';
import Rect from '../components/widgets/Rect.vue';
import Slider from '../components/widgets/Slider.vue'
import {Widget, Circle as CircleWidget, Rectangle as RectWidget, 
        Textbox as TextWidget, Slider as SliderWidget} from '../models/widget.js';

Vue.use(fullscreen);

export default {
    name: 'Workspace',    
    data: () => ({
        curr_room_id: '',
        curr_slide_id: 0,
        fullscreen: false,
        scale: 1,
        fields: [],
        count: 0,

        selected_widgets: [],
        selected_slot: {},
        selected_signal: {},

        // Dragging elements state
        preview: null,
        w: screen.width * 0.7,
        h: screen.height * 0.7
        
    }),
    created() {
    },
    beforeMount () {
        const params = {
            uid: this.$store.getters.uid,
            room: this.$store.getters.room,
            sid: this.$store.getters.sid
        }
        
        this.$socket.emit('join', params)
        this.$socket.emit('get_share_state', params)
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
        update_slide(id) {
            this.curr_slide_id = id;
            this.selected_widgets = [];
            this.selected_slot = {};
            this.selected_signal = {};
        },
        append_slide() {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
            }
            this.$socket.emit('new_slide', params)
        },
        // Signals
        value_changed: function (value) {
            const s_id = value.s_id
            const c_id0 = value.c_id
            const v = value.value
            const signal = value.signal

            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: s_id,
                c_id: c_id0,
                changes: {"value": v}
            }
            this.$socket.emit('update_component_id', params)
            const connections = this.slides[s_id]["connections"]
            const components = this.slides[s_id]["components"]
            if (c_id0 in connections && signal in connections[c_id0])
            {
                const slots = connections[c_id0][signal];
                for (var i = 0; i < slots.length; i++) {
                    const [c_id1, slot] = slots[i];

                    if (c_id1 in components) {
                        const widget = components[c_id1].type_name;
                        const params1 = {
                            uid: this.$store.getters.uid,
                            room: this.$store.getters.room,
                            s_id: s_id,
                            c_id: c_id1,
                            changes: Widget.mapSlot(widget, slot, [v])
                        }
                        this.$socket.emit('update_component_id', params1)
                    }
                }
            }
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
        signal_changed: function(value) {
            this.selected_signal = value;
            console.log(this.selected_signal);
        },
        slot_changed: function(value) {
            this.selected_slot = value;
            console.log(this.selected_slot);
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
                this.preview = new CircleWidget(-1, this.curr_slide_id, 0, 0, 25)
            } else if (widget === 'rectangle') {
                this.preview = new RectWidget(-1, this.curr_slide_id, 0, 0, 50, 50)
            } else if (widget === 'slider') {
                this.preview = new SliderWidget(-1, this.curr_slide_id, 0, 0, 50)
            } else {
                this.preview = null;
            }
        },
        dragOver:function(event) {
            event.preventDefault();
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
            if (s_id === this.curr_slide_id) {
                var selected = this.selected_widgets.find(element => element === c_id);
                if (selected === undefined) {
                    if (this.selected_widgets.length > 1) {
                        this.selected_widgets.shift();
                    }
                    this.selected_widgets.push(c_id);
                }
            }
        },
        addConnection() {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: this.curr_slide_id,
                c_id0: this.selected_signal.c_id,
                c_id1: this.selected_slot.c_id,
                signal: this.selected_signal.signal,
                slot: this.selected_slot.slot
            }
            this.$socket.emit('new_connection', params)
        },
        validSlotsSignals() {
            var valid_signal = Object.keys(this.selected_signal).length != 0;
            var valid_slot = Object.keys(this.selected_slot).length != 0;
            return this.selected_widgets.length == 2 && valid_signal && valid_slot;
        }
    },
    components: {
        Slide,
        Textbox,
        'MyCircle': Circle,
        'MyRect': Rect,
        Slider,
        PermissionModal,
        Property
    },
    computed: {
        ...mapState(['workspace']),
        ...mapState('ws', ['role', 'slides']),
        style () {
            return {
                transform: 'scale(' + this.scale + ')',
                transformOrigin: 'top left'
            }
        }
    }
}
</script>
