<template>
<div class="absolute" :style="{'top': Math.min(y0, y1) - 10 + 'px', 'left': Math.min(x0, x1) - 10 + 'px', 'line-height': 0}">
    <svg :width="20 + (x1 > x0 ? x1 - x0 : x0 - x1)" :height="20 + (y1 > y0 ? y1 - y0 : y0 - y1)">
        <linearGradient :id="`grad${index}`"  gradientUnits="userSpaceOnUse"
            :x1="10 + (x1 > x0 ? 0: x0 - x1)" 
            :y1="10 + (y1 > y0 ? 0: y0 - y1)" 
            :x2="10 + (x1 > x0 ? x1 - x0 : 0)" 
            :y2="10 + (y1 > y0 ? y1 - y0 : 0)">
            <stop stop-color="steelblue" offset="0" />
            <stop stop-color="red" offset="1" />
        </linearGradient>
        <!-- uncomment for arrow -->
        <!-- <marker id="pointer" markerWidth="10" markerHeight="8" 
            refX="10" refY="3.5" orient="auto" markerUnits="userSpaceOnUse">
            <polyline points="0 0, 10 3.5, 0 7" 
                :style="{'fill': 'none', 'stroke': 'red', 'vector-effect': 'non-scaling-stroke', 'stroke-width': '2'}"/>
        </marker> -->
        <line 
            :x1="10 + (x1 > x0 ? 0: x0 - x1)" 
            :y1="10 + (y1 > y0 ? 0: y0 - y1)" 
            :x2="10 + (x1 > x0 ? x1 - x0 : 0)" 
            :y2="10 + (y1 > y0 ? y1 - y0 : 0)" 
            :stroke="`url(#grad${index})`" stroke-width="2" stroke-dasharray="6 12" marker-end="url(#pointer)"/>
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
        index: {
            type: Number
        }
    }
}
</script>

<style scoped>
.absolute {
    position: absolute;
}
</style>