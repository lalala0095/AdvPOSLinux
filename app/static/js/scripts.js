// document.addEventListener('DOMContentLoaded', function () {
//     var passwordField = document.querySelector('[name="password"]');
//     var confirmPasswordField = document.querySelector('[name="confirm_password"]');
//     var capsLockIndicator = document.getElementById('capsLockIndicator');

//     // Function to check Caps Lock state
//     function checkCapsLock(event) {
//         if (event.getModifierState && event.getModifierState("CapsLock")) {
//             capsLockIndicator.style.display = "block";  // Show Caps Lock indicator
//         } else {
//             capsLockIndicator.style.display = "none";  // Hide Caps Lock indicator
//         }
//     }

//     // Check Caps Lock on keydown event for password fields
//     if (passwordField) {
//         passwordField.addEventListener('keydown', checkCapsLock);
//     }
//     if (confirmPasswordField) {
//         confirmPasswordField.addEventListener('keydown', checkCapsLock);
//     }

//     // Optional: Hide the indicator when user clicks outside the password fields
//     passwordField.addEventListener('blur', function() {
//         capsLockIndicator.style.display = "none";
//     });

//     confirmPasswordField.addEventListener('blur', function() {
//         capsLockIndicator.style.display = "none";
//     });
// });


document.addEventListener('DOMContentLoaded', function () {
    // Remove the first product after page load to avoid the issue with pre-rendered totals
    const firstRow = document.querySelector("#products-table tbody tr");
    if (firstRow) {
        firstRow.remove();  // Remove the first pre-rendered product
    }

    // Trigger total calculation for any dynamically added rows
    document.getElementById("add-product-btn").addEventListener("click", addProductRow);

    // Attach remove listeners for dynamically added rows
    attachRemoveListener();
    
    // Capture form data and serialize to hidden input
    document.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();

        const products = [];
        const rows = document.querySelectorAll("#products-table tbody tr");

        rows.forEach(row => {
            const product = {
                product_name: row.querySelector("input[name*='[product_name]']").value,
                product_type: row.querySelector("input[name*='[product_type]']").value,
                quantity: row.querySelector("input[name*='[quantity]']").value,
                price: row.querySelector("input[name*='[price]']").value,
                total: row.querySelector("input[name*='[total]']").value
            };
            products.push(product);
        });

        // Serialize to JSON and set to hidden input
        const productsInput = document.getElementById("products-input");
        productsInput.value = JSON.stringify(products);  // Ensure it's serialized

        // Now submit the form
        this.submit();  // Submit the form normally
    });
});

function addProductRow() {
    const tableBody = document.querySelector("#products-table tbody");
    const rowCount = tableBody.children.length;

    const newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td>
            <label>Product Name</label>
            <input type="text" name="products[${rowCount}][product_name]" class="form-control" />
        </td>
        <td>
            <label>Product Type</label>
            <input type="text" name="products[${rowCount}][product_type]" class="form-control" />
        </td>
        <td>
            <label>Quantity</label>
            <input type="number" name="products[${rowCount}][quantity]" class="form-control" />
        </td>
        <td>
            <label>Price</label>
            <input type="number" name="products[${rowCount}][price]" class="form-control" />
        </td>
        <td>
            <label>Total</label>
            <input type="number" name="products[${rowCount}][total]" class="form-control" readonly />
        </td>
        <td>
            <button type="button" class="btn btn-danger remove-product-btn">Remove</button>
        </td>
    `;
    
    tableBody.appendChild(newRow);
    attachRowListeners(newRow);
    attachRemoveListener();
}

function attachRowListeners(row) {
    const quantityInput = row.querySelector("[name*='[quantity]']");
    const priceInput = row.querySelector("[name*='[price]']");
    if (quantityInput && priceInput) {
        quantityInput.addEventListener("change", function () {
            updateTotal(quantityInput);
        });
        priceInput.addEventListener("change", function () {
            updateTotal(priceInput);
        });
    }
}

function updateTotal(input) {
    const row = input.closest("tr");
    const quantity = parseFloat(row.querySelector("[name*='[quantity]']").value) || 0;
    const price = parseFloat(row.querySelector("[name*='[price]']").value) || 0;
    const totalField = row.querySelector("[name*='[total]']");

    const total = quantity * price;
    totalField.value = total > 0 ? total.toFixed(2) : "";
}

function attachRemoveListener() {
    const removeBtns = document.querySelectorAll(".remove-product-btn");

    removeBtns.forEach((btn) => {
        btn.addEventListener("click", function () {
            btn.closest("tr").remove();
        });
    });
}
