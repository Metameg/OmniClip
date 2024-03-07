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

export {enableFromCheckbox, notEnableFromCheckbox, updateHiddenBln}