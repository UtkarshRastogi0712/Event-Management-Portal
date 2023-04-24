const btn = document.querySelector('#login');
const form = document.querySelector('#login-form');
const messageEl = document.querySelector('#message');

btn.addEventListener('click', (e) => {
    e.preventDefault();
    login();
});

const login = async () => {
    console.log("Button working");
    try {
        let response = await fetch('http://127.0.0.1:8000/token', {
            method: 'POST',
            body: new FormData(form),
        });
        const result = await response.json();
        if (response.status == 200) {
            localStorage.setItem('token', JSON.stringify(result.access_token));
            window.location.href = "index.html";
        }
        else{
            window.alert("Invalid Credentials");
        }
        console.log(result);
        showMessage(result.message, response.status == 200 ? 'success' : 'error');

    } catch (error) {
        showMessage(error.message, 'error');
    }
};

const showMessage = (message, type = 'success') => {
    console.log(message, type);
};