<template>
<div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
    <svg :width="radius*2" :height="radius*2">
        <circle :cx="radius" :cy="radius" :r="radius" fill="blue" />
    </svg>
</div>
</template>

<script>
export default {
    name: 'CircleWidget',
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
        radius: {
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
</style>