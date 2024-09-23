

function enableFromCheckbox (checkbox, dropdown) {
    checkbox.addEventListener('change', function () {
        dropdown.disabled = !checkbox.checked;
    });
}

function notEnableFromCheckbox (checkbox, dropdown) {
    checkbox.addEventListener('change', function () {
        dropdown.disabled = checkbox.checked;
    });
}

function updateHiddenBln (hiddenElement, checkboxElement) {
    checkboxElement.addEventListener('change', function() {
        hiddenElement.value = checkboxElement.checked ? 'true' : 'false';
    });
}

function contains_video(paths) {
    const mime = require('mime');

    // Decode the URL-encoded path
    for (let path of paths) {
        var decodedPath = decodeURIComponent(path);
        var mimeType = mime.getType(decodedPath);

        if (mimeType && mimeType.startsWith('video/')) {
            return true; 
        }
    };

    return false;
}

export {enableFromCheckbox, notEnableFromCheckbox, updateHiddenBln, contains_video}