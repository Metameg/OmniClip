const videoStylerUI = (function () {
    // Private Variables and Functions
    function updateVideoStylerListener(inputs, sampleText) {
        inputs.forEach(function(input) {
            input.addEventListener("input", function() { // Use "input" event for real-time updates
                updateVideoStyler(inputs, sampleText); // Call updateText() whenever any input changes
            });
        });
    }

    function updateVideoStyler(inputs, sampleText) {

        var fontName = inputs[0].value;
        var fontSize = inputs[1].value;
        var isBold = inputs[2].checked;
        var isItalic = inputs[3].checked;
        var isUnderline = inputs[4].checked;
        var primaryColor = inputs[5].value;
        var secondaryColor = inputs[6].value;
        var backColor = inputs[7].value;
        var positionX = inputs[8].value; // Corrected variable name
        var positionY = inputs[9].value; // Corrected variable name
        var aspectRatio = inputs[10].value;
        var mockVideoEle = inputs[11];

        
        sampleText.textContent = 'Sample Text';
        sampleText.style.fontFamily = fontName;
        sampleText.style.fontSize = fontSize + 'px';
        sampleText.style.fontWeight = isBold ? 'bold' : 'normal';
        sampleText.style.fontStyle = isItalic ? 'italic' : 'normal';
        sampleText.style.textDecoration = isUnderline ? 'underline' : 'none';
        sampleText.style.color = primaryColor;
        sampleText.style.backgroundColor = backColor;
        sampleText.style.boxShadow = '0 0 0 5px ' + secondaryColor + ' inset';
        sampleText.style.marginLeft = positionX + 'px';
        sampleText.style.marginBottom = positionY + 'px';
        mockVideoEle.style.width =  aspectRatio === "16:9" ? "406px" : "230px";
        mockVideoEle.style.height = aspectRatio === "9:16" ? "406px" : "230px";
    }

    return {
        configureDOM: function() {
            const fontNameSelect = document.getElementById("font-name");
            const fontSizeSelect = document.getElementById("font-size");
            const boldCheckbox = document.getElementById("bold");
            const italicCheckbox = document.getElementById("italic");
            const underlineCheckbox = document.getElementById("underline");
            const primaryColorInput = document.getElementById("primary-color");
            const secondaryColorInput = document.getElementById("secondary-color");
            const backColorInput = document.getElementById("back-color");
            const positionXInput = document.getElementById("position-x"); // Corrected ID
            const positionYInput = document.getElementById("position-y"); // Corrected ID
            const aspectRatioSelect = document.getElementById("aspect-ratio");
            const mockVideo = document.getElementById("mock-video");
            const sampleText = document.getElementById("sample-text");
            const inputs = [fontNameSelect, fontSizeSelect, boldCheckbox, italicCheckbox, underlineCheckbox, primaryColorInput, secondaryColorInput, backColorInput, positionXInput, positionYInput, aspectRatioSelect, mockVideo];

            updateVideoStylerListener(inputs, sampleText);
        }
    }

})();

export default videoStylerUI;

