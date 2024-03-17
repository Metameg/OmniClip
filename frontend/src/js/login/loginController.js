import { sha256 } from "../shared/auth.js";

export function configureLoginController() {
    
    const loginForm  = document.getElementById('login-form');
    
    loginForm.addEventListener('submit', async function(event) {
        const pwd = document.getElementById("login-pwd").value;
        const loginHash  = document.getElementById('login-hash');
        console.log(pwd);
        // event.preventDefault();
        let hash = await sha256(pwd);
        loginHash.value = hash;
        console.log(loginHash.value);

        this.submit();
    });    

     
}