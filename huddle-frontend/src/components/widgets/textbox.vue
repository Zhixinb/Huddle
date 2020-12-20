<template>
  <div>
    <label>Text Box:</label>
    <input type="text"
    v-model="text_content"
    placeholder="Lorem ipsum dolor"
    @change="onChangeHandler"
    />
  </div>
</template>

<script>
export default {
  name: 'textbox',
  data: () => ({
    text_content: ''
  }),
  methods: {
    onChangeHandler () {
    // emit signal to server
      console.log('text content:' + this.text_content)
      this.$emit('changeInText', this.text_content)
    //   this.text_content = 'bbbbbbbbbbbbb'
    },
    onClear (data) {
      this.text_content = data
    },
    clear() {
      this.text_content = 'bbbb'
    }
  }
}
</script>

<style>

</style>
