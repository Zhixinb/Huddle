<template>
    <v-text-field
        v-model="t"
        label="Text"
        placeholder="Placeholder"
    ></v-text-field>
</template>

<script>

export default {
    name: 'TextboxProperty',
    props: {
        t: String
    },
    data() {
        return { text: this.t }
    }
}
</script>