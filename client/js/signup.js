const btn = document.querySelector('#register');
const form = document.querySelector('#register-form');
const messageEl = document.querySelector('#message');

btn.addEventListener('click', (e) => {
    e.preventDefault();
    register();
});
const register = async () => {
    console.log("Button working");
    const req={
        username:document.getElementById("username").value,
        hashed_password:document.getElementById("hashed_password").value,
        email:document.getElementById("email").value,
        full_name:document.getElementById("full_name").value,
        disabled: false
    };
    console.log(JSON.stringify(req));
    try {
        let response = await fetch('http://127.0.0.1:8000/user/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(req),
        });
        const result = await response.json();
        if (result) {
            window.alert("User Registered Successfully, you can now login");
        }
        console.log(result);

    } catch (error) {
        showMessage(error.message, 'error');
    }
};
const showMessage = (message, type = 'success') => {
    console.log(message, type);
};