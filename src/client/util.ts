import Vue from 'vue';

export let UtilMixin = {
    methods: {
        linkto: function (pathname: string): string {
            // @ts-ignore
            return this.$router.push({ path: pathname })
        }
    }
}

export default { UtilMixin }