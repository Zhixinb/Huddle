<template>
     <v-list-item @click="download_json">
        <v-list-item-title>Download</v-list-item-title>
    </v-list-item>
</template>

<script>

import {mapState} from 'vuex'

export default {
    methods: {
        download_json() {
            var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(this.slides));
            var downloadAnchorNode = document.createElement('a');
            downloadAnchorNode.setAttribute("href",     dataStr);
            downloadAnchorNode.setAttribute("download", "slides_data.json");
            document.body.appendChild(downloadAnchorNode); // required for firefox
            downloadAnchorNode.click();
            downloadAnchorNode.remove();
        },
    },
    computed: {
        ...mapState(['workspace']),
        ...mapState('ws', ['role', 'slides', 'can_share']),
    },
}
</script>

<style>

</style>