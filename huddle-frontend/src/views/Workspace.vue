<template>
    <div>
    <v-navigation-drawer app>
        <v-list-item v-for="s in slides" :key="s.id" link @click.stop="update_slide(s.id)">
            <v-list-item-content>
                <slide :message="s.id"> </slide>
            </v-list-item-content>
        </v-list-item>
    </v-navigation-drawer>

    <v-app-bar app>

        <v-toolbar-title>Huddle: {{ curr_slide_id }} </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" draggable @dragend="new_rect($event)">
                    <v-icon>mdi-square</v-icon>
                </v-btn>
             </template>
             <span>New Rectangle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" draggable @dragend="new_circle($event)">
                    <v-icon>mdi-circle</v-icon>
                </v-btn>
             </template>
             <span>New Circle</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="textbox" draggable @dragstart="onDragStart($event)" @dragend="onDragEnd()">
                    <v-icon>mdi-textbox</v-icon>
                </v-btn>
             </template>
             <span>New Textbox</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="append_slide">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
             </template>
             <span>New Slide</span>
        </v-tooltip>
        <button type="button" @click="toggle" >Fullscreen</button>
    </v-app-bar>

    <div class="pa-5">
        <v-fade-transition appear>
            <v-card id ="graph-wrapper" :width="w*0.7" :height="h*0.7" @dragover="onHover($event)" 
            @drop="onDrop($event)">
                <fullscreen ref="fullscreen" @change="fullscreenChange" background=#FFF>
                    <textbox v-if="dragged === 'textbox'" :width="w*0.7" :height="h*0.7" :x="x" :y="y" />
                    <div v-for="c in slides[curr_slide_id].components" :key="c.c_id">
                        <div v-if="c.type == 'circle'">
                            <MyCircle :x="c.x" :y="c.y" :r="c.y"/>
                        </div>
                        <div v-else-if="c.type == 'rect'">
                            <MyRect :x="c.x" :y="c.y" :w="c.w" :l="c.l"/>
                        </div>
                    </div>
                </fullscreen>
            </v-card>
        </v-fade-transition>
    </div>

    </div>
</template>

<script>
import Slide from '@/components/app/Slide';
import {mapState, mapMutations} from 'vuex'
import fullscreen from 'vue-fullscreen';
import Vue from 'vue';
import Textbox from '../components/app/Textbox.vue';
import Circle from '../components/widgets/Circle.vue';
import Rect from '../components/widgets/Rect.vue';
Vue.use(fullscreen);

export default {
    name: 'Workspace',
    data: () => ({
        curr_slide_id: 0,
        next_c_id: 0,
        next_s_id: 1,
        slides: [
            { id: 0, components: [] }
        ],
        fullscreen: false,
        fields: [],
        count: 0,
        curr_room_id: '',

        // Dragging elements state
        dragged: '',
        x: 0,
        y: 0,
        w: window.innerWidth,
        h: window.innerHeight
    }),
    created() {
        window.addEventListener("resize", this.screenChange);
        this.parse_slide(0);
    },
    beforeMount () {
        const params = {
            uid: this.$store.getters.uid,
            room: this.$route.params.room
        }
        this.set_room(this.room_id)
        this.$socket.emit('join', params)
    },
    beforeDestroy () {
        const params = {
            uid: this.$store.getters.uid,
            room: this.workspace.workspace_id
        }
        this.$socket.emit('leave', params)
    },
    destroyed() {
        window.removeEventListener("resize", this.screenChange);
    },
    methods:
    {
        ...mapMutations(['set_room']),
        parse_slide (id) {
            var curr_slide = this.slides[id];
            var components = curr_slide.components;
            for (var i = 0; i < components.length; i++) {
                console.log(components[i]);
            }
        },
        clear () {
            this.components[0].data.text_content = 'qqqqqqq'
        },
        update_slide(id) {
            this.curr_slide_id = id;
        },
        append_slide() {
            this.slides.push({ id: this.next_s_id, components: [] });
            this.curr_slide_id = this.next_s_id;
            this.next_s_id += 1;
        },
        new_circle(event) {
            const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
            var x = event.x - pos.x;
            var y = event.y - pos.y;
            var c = { c_id: this.next_c_id, type: 'circle', x: x, y: y, r: 25 };
            this.slides[this.curr_slide_id].components.push(c);
            this.next_c_id += 1;
        },
        new_rect(event) {
            const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
            var x = event.x - pos.x;
            var y = event.y - pos.y;
            var c = { c_id: this.next_c_id, type: 'rect', x: x, y: y, w: 50, l: 50 };
            this.slides[this.curr_slide_id].components.push(c);
            this.next_c_id += 1;
        },
        toggle() 
        {
            this.$refs['fullscreen'].toggle()
        },
        fullscreenChange(fullscreen) {
            this.fullscreen = fullscreen
        },
        onDragStart(event) {
            event.dataTransfer.setDragImage(document.createElement('div'), 0, 0);
            this.dragged = event.target.id;
        },
        onDragEnd() {
            this.dragged = '';
        },
        onHover(event) {
            event.preventDefault();
            const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
            if (event.x <= pos.right && event.y <= pos.bottom && event.x >= pos.left && event.y >= pos.top) {
                this.x = event.x - pos.x;
                this.y = event.y - pos.y;
            }
        },
        onDrop (event) {
        },
        screenChange(event) {
            this.w = window.innerWidth;
            this.h = window.innerHeight;
        }
    },
    components: {
        Slide,
        Textbox,
        'MyCircle': Circle,
        'MyRect': Rect
    },
    computed: {
        ...mapState(['workspace'])
    }
}
</script>
