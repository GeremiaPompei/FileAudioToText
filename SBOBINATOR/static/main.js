Vue.createApp({
    data: function() {
        return {
            txt: 'testoo',
            file: undefined
        }
    },
    method: {
        submit() {
            fetch('/api/upload', {method: 'POST',headers: {"Content-Type": "multipart/form-data"
              }, body: this.file})
            .then(res=>res.text())
            .then(val=>console.log(val));
        },
        processFile(event) {
            this.file = event.target.files[0];
            console.log(this.file);
        }
    }
}).mount('#app');