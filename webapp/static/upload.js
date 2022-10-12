var uploadBtn = document.getElementById("uploadBtn");
var uploadFile = document.getElementById("formFile");
uploadBtn.addEventListener("click", function () {
    uploadFile.click();
});

// when the file is selected, upload it
uploadFile.addEventListener("change", function () {
    document.getElementById("uploadForm").submit();
});

// when the file is dragged
var dropZone = document.getElementById("dropZone");
dropZone.addEventListener("dragover", function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.add("dragover");
});

// when the file is dropped
dropZone.addEventListener("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    dropZone.classList.remove("dragover");
    var file = e.dataTransfer.files[0];
    uploadFile.files = e.dataTransfer.files;
    document.getElementById("uploadForm").submit();
});