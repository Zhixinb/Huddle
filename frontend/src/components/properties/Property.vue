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
        c_id: Number,
        s_id: Number,
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
            this.slots = TextWidget.slots.map(element => element[0]);
            this.signals = TextWidget.signals;
        } else if (this.type === 'Circle') {
            this.slots = CircleWidget.slots.map(element => element[0]);
            this.signals = CircleWidget.signals;
        } else if (this.type === 'Rectangle') {
            this.slots = RectWidget.slots.map(element => element[0]);
            this.signals = RectWidget.signals;
        } else if (this.type === 'Slider') {
            this.slots = SliderWidget.slots.map(element => element[0]);
            this.signals = SliderWidget.signals;
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
            var signal_id = this.signals.indexOf(this.selectedSignal);
            if (signal_id != -1) {
                this.$emit('signal_changed', {c_id: this.c_id, s_id: this.s_id, signal: signal_id})
            } else {
                console.log('Signal ID error');
            }
        },
        selected_slot(event) {
            var slot_id = this.slots.indexOf(this.selectedSlot);
            if (slot_id != -1) {
            this.$emit('slot_changed', {c_id: this.c_id, s_id: this.s_id, slot: slot_id})
            } else {
                console.log('Slot ID error');
            }
        }
    }

}
</script>