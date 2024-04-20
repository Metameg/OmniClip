import Validators from "./validators.js";
import { notEnableFromCheckbox, enableFromCheckbox, updateHiddenBln } from "../shared/utils.js";

const renderFormDOM = (function () {
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

    function syncCatgorySelections(quote, clippack) {
        console.log("quote: " + quote);
        clippack.addEventListener('change', function () {
            quote.innerHTML = clippack.value;
        });
    }

    function showDivFromRadio(radiosClass, divs) {

            $(radiosClass).change(function(){
              var selectedDiv = '#' + $(this).attr("id").replace("btn", "content");
              divs.forEach(function(div) {
                 $(div).addClass('d-none');
              })
              $(selectedDiv).removeClass('d-none');
            });

    }

    function collapseDivFromBtn(closeBtn, div) {
        closeBtn.addEventListener('click', function() {
            div.classList.remove('show')
        });
    }

    function showDivFromBtn(showBtn, div) {
        showBtn.addEventListener('click', function() {
            if (div.classList.contains('show')) {
                div.classList.remove('show')
            }
            else {
                div.classList.add('show')
            }
        });
    }

    function updateHiddenInput (hiddenElement, selectElement) {
        selectElement.addEventListener('change', function() {
            hiddenElement.value = selectElement.value;
        });
    }


    function quoteConfirmListener(input, quoteManualConfirmBtn, quoteManualRetryBtn, quoteResponse, quoteValue) {
        quoteManualConfirmBtn.addEventListener('click', function() {
            quoteValue.value = input.value;
            quoteResponse.innerText = input.value;
            input.disabled = true;
            input.classList.add('is-valid');
            quoteManualConfirmBtn.style.display = 'none';
            quoteManualRetryBtn.style.display = 'block';
        });
    }

    function quoteRetryListener (input, quoteManualConfirmBtn, quoteManualRetryBtn, quoteValue) {
        quoteManualRetryBtn.addEventListener('click', function() {
            quoteValue.value = '';
            input.disabled = false;
            input.classList.remove('is-valid');
            quoteManualConfirmBtn.style.display = 'block';
            quoteManualRetryBtn.style.display = 'none';
        });
    }


    // Public API
    return {
        configureDOM: function() {
            // const clippackPath = document.getElementById('clippack-path');
            const manualClippackBln = document.getElementById('clippack-checkbox');
            const manualClippackBlnHidden = document.getElementById('clippack-checkbox-value');
            const clippack = document.getElementById('clippack');
            // const audioPath = document.getElementById('audio-path');
            // const watermarkPath = document.getElementById('watermark-path');
            const totalLength = document.getElementById('total-length-val');
            const numvideos = document.getElementById('num-videos-val');
            const numvideosRange = document.getElementById('num-videos-range');
            const sameCategoryBln = document.getElementById('same-category');
            const sameCategoryBlnHidden = document.getElementById('same-category-value');
            const selectedCategorySpan = document.getElementById('selected-category-span');
            const quoteRadios = document.querySelectorAll('.quote-method-btn');
            const quoteRadioDivs = document.querySelectorAll(['#quote-AI-content','#quote-category-content','#quote-manual-content']);
            const quoteResponse = document.getElementById('quote-response');
            const quoteValue = document.getElementById('quote-val');
            const quoteCategory = document.getElementById('quote-category');
            const quoteCategoryHidden = document.getElementById('quote-category-value');
            const quoteManualInput = document.getElementById('quote-manual');
            const quoteManualConfirmBtn = document.getElementById('manual-confirm-btn');
            const quoteManualRetryBtn = document.getElementById('manual-retry-btn');
            const fadeDuration = document.getElementById('fade-duration-val');
            const fadeDurationRange = document.getElementById('fade-duration-range');
            const voice = document.getElementById('voice-val');
            const collapseMenu = document.getElementById('collapse-voices');
            const voiceRadios = document.querySelectorAll('input[type="radio"][name="voice"]');
            const voiceCloseBtn = document.getElementById('voice-btn-close');
            const voiceSelectBtn = document.getElementById('voice-select-btn');
            const voiceCollapse = document.getElementById('collapse-voices');
            const boldBln = document.getElementById('bold');
            const italicBln = document.getElementById('italic');
            const underlineBln = document.getElementById('underline');
            const boldBlnHidden = document.getElementById('bold-value');
            const italicBlnHidden = document.getElementById('italic-value');
            const underlineBlnHidden = document.getElementById('underline-value');

            enableFromCheckbox(manualClippackBln, clippack);
            // notEnableFromCheckbox(manualClippackBln, clippackPath);
            // Validators.imports.validateVideo(clippackPath);
            // Validators.imports.validateAudio(audioPath);
            // Validators.imports.validateImage(watermarkPath);
            Validators.inputField.validateNumber(totalLength);
            Validators.slides.validateRange(numvideosRange, numvideos, false);
            Validators.slides.validateRange(fadeDurationRange, fadeDuration, false);
            notEnableFromCheckbox(sameCategoryBln, quoteCategory);
            voiceSelect(voice, voiceRadios);
            Validators.voice.validate(voice);
            syncCatgorySelections(selectedCategorySpan, clippack);
            showDivFromRadio(quoteRadios, quoteRadioDivs);
            updateHiddenInput(quoteCategoryHidden, quoteCategory);
            updateHiddenBln(sameCategoryBlnHidden, sameCategoryBln);
            updateHiddenBln(manualClippackBlnHidden, manualClippackBln);
            updateHiddenBln(boldBlnHidden, boldBln);
            updateHiddenBln(italicBlnHidden, italicBln);
            updateHiddenBln(underlineBlnHidden, underlineBln);
            quoteConfirmListener(quoteManualInput, quoteManualConfirmBtn, quoteManualRetryBtn, quoteResponse, quoteValue);
            quoteRetryListener(quoteManualInput, quoteManualConfirmBtn, quoteManualRetryBtn, quoteValue);
            showDivFromBtn(voiceSelectBtn, voiceCollapse);
            collapseDivFromBtn(voiceCloseBtn, voiceCollapse);
        },

        showVideoLoading: () => {
            const carousel = document.getElementById('render-carousel');
            carousel.style.display = 'block';
            $.get('/loading_container_partial', function(data) {
                $('#video-content').html(data);
            });
        }
    };
})();

export default renderFormDOM;