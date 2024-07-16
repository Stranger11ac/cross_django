// Functionamiento de TinyMCE #################################################################
const useDarkMode = window.matchMedia("(prefers-color-scheme: dark)").matches;
const uploadImageTiny = async (blobInfo, progress) => {
    try {
        const formData = new FormData();
        formData.append("file", blobInfo.blob(), blobInfo.filename());
        formData.append("csrfmiddlewaretoken", getCSRFToken());
        const response = await fetch("../../administracion/registrar_img_blog/", {
            method: "POST",
            body: formData,
            credentials: "include",
        });
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        const json = await response.json();
        if (!json || typeof json.location !== "string") {
            throw new Error("Al parecer esta peticion no esta Permitida");
        }
        return json.location;
    } catch (error) {
        console.error(error);
        return null;
    }
};

tinymce.init({
    selector: "#textTiny",
    language: "es_MX",
    branding: false,
    statusbar: false,
    resize: false,
    plugins:
        "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table wordcount quickbars image pagebreak autoresize autosave",
    mobile: {
        toolbar_mode: "sliding",
        autoresize_min_height: 300,
        min_height: 300,
    },
    menubar: false,
    contextmenu: "removeformat | bold italic underline | link image table | hr pagebreak",
    contextmenu_never_use_native: true,
    toolbar_mode: "wrap",
    toolbar:
        "undo redo | forecolor backcolor | styles | bold italic underline removeformat | alignleft aligncenter outdent indent | bullist numlist | table tabledelete | cut paste wordcount",
    quickbars_insert_toolbar: false,
    quickbars_selection_toolbar: "bold italic underline | blocks forecolor backcolor | quicklink blockquote",
    autoresize_min_height: 600,
    min_height: 600,
    promotion: false,
    skin: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "oxide",    
    content_css: window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "",   
});

tinymce.init({
    selector: "#mainTiny",
    language: "es_MX",
    branding: false,
    statusbar: false,
    resize: false,
    plugins:
        "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code fullscreen insertdatetime media table wordcount quickbars image pagebreak autoresize autosave",
    mobile: {
        menubar: true,
        toolbar_mode: "sliding",
        toolbar_sticky: true,
    },
    menubar: "file edit view format table",
    menu: {
        file: { title: "File", items: "restoredraft | preview | print" },
        view: { title: "View", items: "visualaid visualchars visualblocks | spellchecker | preview fullscreen" },
    },
    contextmenu: "removeformat | bold italic underline | link image table | hr pagebreak",
    contextmenu_never_use_native: true,
    toolbar_mode: "wrap", // wrap floating sliding
    toolbar_sticky: true,
    toolbar:
        "undo redo restoredraft | forecolor backcolor | fontfamily styles | bold italic underline removeformat | alignleft aligncenter alignright | alignjustify outdent indent | bullist numlist | table tabledelete | image gallerycustom | insertdatetime link unlink openlink | cut paste wordcount",
    quickbars_insert_toolbar: false,
    quickbars_selection_toolbar: "bold italic underline | blocks forecolor backcolor | quicklink blockquote",
    quickbars_image_toolbar: "image|alignleft aligncenter alignright | rotateleft rotateright | imageoptions",
    color_map: [
        "#ECCAFA","Light Purple",
        "#C2E0F4","Light Blue",
        "#BFEDD2","Light Green",
        "#FBEEB8","Light Yellow",
        "#F8CAC6","Light Red",
        "#B96AD9","Purple",
        "#3598DB","Blue",
        "#2DC26B","Green",
        "#F1C40F","Yellow",
        "#E03E2D","Red",
        "#843FA1","Dark Purple",
        "#3B71CA","Dark Blue",
        "#169179","Dark Turquoise",
        "#E67E23","Orange",
        "#BA372A","Dark Red",
        "#ECF0F1","Light Gray",
        "#CED4D9","Medium Gray",
        "#95A5A6","Gray",
        "#7E8C8D","Dark Gray",
        "#34495E","Navy Blue",
        "#000000","Black",
        "#ffffff","White",
    ],
    skin: (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "oxide"),
    content_css: (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : ""),
    image_title: true,
    automatic_uploads: true,
    // file_picker_types: "image",
    images_upload_url: "../../administracion/registrar_img_blog/",
    images_upload_handler: uploadImageTiny,
    min_height: 625,
    autoresize_min_height: 625,
    autosave_interval: "20m",
    promotion: false,
    insertdatetime_formats: ["%d-%m-%Y", "%Y-%m-%d", "%H:%M:%S", "%I:%M:%S %p"],
    content_style: `
        img.img-tiny {
            max-width: 100%;
            height: auto;
            border: none;
            border-radius: 10px;
            margin: 2px;
        }
    `,
    paste_data_images: true,

    setup: (editor) => {
        editor.ui.registry.addButton("gallerycustom", {
            icon: "gallery",
            onAction: function () {
                var cmsURL = "../../administracion/lista_imagenes/";
                window.open(cmsURL, "Seleccionar Imagen", "width=350,max-height=900");
            },
        });

        editor.on("paste", (event) => {
            const clipboardData = event.clipboardData || window.clipboardData;
            const items = clipboardData.items;
            for (const item of items) {
                if (item.kind === "file" && item.type.startsWith("image/")) {
                    event.preventDefault();
                    const file = item.getAsFile();
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = () => {
                        const blobInfo = editor.editorUpload.blobCache.create(file.name, file, reader.result);
                        editor.editorUpload.blobCache.add(blobInfo);

                        uploadImageTiny(blobInfo).then((url) => {
                            if (url) {
                                editor.insertContent(`<img src="${url}" class="img-tiny"/><p>&nbsp;</p>`);
                            }
                        });
                    };
                }
            }
        });

        editor.on("NodeChange", (event) => {
            const nodes = event.element.getElementsByTagName("img");
            for (const img of nodes) {
                img.classList.add("img-tiny");
            }
        });
    },
});
