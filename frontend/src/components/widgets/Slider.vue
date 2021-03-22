<template>
<div class="absolute slider-length" :style="style">
    <v-slider dense max="100" min="0" :value="value" @input="value_changed($event)"></v-slider>
</div>
</template>

<script>
export default {
    name: 'SliderWidget',
    props: {
        c_id: {
            type: String
        },
        s_id: {
            type: String
        },
        x: {
            type: Number
        },
        y: {
            type: Number
        },
        value: {
            type: Number
        },
        glow: {
            type: Boolean
        },
        glow_color: {
            type: String
        },
        focus: {
            type: Boolean
        }
    },
    methods: {
        value_changed(event) {
            this.$emit('value_changed', {c_id: this.c_id, s_id: this.s_id, value: event, signal: 0})
        }
    },
    computed: {
        style () {
            var base = {
                top: this.y + 'px', 
                left: this.x + 'px', 
                lineHeight: 0
            }
            if (this.glow) {
                base.boxShadow = '0px 0px 20px 5px ' + this.glow_color
            }
            if (this.focus) {
                base.border = '3px dashed green'
            }
            return base
        }
    }
}
</script>

<style scoped>
.absolute {
    position: absolute;
}

.slider-length {
    width: 175px
}
</style>