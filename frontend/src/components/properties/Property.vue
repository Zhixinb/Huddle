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
    <v-text-field v-if="type=='Circle' || type=='Rectangle' || type=='Textbox' || type=='Slider' "
        v-model="prop.x"
        label="X"
        v-on:input="prop_changed('x', Number($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Circle' || type=='Rectangle' || type=='Textbox' || type=='Slider' "
        v-model="prop.y"
        label="Y"
        v-on:input="prop_changed('y', Number($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Circle'"
        v-model="prop.radius"
        label="Radius"
        v-on:input="prop_changed('radius', Number($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Rectangle'"
        v-model="prop.width"
        label="Width"
        v-on:input="prop_changed('width', Number($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Rectangle'"
        v-model="prop.length"
        label="Length"
        v-on:input="prop_changed('length', Number($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Textbox'"
        v-model="prop.text"
        label="Text"
        v-on:input="prop_changed('text', String($event))"
    ></v-text-field>
    <v-text-field v-if="type=='Slider'"
        v-model="prop.value"
        label="Value"
        v-on:input="prop_changed('value', Number($event))"
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
        p: Object,
        items: Array
    },
    data() {
        return { 
            prop: this.p,
            selectedSlot: '',
            selectedSignal: ''
        }
    },
    methods: {
        prop_changed(key, value) {
            this.$emit('property_changed', {c_id: this.c_id, s_id: this.s_id, key: key, value: value})
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