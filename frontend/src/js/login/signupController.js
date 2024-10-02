import { sha256 } from "../shared/auth.js";

export function configureSignupController() {
    const signupForm  = document.getElementById('signup-form');

    signupForm.addEventListener('submit', async function(event) {
        const pwd = document.getElementById("signup-pwd").value;
        const pwdError = document.getElementById("pwd_error");
        const signupHash  = document.getElementById('signup-hash');
        event.preventDefault();
        let hash = await sha256(pwd);
        signupHash.value = hash;
        if (pwd.length < 8) {
            pwdError.style.display = 'block';
        }

        else {
            this.submit();
        }
    });  
} 