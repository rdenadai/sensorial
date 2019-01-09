const app = new Vue({
    el: '#app',
    data: {
        drawer: null
    },
    delimiters: ['[[',']]'],
    methods: {
        empty(event) {
            
        }
    },
    mounted: function () {
        this.empty();
    },
    created() {
        this.$vuetify.theme.primary = '#009688';
        this.$vuetify.theme.secondary = '#607d8b';
        this.$vuetify.theme.accent = '#8bc34a';
        this.$vuetify.theme.error = '#f44336';
        this.$vuetify.theme.warning = '#ffeb3b';
        this.$vuetify.theme.info = '#2196f3';
        this.$vuetify.theme.success = '#4caf50';
    }
});
