function showsection(sectionId) {
    // Hide all sections
    document.querySelector('.addproducts').style.display = 'none';
    document.querySelector('.editproducts').style.display = 'none';
    document.querySelector('.delproduct').style.display = 'none';

    // Show the selected section
    if (sectionId) {
        document.getElementById(sectionId).style.display = 'flex';
    }
}

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

// function showEditForm(productId) {
//    // Hide all edit forms
//     document.querySelectorAll('.information').forEach(form => form.style.display = 'none');
//     // Show the selected form
//     document.getElementById('edit_form_' + productId).style.display = 'flex';
// }

// Initially hide all sections
document.addEventListener('DOMContentLoaded', function() {
    showsection('');

    const addProductForm = document.getElementById('add_product');
    const editProductForm = document.getElementById('edit_product');
    const deleteProductForm = document.getElementById('delete_product');

    addProductForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        const description = document.getElementById('description').value;
        const price = document.getElementById('price').value;
        const currency = document.getElementById('currency').value;
        const stock = document.getElementById('stock').value;
        const category = document.getElementById('category').value;
        const brand = document.getElementById('brand').value;
        const attributes = document.getElementById('attributes').value;

        try {
            const response = await fetch('/add_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    description: description,
                    price: price,
                    currency: currency,
                    stock: stock,
                    category: category,
                    brand: brand,
                    attributes: attributes
                })
            });

            const data = await response.json();
            showmessage(data.message, data.status, 'success', 'error');
        } catch (error) {
            showmessage('An error occurred while adding the product.', 'error', 'success', 'error');
        }
    });

    editProductForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const product_id = document.getElementById('product_id').value;
        const name = document.getElementById('edit_name').value;
        const description = document.getElementById('edit_description').value;
        const price = document.getElementById('edit_price').value;
        const currency = document.getElementById('edit_currency').value;
        const stock = document.getElementById('edit_stock').value;
        const category = document.getElementById('edit_category').value;
        const brand = document.getElementById('edit_brand').value;
        const attributes = document.getElementById('edit_attributes').value;

        try {
            const response = await fetch('/edit_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_id: product_id,
                    name: name,
                    description: description,
                    price: price,
                    currency: currency,
                    stock: stock,
                    category: category,
                    brand: brand,
                    attributes: attributes
                })
            });

            const data = await response.json();

            showmessage(data.message, data.status, 'success', 'error');
        } catch (error) {
            showmessage('An error occurred while editing the product.', 'error', 'success', 'error');
        }
    });

    deleteProductForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const product_id = document.getElementById('product_id').value;

        try {
            const response = await fetch('/delete_product', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_id: product_id
                })
            });

            const data = await response.json();

            showmessage(data.message, data.status, 'success', 'error');
        } catch (error) {
            showmessage('An error occurred while deleting the product.', 'error', 'success', 'error');
        }
    });
});