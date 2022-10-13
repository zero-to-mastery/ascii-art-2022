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
const textInput = document.querySelector('#text');
const asciiArt = document.querySelector('.ascii-art');

if(textInput) {
    textInput.addEventListener('input', (e) => {
        const text = e.target.value;
        fetch('/v2/text/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text
            })
        }).then(res => res.json())
            .then(data => {
                asciiArt.innerHTML = data.art;
            })
    })
}
