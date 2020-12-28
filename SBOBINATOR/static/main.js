const app = Vue.createApp({
    data() {
        return {
            txt: '',
            loadingMex: '',
            file: undefined,
        }
    },
    methods: {
        async submit() {
            const sum = 40;
            if(this.file) {
                var index = sum;
                this.txt = '';
                while(true) {
                    try {
                        this.loadingMex = 'Splitting video ['+index+']...';
                        var data = new FormData();
                        data.append('document', this.file);
                        data.append('index',index.toString());
                        var res = await fetch('/api/split-video', {method: 'POST',body: data});
                        var val = await res.blob();
                        index+=sum;
                        this.loadingMex = 'Video to audio conversion...';
                        var data1 = new FormData();
                        data1.append('document', val);
                        var res2 = await fetch('/api/video-to-audio', {method: 'POST',body: data1});
                        var f = await res2.blob();
                        this.loadingMex = 'Audio to text conversion...';
                        var data2 = new FormData();
                        data2.append('document', f);
                        var res3 = await fetch('/api/audio-to-text', {method: 'POST',body: data2});
                        var val3 = await res3.json();
                        if(val3.text == "Error!") {
                            this.loadingMex = '';
                            break;
                        }
                        this.txt += val3.text;
                        this.loadingMex = '';
                    }catch(e) {
                        console.log(e);
                        this.txt = '';
                        this.loadingMex = '';
                        break;
                    }
                }
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