<template>
    <div>
    <v-navigation-drawer app>
        <v-list-item v-for="s in slides" :key="s.message" link @click.stop="update_slide(s.id)">
            <v-list-item-content>
                <slide :message="s.message"> </slide>
            </v-list-item-content>
        </v-list-item>
    </v-navigation-drawer>

    <v-app-bar app>

        <v-toolbar-title>Huddle: {{ curr_slide_id }} </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="textbox" draggable @dragstart="onDragStart($event)" @dragend="onDragEnd()">
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
                </fullscreen>
            </v-card>
        </v-fade-transition>
    </div>

    </div>
</template>

<script>
import Slide from '@/components/app/Slide';
import {mapState} from 'vuex';
import fullscreen from 'vue-fullscreen';
import Vue from 'vue';
import Textbox from '../components/app/Textbox.vue';
Vue.use(fullscreen);

export default {
    name: 'Workspace',
    data: () => ({
        curr_slide_id: 0,
        slides: [
            { id: 0, message: '0' }
        ],
        fullscreen: false,

        // Dragging elements state
        dragged: '',
        x: 0,
        y: 0,
        w: window.innerWidth,
        h: window.innerHeight
    }),
    created() {
        window.addEventListener("resize", this.screenChange);
    },
    destroyed() {
        window.removeEventListener("resize", this.screenChange);
    },
    methods:
    {
        update_slide(id) {
            this.curr_slide_id = id;
        },
        append_slide() {
            this.slides.push({ id: this.slides.length, message: this.slides.length });
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
        Textbox
    },
    computed: {
        ...mapState(['workspace'])
    }
}
</script>
