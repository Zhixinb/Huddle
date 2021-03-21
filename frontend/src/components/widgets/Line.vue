<template>
<div class="absolute" :style="{'top': Math.min(y0, y1) - 10 + 'px', 'left': Math.min(x0, x1) - 10 + 'px', 'line-height': 0}">
    <svg :width="20 + (x1 > x0 ? x1 - x0 : x0 - x1)" :height="20 + (y1 > y0 ? y1 - y0 : y0 - y1)">
        <linearGradient id="grad" gradientUnits="userSpaceOnUse"
            :x1="10 + (x1 > x0 ? 0: x0 - x1)" 
            :y1="10 + (y1 > y0 ? 0: y0 - y1)" 
            :x2="10 + (x1 > x0 ? x1 - x0 : 0)" 
            :y2="10 + (y1 > y0 ? y1 - y0 : 0)">
            <stop stop-color="steelblue" offset="0" />
            <stop stop-color="red" offset="1" />
        </linearGradient>
        <line 
            :x1="10 + (x1 > x0 ? 0: x0 - x1)" 
            :y1="10 + (y1 > y0 ? 0: y0 - y1)" 
            :x2="10 + (x1 > x0 ? x1 - x0 : 0)" 
            :y2="10 + (y1 > y0 ? y1 - y0 : 0)" 
            stroke="url(#grad)" stroke-width="2" stroke-dasharray="6 12"/>
    </svg>
</div>
</template>

<script>
export default {
    name: 'LineWidget',
    props: {
        c_id: {
            type: String
        },
        s_id: {
            type: String
        },
        x0: {
            type: Number
        },
        y0: {
            type: Number
        },
        x1: {
            type: Number
        },
        y1: {
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