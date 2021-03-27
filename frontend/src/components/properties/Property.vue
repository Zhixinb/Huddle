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

    <v-expansion-panels accordion multiple>
        <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header> Position </v-expansion-panel-header>
            <v-expansion-panel-content>
                <v-text-field v-if="type=='Circle' || type=='Rectangle' || type=='Image' || type=='Textbox' || type=='Slider' "
                    v-model="prop.x"
                    label="X"
                    v-on:input="property_changed('x', Number($event))"
                ></v-text-field>
                <v-text-field v-if="type=='Circle' || type=='Rectangle' || type=='Image' ||  type=='Textbox' || type=='Slider' "
                    v-model="prop.y"
                    label="Y"
                    v-on:input="property_changed('y', Number($event))"
                ></v-text-field>
            </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel class="elevation-0">
            <v-expansion-panel-header> Properties </v-expansion-panel-header>
            <v-expansion-panel-content>                
                <v-text-field v-if="type=='Circle'"
                    v-model="prop.radius"
                    label="Radius"
                    v-on:input="property_changed('radius', Number($event))"
                ></v-text-field>
                <v-text-field v-if="type=='Rectangle' || type=='Image'"
                    v-model="prop.width"
                    label="Width"
                    v-on:input="property_changed('width', Number($event))"
                ></v-text-field>
                <v-text-field v-if="type=='Rectangle' || type=='Image'"
                    v-model="prop.length"
                    label="Length"
                    v-on:input="property_changed('length', Number($event))"
                ></v-text-field>

                <text-editor-modal v-if="type=='Textbox'" :textContent="prop.text"
                @property_changed="property_changed('text', String($event))"/>
                
                <v-text-field v-if="type=='Slider'"
                    v-model="prop.value"
                    label="Value"
                    v-on:input="property_changed('value', Number($event))"
                ></v-text-field>

                <color-picker-modal v-if="type=='Rectangle' || type=='Circle'" :rgba="prop.rgba"
                @property_changed="property_changed('rgba', $event)" />
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
    

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
import ColorPickerModal from '../app/ColorPickerModal.vue'
import TextEditorModal from '../app/TextEditorModal.vue'

export default {
    name: 'Property',
    components: {
        ColorPickerModal,
        TextEditorModal
    },
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
        property_changed(key, value) {
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
        },
        colorPicker(currColor) {
            this.$emit('open_editor', {editor: "colorPicker", c_id: this.c_id, s_id: this.s_id, rgba:currColor})
        }
    }

}
</script>