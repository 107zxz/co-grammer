<template>
    <div class="Editor">
        <div id="menu" class="error" v-if="buffers.length === 0">
          <h1 id="warning">Cannot connect to server or no buffers present!</h1>
        </div>
        <div id="container">
            <div class="box" :key="buffer.id" v-for="buffer in buffers">
              <div :class="{ error: buffer.flagged == true, header: true }">
                <div style="flex-grow: 1">{{ buffer.name }}</div>
                <button v-on:click="buffer.flagged = !buffer.flagged; syncBuffer(buffer.id)" v-if="buffer.id == uid"><i class="material-icons">flag</i></button>
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
      currentBuff: 0,
      userName: '',
      uid: -1
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
      // Update each buffer
      for (var i = 0; i < json.buffers.length; i++) {
        // If pulled buffer is more recent
        if (json.buffers[i].lastModified && json.buffers[i].lastModified > this.buffers[i].lastModified) {
          // Update each field individually for vue.js to update correctly
          this.buffers[i].text = json.buffers[i].text
          this.buffers[i].lastModified = json.buffers[i].lastModified
          this.buffers[i].name = json.buffers[i].name
          this.buffers[i].flagged = json.buffers[i].flagged
        }
        this.buffers[i].buildMessage = json.buffers[i].buildMessage
      }
    },
    async getBuffers () {
      await this.axios.post('http://localhost:5000/querybuff', {}).then((response) => {
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
        console.log('Buffers:')
        console.log(this.buffers)
        console.log('ID: ' + id.toString())
        this.buffers[id]['lastModified'] = Date.now()
        options = {buffer: this.buffers[id]}
      }

      console.log(options)

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
    },

    async promptInput () {
      var nameInput = ''
      while (nameInput.length === 0) {
        nameInput = window.prompt('Username:', '')
      }
      this.userName = nameInput

      // Pull buffers from server first
      await this.getBuffers()

      console.log(this.buffers.length)

      // Add another buffer based on user input
      this.buffers.push({id: this.buffers.length, text: '', buildMessage: '', lastModified: 1, name: nameInput, flagged: false})
      // Set a UID equal to the buffer's index, this allows the flagging system to work
      this.uid = this.buffers.length - 1

      this.syncBuffer(this.buffers.length - 1)
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

    this.promptInput()
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
  height: 95vh;
  margin: 0px auto;

  grid-template-columns: repeat(3, 1fr);
}

#warning {
  text-align: center;
  width: 100%;
  height: 100%;
}

</style>
