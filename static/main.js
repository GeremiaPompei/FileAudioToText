const app = Vue.createApp({
    data() {
        return {
            text: [''],
            loadingMex: '',
            loadingIndex: 0,
            file: undefined
        }
    },
    methods: {
        load(i) {
            var elem = document.getElementById("myBar");
            elem.style.width = i + "%";
            this.loadingIndex = i;
        },
        async submit() {
            if(this.file && this.file.type.includes('video')) {
                try {
                    setTimeout(function(){},3000); // Timer 3 sec
                    this.load(0);
                    var sum = 30;
                    this.text = [''];
                    this.loadingMex = 'Uploading video...';
                    var data = new FormData();
                    data.append('document', this.file);
                    var res = await fetch('/api/upload-video', {method: 'POST',body: data});
                    var json = await res.json();
                    var name = json.name;
                    var duration = json.duration;
                    for(var index=0; index<duration; index+=sum) {
                        this.load(parseInt(index/duration*100));
                        var load = '[ '+index+' / '+duration+' seconds ]...';
                        this.loadingMex = 'Splitting video '+load;
                        var data0 = new FormData();
                        data0.append('name', name);
                        data0.append('index',index.toString());
                        var res = await fetch('/api/split-video', {method: 'POST',body: data0});
                        var val = await res.blob();
                        this.loadingMex = 'Video to audio conversion '+load;
                        var data1 = new FormData();
                        data1.append('document', val);
                        var res2 = await fetch('/api/video-to-audio', {method: 'POST',body: data1});
                        var f = await res2.blob();
                        this.loadingMex = 'Audio to text conversion '+load;
                        var data2 = new FormData();
                        data2.append('document', f);
                        var res3 = await fetch('/api/audio-to-text', {method: 'POST',body: data2});
                        var val3 = await res3.json();
                        this.text[index/sum] = val3.text;
                        this.loadingMex = '';
                    }
                    this.load(100);
                }catch(e) {
                    this.text.push('Operation failed: ['+e.toString()+']');
                    this.loadingMex = '';
                }
                var data4 = new FormData();
                data4.append('name', name.toString());
                fetch('/api/remove-video', {method: 'POST',body: data4});
            }
        },
        processFile() {
            this.file = this.$refs.myFiles.files[0];
        }
    },
    computed: {
        uriTxt() {
            return encodeURIComponent(this.txt);
        },
        txt() {
            return this.text.reduce((x,y)=>x+' '+y);
        }
    }
});