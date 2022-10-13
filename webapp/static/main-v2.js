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

