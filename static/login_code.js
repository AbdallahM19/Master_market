document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/mastermarket/home';
        } else {
            document.getElementById('error').textContent = data.message;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('error').textContent = 'An error occurred';
    });
});