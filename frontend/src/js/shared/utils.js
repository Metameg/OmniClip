

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
    // const path = '/%252Fhome%252Fwicker%252FOmniClip-Dev%252FOmniClip%252Fapp%252Ftools%252F..%252Ftemp%252Fguest/glow_480p(1).mp4';

    // Decode the URL-encoded path
    const decodedPath = decodeURIComponent(paths);
    const mimeType = mime.getType(decodedPath);

    if (mimeType && mimeType.startsWith('video/')) {
        return true; 
    }
    console.log('MIME type:', mimeType);

    return false;
}

export {enableFromCheckbox, notEnableFromCheckbox, updateHiddenBln, contains_video}