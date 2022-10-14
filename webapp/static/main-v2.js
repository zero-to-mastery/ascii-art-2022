/*******************************/
/* 1) Homepage - Image upload */
/*****************************/

var uploadBtn = document.getElementById("uploadBtn");
var uploadFile = document.getElementById("formFile");
if (uploadBtn) {
    uploadBtn.addEventListener("click", function () {
        uploadFile.click();
    });
    
    uploadFile.addEventListener("change", function () {
        document.getElementById("uploadForm").submit();
    });
    
    var dropZone = document.getElementById("dropZone");
    dropZone.addEventListener("dragover", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add("dragover");
    });
    
    dropZone.addEventListener("drop", function (e) {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove("dragover");
        var file = e.dataTransfer.files[0];
        uploadFile.files = e.dataTransfer.files;
        document.getElementById("uploadForm").submit();
    });
}


/*****************************/
/* 2) Gallery - Delete file */
/***************************/

const deleteBtns = document.querySelectorAll('.delete-btn');
const deleteForm = document.querySelector('#deleteForm');
const imageId = document.querySelector('#imageId');

deleteBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault();
        const imageName = btn.getAttribute('data-name');
        imageId.value = imageName;
        deleteForm.submit();
    })
});



/***************************/
/* 3) Text Art - Generate */
/*************************/
const textSettingsForm = document.querySelector('#settingsForm');
const asciiArt = document.querySelector('.ascii-art');
var TEXT_ART = asciiArt.innerText;

if(textSettingsForm) {
    textSettingsForm.addEventListener('input', (e) => {
        const text = e.target.value;
        var data = new FormData(textSettingsForm);

        fetch('/v2/text/generate', {
            method: 'POST',
            body: data
        }).then(res => res.json())
            .then(data => {
                asciiArt.innerHTML = data.art;
                TEXT_ART = data.art;
            })
    })
}
