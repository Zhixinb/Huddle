<template>
<div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
    <svg :width="width" :height="length">
        <rect :width="width" :height="length" fill="blue" />
    </svg>
</div>
</template>

<script>
export default {
    name: 'RectWidget',
    props: {
        c_id: {
            type: String
        },
        s_id: {
            type: String
        },
        x: {
            type: Number,
        },
        y: {
            type: Number
        },
        width: {
            type: Number,
        },
        length: {
            type: Number
        },
        type_name: {
            type: String
        },
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