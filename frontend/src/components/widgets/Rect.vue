<template>
<div class="absolute" :width="width" :height="length" 
    :style="style">
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
        glow: {
            type: Boolean
        },
        glow_color: {
            type: String
        }
    },
    computed: {
        style () {
            if (this.glow) {
                return {
                    top: this.y + 'px', 
                    left: this.x + 'px', 
                    lineHeight: 0, 
                    boxShadow: '0px 0px 20px 5px ' + this.glow_color
                }
            } else {
                return {
                    top: this.y + 'px', 
                    left: this.x + 'px', 
                    lineHeight: 0, 
                }
            }
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