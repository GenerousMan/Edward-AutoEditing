new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/'
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        }
    },
    mounted() {

    }
})
