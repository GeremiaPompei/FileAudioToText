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
                fetch('/api/video-to-audio', {method: 'POST',body: data})
                .then(res=>res.blob())
                .catch(e => {
                    this.txt = 'Error!';
                    this.loading = false;
                }).then(f => {
                    var data2 = new FormData();
                    data2.append('document', f);
                    fetch('/api/audio-to-text', {method: 'POST',body: data2})
                    .then(res=>res.json())
                    .catch(e => {
                        this.txt = 'Error!';
                        this.loading = false;
                    })
                    .then(val=>{
                        this.txt = val.text;
                        this.loading = false;
                    });
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