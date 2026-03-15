function addToCart(id) {
    let sizeSelect = document.getElementById("size-" + id);
    let size = sizeSelect ? sizeSelect.value : null;

    let qtyInput = document.getElementById("qty-" + id);
    let qty = qtyInput ? parseInt(qtyInput.value) : 1;

    fetch("/cart/add", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: id, size: size, qty: qty})
    })
    .then(res => res.json())
    .then(() => {
        updateCartSidebar();
        showToast();
    });
}

function updateCartSidebar() {
    fetch("/cart/get")
        .then(res => res.json())
        .then(cart => {
            const container = document.getElementById("cart-items");
            container.innerHTML = "";

            let total = 0;

            for (const key in cart) {
                const item = cart[key];
                total += item.price * item.qty;

                container.innerHTML += `
                    <div class="cart-item">
                        <p>${item.name}</p>
                        ${item.size ? `<p>Size: ${item.size}</p>` : ""}
                        <p>Qty: ${item.qty}</p>
                        <button onclick="removeFromCart('${key}')" class="remove-btn">Remove</button>
                    </div>
                `;
            }

            document.getElementById("cart-total").innerText = "£" + total.toFixed(2);
        });
}

function removeFromCart(key) {
    fetch("/cart/remove", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id: key})
    })
    .then(() => updateCartSidebar());
}

function openCart() {
    document.getElementById("cart-sidebar").classList.add("open");
}

function closeCart() {
    document.getElementById("cart-sidebar").classList.remove("open");
}

function showToast() {
    const toast = document.getElementById("toast");
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
}
