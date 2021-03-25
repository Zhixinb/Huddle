<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          Edit Color
        </v-btn>
      </template>

      <v-card >
        <v-card-title class="headline grey lighten-2">
          Color Picker
        </v-card-title>
        <v-container fill-height fluid align="center">
            <v-card-text  align="center">      
                <v-color-picker
                    dot-size="25"
                    mode="rgba"
                    swatches-max-height="150"
                    v-model="color"
                ></v-color-picker>
            </v-card-text>
        </v-container>       

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="onClick"
          >
            Set Color
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
  export default {    
    props: {
        c_id: {
            type: String
        },
        s_id: {
            type: String
        },        
        rgba: {
            type: Object
        }
    },
    data () {
      return {
        dialog: false,
        color: this.rgba
      }
    },
    methods: {
        onClick() {
            this.dialog = false
            this.$emit('property_changed', this.color)
        }
    }
  }
</script>
