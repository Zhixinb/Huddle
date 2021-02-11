<template>
    <v-app>
    
    <v-navigation-drawer app clipped>
        <v-list dense>
            <v-list-item v-for="s in slides" :key="s.id" link @click.stop="update_slide(s.id)">
                <v-list-item-content>
                    <slide :message="s.id"> </slide>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer app clipped right>
        <v-list>
            <v-list-item v-for="c_id in this.selected_widgets" :key="c_id" link>
                <v-list-item-content>
                    <div v-if="slides[curr_slide_id]['components'][c_id].type_name === 'Textbox'">
                        <TextboxProperty :t="slides[curr_slide_id]['components'][c_id].text" 
                            :c_id="c_id" :s_id="curr_slide_id" @text_changed="text_changed" />
                    </div>
                </v-list-item-content>
            </v-list-item>
         </v-list>
    </v-navigation-drawer>

    <v-app-bar app clipped-left clipped-right permanent>

        <v-toolbar-title>Huddle(Slide:{{ curr_slide_id }}, Role: {{role}}) </v-toolbar-title>
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
                        :x="w * preview.x" :y="h * preview.y" :text="preview.text"/>
                    <MyCircle v-else-if="preview !== null && preview.constructor.name == 'Circle'" 
                        :x="w * preview.x" :y="h * preview.y" :r="preview.r"/>
                    <MyRect v-else-if="preview !== null && preview.constructor.name == 'Rectangle'" 
                        :x="w * preview.x" :y="h * preview.y" :w="preview.w" :l="preview.l"/>
                    <Slider v-else-if="preview !== null && preview.constructor.name == 'Slider'" 
                        :x="w * preview.x" :y="h * preview.y" :value="preview.value"/>
                  <!-- TODO: fix empty list error, check slides.length before accessing component -->
                    <div v-for="c in slides[curr_slide_id].components" :key="c.c_id">
                        <div v-if="c.type_name === 'Textbox'" draggable v-on:click="widgetClicked($event, c.s_id, c.c_id)"
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Textbox :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :text="c.text" />
                        </div>
                        <div v-else-if="c.type_name === 'Circle'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyCircle :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :r="c.r"/>
                        </div>
                        <div v-else-if="c.type_name == 'Rectangle'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyRect :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :w="c.w" :l="c.l"/>
                        </div>
                        <div v-else-if="c.type_name == 'Slider'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Slider :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :value="c.value" @value_changed="value_changed"/>
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
import TextboxProperty from '../components/properties/TextboxProperty.vue';
import Textbox from '@/components/widgets/Textbox.vue';
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
        next_c_id: 0,
        next_s_id: 1,
        fullscreen: false,
        fields: [],
        count: 0,
        selected_widgets: [],

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
        },
        append_slide() {
            this.curr_slide_id = this.next_s_id;
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: this.next_s_id
            }
            this.$socket.emit('new_slide', params)
            this.next_s_id += 1;
        },
        // Signals
        value_changed: function (value) {
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: value.s_id,
                c_id: value.c_id,
                changes: {"value": value.value}
            }
            this.$socket.emit('update_component_id', params)
        },
        text_changed: function (value) {
            console.log("text change enter")
            const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                s_id: value.s_id,
                c_id: value.c_id,
                changes: {"text": value.text}
            }
            console.log('params')
            console.log(params)
            this.$socket.emit('update_component_id', params)
        },
        toggle() {
            this.$refs['fullscreen'].toggle()
        },
        fullscreenChange(full) {
            if (full) {
                this.w = screen.width;
                this.h = screen.height;
            } else {
                this.w = screen.width * 0.7;
                this.h = screen.height * 0.7;
            }
            this.fullscreen = full
        },
        dragStart:function(event) {
            event.dataTransfer.setDragImage(document.createElement('div'), 0, 0);
            const widget = event.target.id;
            if (widget === 'textbox') {
                this.preview = new TextWidget(this.next_c_id, this.curr_slide_id, 0, 0, "Text");
            } else if (widget === 'circle') {
                this.preview = new CircleWidget(this.next_c_id, this.curr_slide_id, 0, 0, 25)
            } else if (widget === 'rectangle') {
                this.preview = new RectWidget(this.next_c_id, this.curr_slide_id, 0, 0, 50, 50)
            } else if (widget === 'slider') {
                this.preview = new SliderWidget(this.next_c_id, this.curr_slide_id, 0, 0, 50)
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
                this.slides[this.curr_slide_id].components[this.preview.c_id] = this.preview;
                this.next_c_id += 1;
                const params = {
                    uid: this.$store.getters.uid,
                    room: this.$store.getters.room,
                    component: this.preview
                }
                this.$socket.emit('new_widget', params)
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
        }
    },
    components: {
        Slide,
        Textbox,
        TextboxProperty,
        'MyCircle': Circle,
        'MyRect': Rect,
        Slider,
        PermissionModal
    },
    computed: {
        ...mapState(['workspace']),
        ...mapState('ws', ['role', 'slides'])
    }
}
</script>
