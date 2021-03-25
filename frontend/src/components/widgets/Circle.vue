<template>
<div class="absolute" :style="style">
        <svg :width="radius*2" :height="radius*2">
            <circle :cx="radius" :cy="radius" :r="radius" :fill="'rgb(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ')'" :fill-opacity="rgba.a"/>
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
        glow: {
            type: Boolean
        },
        glow_color: {
            type: String
        },
        focus: {
            type: Boolean
        },
        rgba: {
            type: Object
        }
    },
    computed: {
        style () {
            var base = {
                top: this.y + 'px', 
                left: this.x + 'px', 
                lineHeight: 0,
                borderRadius: '50%'
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
</style>