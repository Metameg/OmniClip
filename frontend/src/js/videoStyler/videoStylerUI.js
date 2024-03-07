import { notEnableFromCheckbox, updateHiddenBln } from "../shared/utils.js";

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
        
        var isOutlineTransparent = inputs[8].checked;
        var isBackTransparent = inputs[9].checked;
        var outlineColor = isOutlineTransparent ? '#00000000' : inputs[6].value;
        var backColor = isBackTransparent ? '#00000000' : inputs[7].value;

        var positionX = inputs[10].value; 
        var positionY = inputs[11].value; 
        var aspectRatio = inputs[12].value;
        var mockVideoEle = inputs[13];

        sampleText.textContent = 'Sample Text';
        sampleText.style.fontFamily = fontName;
        sampleText.style.fontSize = fontSize + 'px';
        sampleText.style.fontWeight = isBold ? 'bold' : 'normal';
        sampleText.style.fontStyle = isItalic ? 'italic' : 'normal';
        sampleText.style.textDecoration = isUnderline ? 'underline' : 'none';
        sampleText.style.color = primaryColor;
        sampleText.style.backgroundColor = backColor;
        sampleText.style.boxShadow = '0 0 0 5px ' + outlineColor + ' inset';
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
            const boldBlnHidden = document.getElementById('bold-value');
            const italicBlnHidden = document.getElementById('italic-value');
            const underlineBlnHidden = document.getElementById('underline-value');
            const primaryColorInput = document.getElementById("primary-color");
            const outlineColorInput = document.getElementById("outline-color");
            const backColorInput = document.getElementById("back-color");
            const outlineTransparentBln = document.getElementById('outline-transparent-bln');
            const backTransparentBln = document.getElementById('background-transparent-bln');
            const positionXInput = document.getElementById("position-x"); // Corrected ID
            const positionYInput = document.getElementById("position-y"); // Corrected ID
            const aspectRatioSelect = document.getElementById("aspect-ratio");
            const mockVideo = document.getElementById("mock-video");
            const sampleText = document.getElementById("sample-text");
            // const inputs = [fontNameSelect, fontSizeSelect, boldCheckbox, italicCheckbox, underlineCheckbox, positionXInput, positionYInput, aspectRatioSelect, mockVideo];
            const inputs = [fontNameSelect, fontSizeSelect, boldCheckbox, 
                            italicCheckbox, underlineCheckbox, primaryColorInput,
                            outlineColorInput, backColorInput, 
                            outlineTransparentBln, backTransparentBln, positionXInput, 
                            positionYInput, aspectRatioSelect, mockVideo];

            updateHiddenBln(boldBlnHidden, boldCheckbox);
            updateHiddenBln(italicBlnHidden, italicCheckbox);
            updateHiddenBln(underlineBlnHidden, underlineCheckbox);
            notEnableFromCheckbox(outlineTransparentBln, outlineColorInput);
            notEnableFromCheckbox(backTransparentBln, backColorInput);
            updateVideoStylerListener(inputs, sampleText);
        }
    }

})();

export default videoStylerUI;

