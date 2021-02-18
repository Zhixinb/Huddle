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
import {Circle as CircleWidget, Rectangle as RectWidget, 
        Textbox as TextWidget, Slider as SliderWidget} from '../../models/widget.js';

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
        if (this.type === 'Textbox') {
            this.slots = Object.keys(TextWidget.slots);
            this.signals = Object.keys(TextWidget.signals);
        } else if (this.type === 'Circle') {
            this.slots = Object.keys(CircleWidget.slots);
            this.signals = Object.keys(CircleWidget.signals);
        } else if (this.type === 'Rectangle') {
            this.slots = Object.keys(RectWidget.slots);
            this.signals = Object.keys(RectWidget.signals);
        } else if (this.type === 'Slider') {
            this.slots = Object.keys(SliderWidget.slots);
            this.signals = Object.keys(SliderWidget.signals);
        } else {
            console.log('Error fetching slots and signals')
        }
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