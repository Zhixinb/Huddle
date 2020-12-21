<template>
    <div class="absolute" :style="{'top': y + 'px', 'left': x + 'px'}">
        {{text}}
    </div>
</template>

<script>
import Vue from 'vue';


export default {
    name: 'TextWidget',
    props: {
        x: Number,
        y: Number,
        text: String,
        type_name: {
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