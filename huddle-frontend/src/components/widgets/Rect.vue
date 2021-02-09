<template>
<div>
    <div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
        <svg width="100" height="100">
            <rect :width="w" :height="l" fill="blue" />
        </svg>
    </div>
</div>
</template>

<script>
export default {
    name: 'RectWidget',
    props: {
        c_id: {
            type: Number
        },
        s_id: {
            type: Number
        },
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