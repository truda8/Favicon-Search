const getBase64OfFile = (file, callback) => {
    const fr = new FileReader();
    fr.addEventListener("load", (e) => {
        if (typeof callback === "function") {
            callback(fr.result);
        }
    });
    fr.readAsDataURL(file);
};

Notiflix.Loading.Init({
    messageColor: "#7784ff",
    svgColor: "#636cff",
    messageFontSize: "18px",
});
Notiflix.Report.Init({
    messageFontSize: "18px",
});

Notiflix.Notify.Init({
    fontSize: "16px",
});

axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';

new Vue({
    el: "#panel",
    data: {
        isUrl: false,
        showList: false,
        favicon_url: "",
        result: [],
        upload_image: "static/images/images.svg",
        file: { name: "Drag & Drag your image here", size: null },
        copy_text: "",
    },
    methods: {
        search() {
            let data = new Object();
            let upload_image = this.upload_image;
            let favicon_url = this.favicon_url;
            if (this.isUrl) {
                if (favicon_url) {
                    data = { favicon_url: favicon_url };
                } else {
                    Notiflix.Report.Failure(
                        "Search Failure",
                        "Please enter favicon link.",
                        "OK"
                    );
                }
            } else {
                if (upload_image.indexOf("base64") != -1) {
                    data = { upload_image: upload_image };
                } else {
                    Notiflix.Report.Failure(
                        "Search Failure",
                        "No favicon image selected.",
                        "OK"
                    );
                }
            }
            this.search_request(data);
        },
        tab_switch(tab_name) {
            this.showList = false;
            if (tab_name == "upload") {
                this.isUrl = false;
            } else {
                this.isUrl = true;
            }
        },
        response_error(msg) {
            Notiflix.Loading.Remove();
            Notiflix.Report.Failure("Search Failure", msg, "OK");
        },
        search_request(data) {
            Notiflix.Loading.Hourglass("Search Loading...");
            let _this = this;
            axios
                .post("/api/search", data)
                .then(function(response) {
                    Notiflix.Loading.Remove();
                    if (response.status == 200) {
                        let data = response.data;
                        console.log(data);
                        if (data.status == 200) {  // Successful
                            _this.result = data.urls;
                            if (data.urls.length !== 0) { // Has content
                                _this.showList = true;
                                Notiflix.Notify.Success('Search successful!');
                            } else {
                                Notiflix.Report.Warning('Search complete', 'Sorry, no matching favicon was found.', 'OK');
                            }
                        } else {
                            _this.response_error(data.msg);
                        }
                    } else {
                        _this.response_error("Request error.");
                    }
                })
                .catch(function (error) {
                    _this.response_error(error);
                });
        },
        set_base64(base64) {
            this.upload_image = base64;
        },
        addFile(file) {
            if (!file) {
                return;
            }
            if (file.type.indexOf("image") == -1) {
                Notiflix.Report.Failure("Failure", "Not a picture", "OK");
                return false;
            }
            this.file = file;
            getBase64OfFile(file, this.set_base64);
        },
        dragImg(e) {
            let file = e.dataTransfer.files[0];
            this.addFile(file);
        },
        choiceImg() {
            this.$refs.filElem.dispatchEvent(new MouseEvent("click"));
        },
        getFile(event) {
            let file = event.target.files[0];
            this.addFile(file);
        },
        comeBack() {
            this.showList = false;
        },
        copyText(text) {
            this.$copyText(text).then(
                () => {
                    Notiflix.Notify.Success('Copy successfully!');
                },
                () => {
                    Notiflix.Notify.Failure('Copy failed!');
                }
            );
        },
        linkDownload(link) {
            window.open(link, '_blank');
        }
    },
});
