<template>
<div>
    <div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
        <svg width="100" height="100">
            <rect :width="width" :height="length" fill="blue" />
        </svg>
    </div>
    <div class="absolute" :style="{'top': y - 25 + 'px', 'left': x + 150 + 'px'}">
        <v-slider dense v-model="length" max="100" min="1" vertical></v-slider>
    </div>
    <div class="absolute slider-length" :style="{'top': y -65 + 'px', 'left': x - 45 + 'px'}">
        <v-slider dense v-model="width" max="100" min="1"></v-slider>
    </div>
</div>
</template>

<script>
export default {
    name: 'Rect',
    props: {
        x: {
            type: Number,
        },
        y: {
            type: Number
        },
        w: {
            type: Number,
        },
        l: {
            type: Number
        },
    },
    data() {
        return { 
            width: this.w,
            length: this.l
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