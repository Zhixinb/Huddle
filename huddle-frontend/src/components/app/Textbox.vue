<template>
    <movable :bounds="{x:[0, width], y:[0, height]}" :posLeft="x" :posTop="y">
        <div>
            {{this.text}}
        </div>
    </movable>
</template>

<script>
import Vue from 'vue';
import movable from 'v-movable';
Vue.use(movable);

export default {
    name: 'textbox',
    props: ['width', 'height', 'x', 'y'],
    data: () => ({
        text: 'hello'
    })
}
</script>
