document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');
    const username = document.getElementById("username");
    const password = document.getElementById("password");

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        sendLogin(username.value, password.value);
    });

    async function sendLogin(username, password) {
        const message = { "username": username, "password": password };
        console.log(message);
        await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(message)
        });
    }
});
