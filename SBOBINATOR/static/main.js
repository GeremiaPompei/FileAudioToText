const app = Vue.createApp({
    data() {
        return {
            txt: '',
            loadingMex: '',
            file: undefined,
        }
    },
    methods: {
        submit() {
            if(this.file){
                this.loadingMex = 'Video to audio conversion...';
                var data = new FormData();
                data.append('document', this.file);
                fetch('/api/video-to-audio', {method: 'POST',body: data})
                .then(res=>res.blob())
                .catch(e => {
                    this.txt = '';
                    this.loadingMex = '';
                }).then(f => {
                    this.loadingMex = 'Audio to text conversion...';
                    var data2 = new FormData();
                    data2.append('document', f);
                    fetch('/api/audio-to-text', {method: 'POST',body: data2})
                    .then(res=>res.json())
                    .catch(e => {
                        this.txt = '';
                        this.loadingMex = '';
                    })
                    .then(val=>{
                        this.txt = val.text;
                        this.loadingMex = '';
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