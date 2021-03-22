<template>
    <div class="absolute" :style="style">
        {{text}}
    </div>
</template>

<script>


export default {
    name: 'TextWidget',
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
        text: {
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
                left: this.x + 'px'
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
