<template>
    <div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
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
        }
    }
}
</script>

<style scoped>
.absolute {
    position: absolute;
}
</style>
