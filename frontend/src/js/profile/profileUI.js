import Validators from "./validators.js";
import { notEnableFromCheckbox, enableFromCheckbox, updateHiddenBln } from "../shared/utils.js";

const profileDOM = (function () {
    // Private variables and functions

    function voiceSelect (voice, radios) {
        radios.forEach(function (radioButton) {
            radioButton.addEventListener('click', function () {
                if (radioButton.checked) {
                    console.log(radioButton.value);
                    voice.value = radioButton.value;
                    Validators.voice.validate(voice);
                }
            });
        });
    }




    // Public API
    return {
        configureDOM: function() {
            // const clippackPath = document.getElementById('clippack-path');
            const manualClippackBln = document.getElementById('clippack-checkbox');
            const manualClippackBlnHidden = document.getElementById('clippack-checkbox-value');
            
            const rendersList = document.getElementById('clippack-checkbox-value');

            Validators.inputField.validateNumber(totalLength);
            Validators.slides.validateRange(numvideosRange, numvideos, false);
            Validators.slides.validateRange(fadeDurationRange, fadeDuration, false);
            notEnableFromCheckbox(sameCategoryBln, quoteCategory);
            voiceSelect(voice, voiceRadios);
            
        }
    };
})();

export default profileDOM;