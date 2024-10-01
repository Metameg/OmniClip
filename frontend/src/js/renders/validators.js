const Validators = (function() {
    function addValid(field) {
        field.classList.remove("is-invalid");
        field.classList.add("is-valid");
    }
    
    function addInvalid(field) {
        field.classList.remove("is-valid");
        field.classList.add("is-invalid");
    }

    function hasValidVideoFile(files) {
        return Array.from(files).some(file => {
            const fileType = file.type.toLowerCase();
            return fileType === 'video/mp4' || fileType === 'video/quicktime' || 
                fileType === 'video/webm'  || fileType === 'video/ogg' || 
                fileType === 'video/x-msvideo' || fileType === 'video/x-ms-wmv';
        });
    }
    
    function hasValidAudioFile(files) {
        return Array.from(files).some(file => {
            const fileType = file.type.toLowerCase();
            return fileType === 'audio/mpeg' || fileType === 'audio/wav' || 
                fileType === 'audio/wave' || fileType === 'audio/x-wav' || 
                fileType === 'audio/ogg' || fileType === 'audio/aac' || 
                fileType === 'audio/flac' || fileType === 'audio/midi' || 
                fileType === 'audio/x-midi' || fileType === 'audio/amr' || 
                fileType === 'audio/webm';
        });
    }
    
    function hasValidImageFile(files) {
        return Array.from(files).some(file => {
            const fileType = file.type.toLowerCase();
            return fileType === 'image/jpeg' || fileType === 'image/png' || 
            fileType === 'image/gif' || fileType === 'image/bmp' || 
            fileType === 'image/tiff' || fileType === 'image/svg+xml' || 
            fileType === 'image/webp' || fileType === 'image/x-icon';
            
        });
    }
    
    return {
        imports: {
            validateVideo: (inputField) => {
                inputField.addEventListener("change", function(event) {
                    const files = inputField.files; 
                    if (hasValidVideoFile(files)) {
                        addValid(inputField);
                    }
                    else {
                        addInvalid(inputField);
                    }  
                });
                
            },

            validateAudio: (inputField) => {
                inputField.addEventListener("change", function(event) {
                    const files = inputField.files; 
                    if (hasValidAudioFile(files)) {
                        addValid(inputField);
                    }
                    else {
                        addInvalid(inputField);
                    }  
                });
                
            },

            validateImage: (inputField) => {
                inputField.addEventListener("change", function(event) {
                    const files = inputField.files; 
                    if (hasValidImageFile(files)) {
                        addValid(inputField);
                    }
                    else {
                        addInvalid(inputField);
                    }  
                });
                
            }
        },

        slides: {
            validateRange: function(range, input, needsLengthRecal)  {

                input.addEventListener('input', function () {
                    var inputValue = parseFloat(input.value) || 0; // Ensure it's a valid number
                    // Enforce min and max values
                    inputValue = Math.min(Math.max(inputValue, parseFloat(range.min)), parseFloat(range.max));
                    range.value = inputValue;
                    if (needsLengthRecal){
                        this.calculateTotalLength();
                    }
                }.bind(this));
                
                input.addEventListener('change', function () {
                    var inputValue = parseFloat(input.value) || 0; // Ensure it's a valid number
                    // Enforce min and max values
                    inputValue = Math.min(Math.max(inputValue, parseFloat(range.min)), parseFloat(range.max));
                    input.value = inputValue;
    
                    if (needsLengthRecal){
                        this.calculateTotalLength();
                    }
                }.bind(this));
                
                range.addEventListener('input', function () {
                    input.value = range.value;
                    if (needsLengthRecal){
                        this.calculateTotalLength();
                    }
                }.bind(this));
            },

            calculateTotalLength: function() {
                const numclips = document.getElementById('num-clips-val');
                const clipLength = document.getElementById('clip-length-val');
                const totalLength = document.getElementById('total-length-val');
                console.log(numclips.value, clipLength.value, totalLength.value);
                
                totalLength.value = numclips.value * clipLength.value;
            },

            calculateClipLength: () => {
                const numclips = document.getElementById('num-clips-val');
                const clipLength = document.getElementById('clip-length-val');
                const clipLengthRange = document.getElementById('clip-length-range');
                const totalLength = document.getElementById('total-length-val');
                console.log(numclips, clipLength, totalLength);
                
                totalLength.addEventListener('input', function () {
                    var inputValue = parseFloat(totalLength.value) || 0; // Ensure it's a valid number
                    // Enforce min and max values
                    inputValue = Math.max(inputValue, parseFloat(totalLength.min));
                    totalLength.value = inputValue;
                    clipLength.value = totalLength.value / numclips.value;
                    clipLengthRange.value = totalLength.value / numclips.value;
                });
                totalLength.addEventListener('change', function () {
                    var inputValue = parseFloat(totalLength.value) || 0; // Ensure it's a valid number
                    // Enforce min and max values
                    inputValue = Math.max(inputValue, parseFloat(totalLength.min));
                    totalLength.value = inputValue;
                    clipLength.value = totalLength.value / numclips.value;
                    clipLengthRange.value = totalLength.value / numclips.value;
                });
            }
        },

        voice: {
            validate: (voice) => {
                const voices = ["joey", "amy", "arthur", "kendra", "pedro"];
                
                var value = voice.value.toLowerCase();
                voices.includes(value) ? addValid(voice) : addInvalid(voice);   
                
                voice.addEventListener('change', function () {
                    var value = voice.value.toLowerCase();
                    console.log(value);
                    voices.includes(value) ? addValid(voice) : addInvalid(voice);   
                });
            }
        },

        audioFile: {
            validate: (file) => {
                const fileType = file.type.toLowerCase();
        
                return fileType === 'audio/mpeg' || fileType === 'audio/wav' || 
                    fileType === 'audio/wave' || fileType === 'audio/x-wav' || 
                    fileType === 'audio/ogg' || fileType === 'audio/aac' || 
                    fileType === 'audio/flac' || fileType === 'audio/midi' || 
                    fileType === 'audio/x-midi' || fileType === 'audio/amr' || 
                    fileType === 'audio/webm';
            }
            
        },

        inputField: {
            validateNumber: (input) => {
                input.addEventListener('input', function () {
                    var inputValue = parseFloat(input.value) || 0; // Ensure it's a valid number
            
                    // Enforce min and max values
                    inputValue = Math.min(Math.max(inputValue, parseFloat(input.min)), parseFloat(input.max));
                    input.value = inputValue;
                
                });
                
                input.addEventListener('change', function () {
                    var inputValue = parseFloat(input.value) || 0; // Ensure it's a valid number
                    // Enforce min and max values
                    inputValue = Math.min(Math.max(inputValue, parseFloat(input.min)), parseFloat(input.max));
                    input.value = inputValue;
                });
            }
        }
    };
})();

export default Validators;
