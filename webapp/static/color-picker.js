var colors = [
    {
        hex: '#FFFFFF',
        name: 'White'
    },
    {
        hex: '#01A0E4',
        name: 'Blue'
    },
    {
        hex: '#F7941D',
        name: 'Orange'
    },
    {
        hex: '#F67400',
        name: 'Orange 2'
    },
    {
        hex: '#DB2D20',
        name: 'Red'
    },
    {
        hex: '#01A252',
        name: 'Green'
    },
    {
        hex: '#FDED02',
        name: 'Yellow'
    }
];

var dropdown = document.getElementById('color-picker-dropdown');
var colorPreview = document.getElementById('color-preview-color');
var colorPreviewName = document.getElementById('color-preview-name');
var colorInput = document.querySelector('input[name="color"]');
var dropdownOpen = false;

colors.forEach(function (color) {
    var li = document.createElement('li');
    li.innerHTML = '<span style="background: ' + color.hex + '" data-color="' + color.hex + '"></span> ' + color.name;
    li.addEventListener('click', function () {
        colorPreview.style.background = color.hex;
        colorPreviewName.innerHTML = color.name;
        colorInput.value = color.hex;
        dropdown.style.display = 'none';
        dropdownOpen = false;
        toggleDropdown();
        updateColor();

    });
    dropdown.appendChild(li);
});

function toggleDropdown() {
    if (dropdownOpen) {
        dropdown.style.display = 'none';
        dropdownOpen = false;
    } else {
        dropdown.style.display = 'block';
        dropdownOpen = true;
    }
}

function updateColor() {
    var color = colorInput.value;
    var textArtContainer = document.querySelector('.text-art');
    textArtContainer.style.color = color;
}


document.querySelector('.wrapper-dropdown').addEventListener('click', toggleDropdown);

