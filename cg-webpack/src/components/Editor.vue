<template>
    <div class="Editor">
        <div id="container">
            <div v-bind:key="i" v-for="i in ['11', '12', '21', '22']" :style="'grid-row: ' + i[0] + '; grid-column: ' + i[1]" class="box">
              <editor ref="editwins" @init="editorInit" lang="python" theme="monokai"></editor>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Editor',
  data () {
    return {
      windows: [0, 1, 2]
    }
  },
  methods: {
    editorInit: function () {
      require('brace/ext/language_tools')
      require('brace/mode/python')
      require('brace/theme/monokai')
    }
  },
  components: {
    editor: require('vue2-ace-editor')
  },
  mounted () {
    this.windows = this.$refs.editwins
    for (var i = 0; i < this.windows.length; i++) {
      this.windows[i].setReadOnly(true)
    }
  }
}

</script>

<style scoped>
* {
    display: inline-block;
}

#container {
    display: grid;
    width: 99vw;
    height: 98vh;
    text-align: center;
}

.box {
  padding: 1%;
}

</style>
