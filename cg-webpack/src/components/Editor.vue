<template>
    <div class="Editor">
        <div id="menu">
          <button :key="buffer.id" v-for="buffer in buffers" :id="'s' + (buffer.id + 1)" v-on:click="syncBuffer">Sync Buffer {{buffer.id}}</button>
        </div>
        <div id="container">
            <div class="box" :key="buffer.id" v-for="buffer in buffers">
              <editor v-model="buffers[buffer.id]['text']" ref="editwins" @init="editorInit" lang="python" theme="chrome"></editor>
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
        {id: 0, text: 'Hello'},
        {id: 1, text: 'Goodbye'}
      ]
    }
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/theme/monokai')
      require('brace/theme/chrome')
    },

    syncBuffer: function (event) {
      var options = []

      if (event) {
        console.log(event.target.innerHTML)
        if (event.target.id === 's1') {
          options = {buffer: this.buffers[0]}
        }
        if (event.target.id === 's2') {
          options = {buffer: this.buffers[1]}
        }
      }

      this.axios.post('http://localhost:5000/json', options).then((response) => {
        console.log(response)
        this.buffers = response.data.buffers
      })
    }
  },
  components: {
    editor: require('vue2-ace-editor'),
    axios: require('axios')
  },
  mounted () {
    this.windows = this.$refs.editwins
    this.syncBuffer()
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
