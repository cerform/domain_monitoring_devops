document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('login-form');
    const username = document.querySelector('#username');
    const password = document.querySelector('#password');

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        sendLogin(username.value, password.value);
    });

    async function sendLogin(username, password) {
        const message = { username, password };
        await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(message)
        });
    }

    // Optionally, handle register button click
    document.getElementById('register').addEventListener('click', function() {
        window.location.href = '/register';
    });
});
