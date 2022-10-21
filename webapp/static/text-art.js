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
        hex: '#274dca',
        name: 'Blue 2'
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
        hex: '#FF000F',
        name: 'Red 2'
    },
    {
        hex: '#01A252',
        name: 'Green'
    },
    {
        hex: '#18E000',
        name: 'Green 2'
    },
    {
        hex: '#FDED02',
        name: 'Yellow'
    },
    {
        hex: '#ff0883',
        name: 'Pink'
    },

    // 2 colors
    {
        hex: ['#08FF83', '#01A0E4'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#08FF83', '#F7941D'],
        name: '',
        type: 'horizontal'
    },


    // 3 colors
    {
        hex: ['#00AEEF', '#FF0099', '#FFD500'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#FF0099', '#00AEEF', '#00A651'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#FF0099', '#00AEEF', '#FFD500'],
        name: '',
        type: 'horizontal'
    },

    // 4 colors
    {
        hex: ['#FF0099', '#00AEEF', '#00A651', '#FFD500'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#1eff8e', '#ffb900', '#fd5ff1', '#00a0e4'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#FF0099', '#00AEEF', '#00A651', '#FFD500', '#DB2D20'],
        name: '',
        type: 'horizontal'
    },
    {
        hex: ['#FF6480', '#CE33C0', '#8E44AD', '#2980B9', '#00A0E4'],
        name: '',
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

function setMultilineColor(colors, type=null) {
    var lines = TEXT_ART.split('\n');
    // remove last line if its empty
    if (lines[lines.length - 1] === '') {
        lines.pop();
    }

    var totalLines = 0;
    lines.forEach(line => {
        if(line.trim() !== '') {
            totalLines++;
        }
    });

    var colorsCount = colors.length;

    var linesPerColor = Math.floor(totalLines / colorsCount);
    var linesLeft = totalLines - (linesPerColor * colorsCount);

    var colorLines = {}
    colors.forEach(function (color, index) {
        colorLines[index] = linesPerColor;
    });

    for (var i = 0; i < linesLeft; i++) {
        colorLines[i] += 1;
    }

    var output = '';
    var colorIndex = 0;

    lines.forEach(function (line) {
        if (colorLines[colorIndex] == 0) {
            colorIndex++;
        }

        if (line.trim() !== '') {
            colorLines[colorIndex]--;
        }


        output += `<span style="color: ${colors[colorIndex]}">${line}</span>\n`;
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
    if (color.indexOf(',') > -1) {
        var colors = color.split(',');
        setMultilineColor(colors);
    } else {
        var textArtContainer = document.querySelector('.text-art');
        textArtContainer.style.color = color;
    }
}

function downloadArt() {
    var artContainer = document.querySelector('.ascii-art');
    html2canvas(artContainer).then(canvas => {
        document.body.appendChild(canvas);
        var link = document.createElement('a');
        link.download = 'text-art.png';
        link.href = canvas.toDataURL();
        link.click();

        document.body.removeChild(canvas);

    });
}

document.querySelector('.wrapper-dropdown').addEventListener('click', toggleDropdown);


document.querySelector("#background-color").addEventListener('input', () => {
    document.querySelector('.ascii-art').style.backgroundColor = document.querySelector("#background-color").value;
})