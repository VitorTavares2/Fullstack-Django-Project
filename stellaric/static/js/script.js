document.addEventListener('DOMContentLoaded', () => {
    const bar = document.getElementById('bar');
    const close = document.getElementById('close');
    const nav = document.getElementById('navbar1');

    if (bar) {
        bar.addEventListener('click', () => {
            nav.classList.add('active');
        });
    }

    if (close) {
        close.addEventListener('click', () => {
            nav.classList.remove('active');
        });
    }
});


let cart = [];

function addToCart(index) {
    const quantityInput = document.getElementById('quantityInput');
    const quantity = parseInt(quantityInput.value);
    if (quantity > 0) {
        const item = {
            name: 'White T-Shirt With Details',
            price: 135,
            quantity: quantity
        };
        cart.push(item);
        updateCart();
        quantityInput.value = 0; // Reiniciar o valor do input
    } else {
        alert('Por favor, selecione uma quantidade válida.');
    }
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

function updateCart() {
    const tbody = document.querySelector('#cart tbody');
    tbody.innerHTML = '';

    let cartSubtotal = 0;
    cart.forEach((item, index) => {
        const subtotal = item.price * item.quantity;
        cartSubtotal += subtotal;

        const row = `
            <tr>
                <td><a href="#" onclick="removeFromCart(${index})"><i class="far fa-times-circle"></i></a></td>
                <td><img src="img/ph1.png" alt=""></td>
                <td>${item.name}</td>
                <td>R$ ${item.price.toFixed(2)}</td>
                <td>${item.quantity}</td>
                <td>R$ ${subtotal.toFixed(2)}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });

    document.getElementById('cartSubtotal').textContent = `R$ ${cartSubtotal.toFixed(2)}`;
    document.getElementById('totalAmount').textContent = cartSubtotal.toFixed(2);
}

function applyCoupon() {
    const couponInput = document.getElementById('couponInput');
    const couponCode = couponInput.value.trim();
    const correctCoupon='STELLA15';
    if (couponCode.toUpperCase() === correctCoupon.toUpperCase()) {
        alert('Your Discount Has Been Applied With Success');
    } else {
        alert('Wrong Code, Please Enter a Valid Coupon');
    }
    couponInput.value = ''; 
}

function proceedToCheckout() {
    alert('Proceeding to checkout...');
}

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.toast').forEach(function (toastEl) {
        new bootstrap.Toast(toastEl).show();
    });
});