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
    const productsTable = document.querySelector("#products-table tbody");
    const addProductBtn = document.getElementById("add-product-btn");
    const productsInput = document.getElementById("products-input");

    // Add a product row when the "Add" button is clicked
    addProductBtn.addEventListener("click", function () {
        const rowCount = productsTable.children.length;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="products[${rowCount}][product_name]" class="form-control" placeholder="Product Name" required />
            </td>
            <td>
                <input type="text" name="products[${rowCount}][product_type]" class="form-control" placeholder="Product Type" />
            </td>
            <td>
                <input type="number" name="products[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="products[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="text" name="products[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-product-btn">Remove</button>
            </td>
        `;
        productsTable.appendChild(newRow);

        attachRowListeners(newRow);
    });

    // Remove product rows dynamically
    productsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-product-btn")) {
            e.target.closest("tr").remove();
            updateRowNames();
        }
    });

    // Serialize form data into the hidden input on form submission
    document.querySelector("form").addEventListener("submit", function (e) {
        const rows = productsTable.querySelectorAll("tr");
        const products = Array.from(rows).map(row => ({
            product_name: row.querySelector("input[name*='[product_name]']").value,
            product_type: row.querySelector("input[name*='[product_type]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));

        // Set the serialized JSON into the hidden input
        productsInput.value = JSON.stringify(products);
    });

    // Automatically calculate totals for each row
    function attachRowListeners(row) {
        const quantityInput = row.querySelector("input[name*='[quantity]']");
        const priceInput = row.querySelector("input[name*='[price]']");

        [quantityInput, priceInput].forEach(input => {
            input.addEventListener("input", function () {
                const quantity = parseFloat(quantityInput.value || 0);
                const price = parseFloat(priceInput.value || 0);
                const totalField = row.querySelector("input[name*='[total]']");
                totalField.value = (quantity * price).toFixed(2);
            });
        });
    }

    // Update row input names after a row is removed
    function updateRowNames() {
        const rows = productsTable.querySelectorAll("tr");
        rows.forEach((row, index) => {
            row.querySelectorAll("input").forEach(input => {
                const name = input.name.replace(/\[\d+\]/, `[${index}]`);
                input.name = name;
            });
        });
    }
});
