<template>
  <div class="text-center">
    <v-dialog
      v-model="dialog"
      width="1000"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
          class='ma-1'
          block
        >
          Edit Text
        </v-btn>
      </template>

      <v-card >
        <v-card-title class="headline grey lighten-2">
          Text Editor
        </v-card-title>
        <v-container fill-height fluid align="center">
            <v-card-text  align="center">      
                <div class="quill-editor-container">
                    <quill-editor
                    class="editor"
                    ref="myTextEditor"
                    :value="content"
                    :options="editorOption"
                    @change="onEditorChange"
                    @blur="onEditorBlur($event)"
                    @focus="onEditorFocus($event)"
                    @ready="onEditorReady($event)"
                    />                    
                </div>
            </v-card-text>
        </v-container>       

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="dialog = false"
          >
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>

  import hljs from 'highlight.js'
  import debounce from 'lodash/debounce'
  import { quillEditor } from 'vue-quill-editor'
  // highlight.js style
  import 'highlight.js/styles/tomorrow.css'
  // import theme style
  import 'quill/dist/quill.core.css'
  import 'quill/dist/quill.snow.css'
  export default {
    name: 'quill-editor-container-snow',
    components: {
      quillEditor
    },
    props: {     
        textContent: {
            type: String
        }
    },
    data() {
      return {
        dialog: false,        
        editorOption: {
          modules: {
            toolbar: [
              ['bold', 'italic', 'underline', 'strike'],
              ['blockquote', 'code-block'],
              [{ 'header': 1 }, { 'header': 2 }],
              [{ 'list': 'ordered' }, { 'list': 'bullet' }],
              [{ 'script': 'sub' }, { 'script': 'super' }],
              [{ 'indent': '-1' }, { 'indent': '+1' }],
              [{ 'direction': 'rtl' }],
              [{ 'size': ['small', false, 'large', 'huge'] }],
              [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
              [{ 'font': [] }],
              [{ 'color': [] }, { 'background': [] }],
              [{ 'align': [] }],
              ['clean'],
              ['link', 'image', 'video']
            ],
            syntax: {
              highlight: text => hljs.highlightAuto(text).value
            }
          }
        },
        content: this.textContent
      }
    },
    methods: {
      onEditorChange: debounce(function(value) {
        this.content = value.html
        this.$emit('property_changed', this.content)
      }, 466),
      onEditorBlur(editor) {
        // console.log('editor blur!', editor)
      },
      onEditorFocus(editor) {
        // console.log('editor focus!', editor)
      },
      onEditorReady(editor) {
        // console.log('editor ready!', editor)
      }
    },
    computed: {
      contentCode() {
        return hljs.highlightAuto(this.content).value
      }
    }
  }
</script>

<style lang="css" scoped>
.quill-editor-container {
    display: flex;
    flex-direction: column;
}
.quill-editor-container .editor {
    height: 40rem;
    overflow: hidden;
}
</style>