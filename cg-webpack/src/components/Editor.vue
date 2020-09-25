<template>
    <div class="Editor">
        <div id="menu" :class="{ error: buffers.length === 0 }">
          <h1 id="warning" v-if="buffers.length === 0">Cannot connect to server or no buffers present!</h1>
        </div>
        <div id="container">
            <div class="box" :key="buffer.id" v-for="buffer in buffers">
              <div class="header">
                <div>Buffer {{ buffer.id + 1 }}</div>
                <button v-on:click="buildBuffer(buffer.id)" style="padding: 0"><i class="material-icons">play_arrow</i></button>
              </div>
              <editor v-on:click="currentBuff=buffer.id" v-on:input="syncBuffer(buffer.id)" v-model="buffers[buffer.id]['text']" ref="editwins" @init="editorInit" lang="python" theme="chrome"></editor>
              <span :id="'b' + buffer.id" class="build">{{buffer.buildMessage}}</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Editor',
  data () {
    return {
      buffers: [],
      currentBuff: 0
    }
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/theme/monokai')
      require('brace/theme/chrome')
    },

    // Update buffers from returned json
    updateBuffers (json) {
      for (var i = 0; i < json.buffers.length; i++) {
        if (json.buffers[i].lastModified && json.buffers[i].lastModified > this.buffers[i].lastModified) {
          this.buffers[i].text = json.buffers[i].text
          this.buffers[i].lastModified = json.buffers[i].lastModified
        }
        this.buffers[i].buildMessage = json.buffers[i].buildMessage
      }
    },
    getBuffers () {
      this.axios.post('http://localhost:5000/buffers', {}).then((response) => {
        if (this.buffers.length === response.data.buffers.length) {
          this.updateBuffers(response.data)
        } else {
          this.buffers = response.data.buffers
        }

      // this.buffers = response.data.buffers
      }).catch(e => {
        this.buffers = []
      })
    },

    syncBuffer (id) {
      var options = []

      this.currentBuff = id

      if (typeof id !== 'undefined' && id !== -1) {
        this.buffers[id]['lastModified'] = Date.now()
        options = {buffer: this.buffers[id]}
      }

      this.axios.post('http://localhost:5000/buffers', options).then((response) => {
        this.updateBuffers(response.data)
      }).catch(e => {
        this.buffers = []
      })
    },

    buildBuffer (id) {
      var options = {buffer: this.buffers[id]}

      console.log(options['code'])

      // Send buffer to server with a special type of request
      this.axios.post('http://localhost:5000/build', options).then((response) => {
        console.log(response.data)
        this.updateBuffers(response.data)

        var buildView = document.getElementById('b' + id.toString())
        buildView.scrollTop = buildView.scrollHeight
      }).catch(e => {
        this.buffers = []
      })
    }
  },
  components: {
    editor: require('vue2-ace-editor'),
    axios: require('axios')
  },
  mounted () {
    this.windows = this.$refs.editwins
    this.getBuffers()

    setInterval(() => {
      this.getBuffers()
    }, 1000)
  }
}

</script>

<style scoped>

#menu {
  height: 80px;
  border: solid 2px;
}

.header {
  background-color: #f2f2f2;
  height: 24px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.error {
  background-color: red;
}

.build {
  height: 45%;
  padding: 5px;
  border-top: 2px solid black;
  white-space: pre-line;
  overflow: scroll;
  max-height: 45vh;
}

.box {
  padding: 1px;
  border: 2px solid black;
  display: flex;
  flex-direction: column;
}

#container {
  display: grid;
  width: 98%;
  height: 85vh;
  margin: 0px auto;

  grid-template-columns: repeat(3, 1fr);
}

#warning {
  text-align: center;
  width: 100%;
  height: 100%;
}

</style>
