const app = Vue.createApp({
    data() {
        return {
            txt: '',
            file: undefined,
            loading: false
        }
    },
    methods: {
        submit() {
            if(this.file){
                this.loading = true;
                var data = new FormData();
                data.append('document', this.file);
                fetch('/api/upload', {method: 'POST',body: data})
                .then(res=>res.json())
                .catch(e => {
                    this.txt = 'Error!';
                    this.loading = false;
                })
                .then(val=>{
                    this.txt = val.text;
                    this.loading = false;
                });
            }
        },
        processFile() {
            this.file = this.$refs.myFiles.files[0];
        }
    },
    computed: {
        uriTxt() {
            return encodeURIComponent(this.txt);
        }
    }
});