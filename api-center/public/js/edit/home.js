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
        begin() {
            window.location.href = '/edit/select'
        }
    },
    mounted() {

    }
})
