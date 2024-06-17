function showmessage(message, status, successElementId, errorElementId) {
    let successElement = document.getElementById(successElementId);
    let errorElement = document.getElementById(errorElementId);

    if (status === 'success') {
        successElement.textContent = message;
        successElement.style.display = 'block';
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    } else {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
        successElement.textContent = '';
        successElement.style.display = 'none';
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    const saveButtons = document.querySelectorAll('.save');
    const favoriteButtons = document.querySelectorAll('.favorite');
    const far_buttons = document.querySelectorAll('.button_fav');

    // Handle save buttons
    saveButtons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const productId = e.target.getAttribute('data-product-id');

            try {
                const response = await fetch('/add_to_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ product_id: productId })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    showmessage(data.message, data.status, 'success', 'error', button);
                    location.reload();
                } else {
                    showmessage(data.message, data.status, 'success', 'error', button);
                }
            } catch (error) {
                showmessage('An error occurred while adding the product to the cart.', 'error', 'success', 'error', button);
            }
        });
    });

    // Fetch favorite products
    try {
        const response = await fetch('/get_favorites', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (data.status === 'success') {
            const favorites = data.favorites;

            favoriteButtons.forEach(button => {
                const productId = button.getAttribute('data-product-id');

                if (favorites.includes(productId)) {
                    button.classList.add('active');
                }

                button.addEventListener('click', async (e) => {
                    try {
                        const response = await fetch('/add_to_favorite', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ product_id: productId })
                        });

                        const data = await response.json();

                        if (data.status === 'success') {
                            showmessage(data.message, data.status, 'success', 'error');
                            location.reload();
                        } else {
                            showmessage(data.message, data.status, 'success', 'error');
                        }
                    } catch (error) {
                        showmessage('An error occurred while adding the product to the cart.', 'error', 'success', 'error', button);
                    }
                });
            });
        }
    } catch (error) {
        console.error('Error fetching favorite products:', error);
    }

    // Handle del far product
    far_buttons.forEach(button => {
        button.addEventListener('click', async (e) => {
            const productId = e.target.getAttribute('data-product-id');

            try {
                const response = await fetch('/delete_from_cart', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ product_id: productId })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    showmessage(data.message, data.status, 'success', 'error', button);
                    location.reload();
                } else {
                    showmessage(data.message, data.status, 'success', 'error', button);
                }
            } catch (error) {
                showmessage('An error occurred while adding the product to the cart.', 'error', 'success', 'error', button);
            }
        });
    });
});

function toggleFavorite(button) {
    button.classList.toggle('active')
}