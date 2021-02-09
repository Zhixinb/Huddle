<template>
<div>
    <div class="absolute slider-length" :style="{'top': y + 'px', 'left': x + 'px'}">
        <v-slider dense max="100" min="0" :value="value" @change="value_changed($event)"></v-slider>
    </div>
</div>
</template>

<script>
export default {
    name: 'SliderWidget',
    props: {
        c_id: {
            type: Number
        },
        s_id: {
            type: Number
        },
        x: {
            type: Number
        },
        y: {
            type: Number
        },
        value: {
            type: Number
        }
    },
    methods: {
        value_changed(event) {
            this.$emit('value_changed', {c_id: this.c_id, s_id: this.s_id, value: event})
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