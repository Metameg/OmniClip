import '../scss/_variables.scss';
import '../scss/about.scss';
import '../scss/btn-spinner.scss';
import '../scss/checkout.scss';
import '../scss/circular-progress.scss';
import '../scss/create-content.scss';
import '../scss/fine-tuning-box.scss';
import '../scss/index.scss';
import '../scss/login.scss';
import '../scss/pricing.scss';
import '../scss/profile.scss';
import '../scss/affiliate/affiliate-dashboard.scss';
import '../scss/affiliate/affiliate-signup.scss';
import '../scss/affiliate/affiliate-about.scss';

// console.log('hello');

import { configureRenderForm } from './renders/renderFormController.js';
import { configureQuoteGenerator } from './quoteGenerator/quoteController.js';
import { configureAffiliate } from './affiliate/affiliateController.js';
import { configuremediaUploader } from './mediaUploader/mediaUploaderController.js';



$(document).ready(function() {

    if (window.location.pathname.startsWith('/create-content')) {
        configureRenderForm();
        configuremediaUploader();
        configureQuoteGenerator();
        // configureVideoStyler();
    }  
    if (window.location.pathname.startsWith('/affiliate-program/dashboard')) {
        configureAffiliate();
    }  
}); 







