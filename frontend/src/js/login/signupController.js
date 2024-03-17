import { sha256 } from "../shared/auth.js";

export function configureSignupController() {
    const signupForm  = document.getElementById('signup-form');

    signupForm.addEventListener('submit', async function(event) {
        const pwd = document.getElementById("signup-pwd").value;
        const signupHash  = document.getElementById('signup-hash');
        console.log(pwd);
        event.preventDefault();
        let hash = await sha256(pwd);
        signupHash.value = hash;
        console.log(signupHash.value);

        this.submit();
    });  
} 