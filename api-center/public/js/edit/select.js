new Vue({
    el: '#app',
    data: function() {
      return {
            activeIndex: '/edit'
        }
    },
    methods: {
        handleSelect(key) {
            window.location.href = key;
        },
        jump(url) {
            window.location.href = '/edit/' + url;
        }
    },
    mounted() {

    }
})