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
        <permission-modal/>
        <button type="button" @click="toggle" >Fullscreen</button>
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
                  <div> {{slides[curr_slide_id].components}}</div>
                  <!-- TODO: fix empty list error, check slides.length before accessing component -->
                    <div v-for="c in slides[curr_slide_id].components" :key="c.c_id">
                        <div v-if="c.type_name === 'Textbox'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <Textbox :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :text="c.text"/>
                        </div>
                        <div v-else-if="c.type_name === 'Circle'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyCircle :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :r="c.r" @update_radius="update_radius"/>
                        </div>
                        <div v-else-if="c.type_name == 'Rectangle'" draggable 
                            v-on:dragstart="widgetDragStart($event, c)" v-on:dragend="widgetDragEnd($event, c)">
                            <MyRect :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :w="c.w" :l="c.l" @update_dimen="update_dimen"/>
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
import PermissionModal from '@/components/app/PermissionModal'
import {mapState, mapMutations} from 'vuex'
import fullscreen from 'vue-fullscreen';
import Vue from 'vue';
import Textbox from '@/components/widgets/Textbox.vue';
import Circle from '../components/widgets/Circle.vue';
import Rect from '../components/widgets/Rect.vue';
import {Widget, Circle as CircleWidget, Rectangle as RectWidget, Textbox as TextWidget} from '../models/widget.js';

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
        curr_room_id: '',

        // Dragging elements state
        preview: null,
        w: screen.width * 0.7,
        h: screen.height * 0.7
        
    }),
    watch: {
      // TODO FOR KEVIN: Synchronize on a per-delta basis rather than per-slide
      slides: {
        deep: true,
        handler(newState, oldState) {

          const params = {
            uid: this.$store.getters.uid,
            room: this.$route.params.room,
            new_state: newState
          }
          // console.log(params)
          this.$socket.emit('update_slides', params)
      }
      }
    },
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
            this.slides.push({ id: this.next_s_id, components: [] });
            this.curr_slide_id = this.next_s_id;
            this.next_s_id += 1;
        },
        new_circle(event) {
            const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
            if (event.x <= pos.right && event.y <= pos.bottom && event.x >= pos.left && event.y >= pos.top) {
                var x = event.x - pos.x;
                var y = event.y - pos.y;
                var widget = new CircleWidget(this.next_c_id, this.curr_slide_id, x, y, 25, 'Circle')
                this.slides[this.curr_slide_id].components.push(widget);
                this.next_c_id += 1;
            }
        },
        new_rect(event) {
            const pos = document.getElementById('graph-wrapper').getBoundingClientRect();
            if (event.x <= pos.right && event.y <= pos.bottom && event.x >= pos.left && event.y >= pos.top) {
                var x = event.x - pos.x;
                var y = event.y - pos.y;
                this.slides[this.curr_slide_id].components.push(new RectWidget(this.next_c_id, this.curr_slide_id, 
                    x, y, 50, 50, 'Rectangle'));
                this.next_c_id += 1;
            }
        },
        update_radius: function (value) {
            const params = {
              uid: this.$store.getters.uid,
              room: this.$store.getters.room,
              s_id: value.s_id,
              c_id: value.c_id,
              value: value.r,
              name: 'Circle'
            }
            this.$socket.emit('update_widget_state', params)
            //this.slides[this.curr_slide_id].components.find(x => x.c_id === value.c_id).r = value.r;
        },
        update_dimen: function (value) {
          const params = {
              uid: this.$store.getters.uid,
              room: this.$store.getters.room,
              s_id: value.s_id,
              c_id: value.c_id,
              w: value.w,
              l: value.l,
              name: 'Rectangle'
            }
            this.$socket.emit('update_widget_state', params)
            // var obj = this.slides[this.curr_slide_id].components.find(x => x.c_id === value.c_id);
            // obj.w = value.w;
            // obj.l = value.l;
        },
        toggle() 
        {
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
                this.preview = new TextWidget(this.next_c_id, this.curr_slide_id, 0, 0, "Text", "Textbox");
            } else if (widget === 'circle') {
                this.preview = new CircleWidget(this.next_c_id, this.curr_slide_id, 0, 0, 25, "Circle")
            } else if (widget === 'rectangle') {
                this.preview = new RectWidget(this.next_c_id, this.curr_slide_id, 0, 0, 50, 50, "Rectangle")
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
                this.slides[this.curr_slide_id].components.push(this.preview);
                this.next_c_id += 1;
                console.log("Signal: New Widget Created")
            }
            this.preview = null;
        },
        widgetDragStart:function(event, widget) {
            event.dataTransfer.setDragImage(document.createElement('div'), 0, 0);
            this.preview = widget.copy();
        },
        widgetDragEnd:function(event, widget) {
            widget.x = this.preview.x;
            widget.y = this.preview.y;
            this.preview = null;
            console.log("Signal: Widget moved")
        }
    },
    components: {
        Slide,
        Textbox,
        'MyCircle': Circle,
        'MyRect': Rect,
        PermissionModal
    },
    computed: {
        ...mapState(['workspace']),
        ...mapState('ws', ['role', 'slides'])
    }
}
</script>
