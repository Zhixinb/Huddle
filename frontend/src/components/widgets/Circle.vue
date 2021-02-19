<template>
<div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
    <svg width="100" height="100">
        <circle cx="50" cy="50" :r="r" fill="blue" />
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
        r: {
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