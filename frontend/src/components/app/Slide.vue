<template>
    <v-fade-transition appear>
        <div class="pa-2">
            <v-card id="preview" width=100% :height='h'>
                <div>
                    <div v-for="c in slides[id].components" :key="c.c_id">
                        <div v-if="c.type_name === 'Textbox'">
                            <Textbox :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :text="c.text" 
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name === 'Circle'">
                            <MyCircle :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :radius="c.radius" :rgba="c.rgba"
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name == 'Rectangle'">
                            <MyRect :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :width="c.width" :length="c.length" :rgba="c.rgba"
                                :style="style"/>
                        </div>
                        <div v-else-if="c.type_name == 'Slider'">
                            <Slider :c_id="c.c_id" :s_id="c.s_id" :x="w * c.x" :y="h * c.y" :value="c.value"
                                :style="style"/>
                        </div>
                    </div>
                </div>
            </v-card>
        </div>
    </v-fade-transition>
</template>

<script>
import Textbox from '../widgets/Textbox.vue';
import Circle from '../widgets/Circle.vue';
import Rect from '../widgets/Rect.vue';
import Slider from '../widgets/Slider.vue'
import {mapState} from 'vuex';
export default {
    name: 'slide',
    data: () => ({
        w: 208,
        h: 117,
        scale: 1
    }),
    props: {
        id: {
            type: String
        }
    },
    mounted() {
        const rect = document.getElementById('preview').getBoundingClientRect()
        this.w = rect.width
        this.h = this.w * screen.height / screen.width
        this.scale = this.w / screen.width / 0.7
    },
    components: {
        Textbox,
        'MyCircle': Circle,
        'MyRect': Rect,
        Slider,
    },
    computed: {
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
