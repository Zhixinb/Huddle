<template>
<div>
    <v-btn :style="{'position': 'absolute', 'top': 0, 'left': 0}"
        color="error"
        plain
        small
        @click="deselect()"
    >
        <v-icon dark>
            mdi-close-thick
        </v-icon>
    </v-btn>
    <h3 :style="{'color': index === 0 ? 'steelblue' : 'red'}">{{type}}</h3>
    <v-text-field v-if="type=='Textbox'"
        v-model="text"
        label="Text"
        v-on:input="text_changed($event)"
    ></v-text-field>
    <v-select v-if="index === 0"
        v-model="selectedSignal"
        :items="items"
        label="Signals"
        @change="selected_signal($event)"
    ></v-select>
    <v-select v-else
        v-model="selectedSlot"
        :items="items"
        label="Slots"
        @change="selected_slot($event)"
        
    ></v-select>
</div>
</template>

<script>

export default {
    name: 'Property',
    props: {
        index: Number,
        type: String,
        c_id: String,
        s_id: String,
        t: String,
        items: Array
    },
    data() {
        return { 
            text: this.t,
            selectedSlot: '',
            selectedSignal: ''
        }
    },
    methods: {
        text_changed(event) {
            this.$emit('text_changed', {c_id: this.c_id, s_id: this.s_id, text: event})
        },
        selected_signal(event) {
            this.$emit('signal_changed', event)
        },
        selected_slot(event) {
            this.$emit('slot_changed', event)
        },
        deselect() {
            this.$emit('deselect_clicked', this.index)
        }
    }

}
</script>