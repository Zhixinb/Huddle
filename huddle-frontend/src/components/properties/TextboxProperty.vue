<template>
    <v-text-field
        v-model="text"
        label="Text"
        @change="text_changed($event)"
    ></v-text-field>
</template>

<script>
export default {
    name: 'TextboxProperty',
    props: {
        t: String,
        c_id: Number,
        s_id: Number
    },
    data() {
        return { text: this.t }
    },
    methods: {
        text_changed(event) {
            this.$emit('text_changed', {c_id: this.c_id, s_id: this.s_id, text: event})
        }
    }
}
</script>