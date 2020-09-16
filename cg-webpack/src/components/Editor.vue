<template>
    <div class="Editor">
        <div id="menu"></div>
        <div id="container">
            <div class="box" v-bind:key="buffer.key" v-for="buffer in buffers">
              <editor v-model="buffers[buffer]" ref="editwins" @init="editorInit" lang="python" theme="chrome"></editor>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Editor',
  data () {
    return {
      buffers: [
        {id: 0, text: 'hello'},
        {id: 1, text: 'hello'}
      ],
      content: 'Hello'
    }
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/theme/monokai')
      require('brace/theme/chrome')
    }
  },
  components: {
    editor: require('vue2-ace-editor')
  },
  mounted () {
    console.log(this.$refs)
    this.windows = this.$refs.editwins
    this.windows[0].editor.setReadOnly(true)
    for (var i = 0; i < this.windows.length; i++) {
      this.windows[i].setReadOnly(true)
    }
  }
}

</script>

<style scoped>

.ace_editor {
  border: solid 2px black;
}

#menu {
  height: 10vh;
  border: solid 2px;
}

.box {
  padding: 1px;
}

#container {
    display: grid;
    width: 98%;
    height: 85vh;
    margin: 0px auto;

    grid-template-columns: repeat(3, 1fr);
}

</style>
