const login = async () => {
    const tokenSTR=localStorage.getItem('token');
    const token=tokenSTR.replaceAll('"', '');
    try {
        let response = await fetch('http://127.0.0.1:8000/user/me', {
            method: 'GET',
            headers: {
              'Authorization': 'Bearer ' + token
            }
        });
        const result = await response.json();
        document.getElementById("username-left").innerHTML = result.username;
        console.log(result.message, response.status == 200 ? 'success' : 'error');

    } catch (error) {
        console.log(error.message, 'error');
    }
};

login();
