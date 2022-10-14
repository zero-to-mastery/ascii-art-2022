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
    },
    {
        hex: ['#00AEEF', '#FF0099', '#FFD500'],
        name: 'B P Y',
        type: 'horizontal'
    },
    {
        hex: ['#FF0099', '#00AEEF', '#00A651'],
        name: 'P B G',
        type: 'horizontal'
    }
];

var dropdown = document.getElementById('color-picker-dropdown');
var colorPreview = document.getElementById('color-preview');
var colorPreviewName = document.getElementById('color-preview-name');
var colorInput = document.querySelector('input[name="color"]');
var dropdownOpen = false;

colors.forEach(function (color) {
    var li = document.createElement('li');
    li.dataset.color = color.hex;
    if (color.type) {
        li.dataset.type = color.type;
    }
    if (Array.isArray(color.hex)) {
        var output = '';
        color.hex.forEach(function (hex) {
            output += `<span class="color-multiple" style="background-color: ${hex}"></span>`;
        });

        output += `${color.name}`
        li.innerHTML = output;
    } else {
        li.innerHTML = '<span style="background: ' + color.hex + '"></span> ' + color.name;

    }


    li.addEventListener('click', function () {
        output = '';
        if (color.type) {
            color.hex.forEach(function (hex) {
                console.log(hex);
                output += `<span class="color-multiple" style="background-color: ${hex}"></span>`;
            });

            colorPreview.innerHTML = output;

            setMultilineColor(color.hex, color.type);

        } else {
            var textArtContainer = document.querySelector('.text-art');
            textArtContainer.innerHTML = TEXT_ART;
            textArtContainer.style.color = color.hex;
            colorPreview.innerHTML = `<span style="background: ${color.hex}"></span>`;
        }
        colorInput.value = color.hex;
        colorPreviewName.innerHTML = color.name;
        dropdownOpen = false;
        toggleDropdown();
        // updateColor();
    });

    dropdown.appendChild(li);
});

function setMultilineColor(colors, type) {
    var lines = TEXT_ART.split('\n');
    var total = lines.length;
    var colorsCount = colors.length;

    var linesPerColor = Math.floor(total / colorsCount);
    var linesLeft = total - (linesPerColor * colorsCount);

    var output = '';
    var colorIndex = 0;
    var linesCount = 0;
    lines.forEach(function (line) {
        if (linesCount >= linesPerColor) {
            linesCount = 0;
            linesLeft--;
            colorIndex++;
        }

        output += `<span style="color: ${colors[colorIndex]}">${line}</span>\n`;
        linesCount++;
    });

    var textArtContainer = document.querySelector('.text-art');
    textArtContainer.style.color = '';
    textArtContainer.innerHTML = output;

}

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

