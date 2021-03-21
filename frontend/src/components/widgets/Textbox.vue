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
        }
    },
    computed: {
        style () {
            if (this.glow) {
                return {
                    top: this.y + 'px', 
                    left: this.x + 'px',
                    boxShadow: '0px 0px 20px 5px ' + this.glow_color
                }
            } else {
                return {
                    top: this.y + 'px', 
                    left: this.x + 'px'
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
