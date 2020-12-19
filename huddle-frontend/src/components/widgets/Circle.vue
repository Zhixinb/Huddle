<template>
<div>
    <div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
        <svg width="100" height="100">
            <circle cx="50" cy="50" :r="radius" fill="blue" />
        </svg>
    </div>
    <div class="absolute" :style="{'top': y - 25 + 'px', 'left': x + 150 + 'px'}">
        <v-slider dense v-model="radius" max="50" min="1" vertical @input="emit_radius"></v-slider>
    </div>
</div>
</template>

<script>
export default {
    name: 'Circle',
    props: {
        c_id: {
            type: Number
        },
        x: {
            type: Number
        },
        y: {
            type: Number
        },
        r: {
            type: Number
        },
    },
    methods: {
        emit_radius() {
            this.$emit('update_radius', { c_id: this.c_id, r: this.radius })
        }
    },
    data() {
        return { radius: this.r }
    }
}
</script>

<style scoped>
.absolute {
    position: absolute;
}
</style>