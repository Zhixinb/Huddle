<template>
<div class="absolute" :width="width" :height="length" 
    :style="style">
    <img :width="width" :height="length" :src="src" />
</div>
</template>

<script>
export default {
    name: 'ImageWidget',
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
        src: {
            type: String
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