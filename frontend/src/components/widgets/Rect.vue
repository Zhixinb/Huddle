<template>
<div class="absolute" :width="width" :height="length" 
    :style="style">
    <svg :width="width" :height="length">
        <rect :width="width" :height="length" :fill="'rgb(' + rgba.r + ',' + rgba.g + ',' + rgba.b + ')'" :fill-opacity="rgba.a"/>
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
                lineHeight: 0
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

.slider-length {
    width: 175px
}
</style>