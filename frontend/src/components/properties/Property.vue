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
        :items="signals"
        label="Signals"
        @change="selected_signal($event)"
    ></v-select>
    <v-select v-else
        v-model="selectedSlot"
        :items="slots"
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
        t: String
    },
    data() {
        return { 
            text: this.t,
            slots: [],
            signals: [],
            selectedSlot: '',
            selectedSignal: ''
        }
    },
    mounted() {
        this.signals = Object.keys(Widget.signals[this.type]);
        this.slots = Object.keys(Widget.slots[this.type]);
    },
    methods: {
        text_changed(event) {
            console.log(this.slots);
            console.log(this.signals);
            this.$emit('text_changed', {c_id: this.c_id, s_id: this.s_id, text: event})
        },
        selected_signal(event) {
            this.$emit('signal_changed', event)
        },
        selected_slot(event) {
            this.$emit('slot_changed', event)
        }
    }

}
</script>