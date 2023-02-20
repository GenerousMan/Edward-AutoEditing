<template>
  <div id="app">
    <transition name="fade" mode="out-in" :duration="300">
      <router-view @loading="loading" @cancelLoading="cancelLoading"></router-view>
    </transition>
    <transition name="fade">
      <Loading :msg="msg" v-if="loadingShow"/>
    </transition>
  </div>
</template>

<script>
import Loading from './components/Loading.vue'
export default {
  name: 'App',
  data: () => {
    return {
      msg: '',
      loadingShow: false
    }
  },
  components: {
      Loading
  },
  methods: {
    loading(msg) {
      this.msg = msg;
      this.loadingShow = true;
    },
    cancelLoading() {
      this.loadingShow = false;
    }
  }
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
  overflow-y: scroll;
  background: rgb(27, 27, 27);
}

html, body {
  background: rgb(27, 27, 27);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

<style>
::-webkit-scrollbar{
    width: 12px;
    height: 12px;
    /* background-color: #ccc; */
    background-color: rgb(27, 27, 27);
}
/*滚动条的轨道*/
::-webkit-scrollbar-track{
    /* box-shadow: inset 0 0 5px rgba(0,0,0,.3); */
    /* background-color: rgb(0, 0, 0); */
}
/*滚动条的滑块按钮*/
::-webkit-scrollbar-thumb{
    border-radius: 10px;
    background-color: white;
    /* box-shadow: inset 0 0 5px #000; */
}
/*滚动条的上下两端的按钮*/
::-webkit-scrollbar-button{
    height: 0px;
    width: 0px;
    /* background-color: #333; */
}
</style>