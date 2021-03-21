<template>
<div class="absolute" :style="style">
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
                    borderRadius: '50%',
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
</style>