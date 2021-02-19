<template>
<div>
    <h3>{{type}}</h3>
    <v-text-field v-if="type=='Textbox'"
        v-model="text"
        label="Text"
        @change="text_changed($event)"
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
import {Widget} from '../../models/widget.js';

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
            console.log(event)
            this.$emit('slot_changed', event)
        }
    }

}
</script>