document.addEventListener('DOMContentLoaded', function () {
    var passwordField = document.querySelector('[name="password"]');
    var confirmPasswordField = document.querySelector('[name="confirm_password"]');
    var capsLockIndicator = document.getElementById('capsLockIndicator');

    // Function to check Caps Lock state
    function checkCapsLock(event) {
        if (event.getModifierState && event.getModifierState("CapsLock")) {
            capsLockIndicator.style.display = "block";  // Show Caps Lock indicator
        } else {
            capsLockIndicator.style.display = "none";  // Hide Caps Lock indicator
        }
    }

    // Check Caps Lock on keydown event for password fields
    if (passwordField) {
        passwordField.addEventListener('keydown', checkCapsLock);
    }
    if (confirmPasswordField) {
        confirmPasswordField.addEventListener('keydown', checkCapsLock);
    }

    // Optional: Hide the indicator when user clicks outside the password fields
    passwordField.addEventListener('blur', function() {
        capsLockIndicator.style.display = "none";
    });

    confirmPasswordField.addEventListener('blur', function() {
        capsLockIndicator.style.display = "none";
    });
});



function updateProductDetails(productSelect) {
    // Get the selected option
    var selectedOption = productSelect.options[productSelect.selectedIndex];

    // Retrieve the data attributes (product_type, price)
    var productType = selectedOption.getAttribute('data-product-type');
    var productPrice = selectedOption.getAttribute('data-product-price');
    
    // Get the closest product form to update the product details
    var productForm = productSelect.closest('.product-form'); // Make sure your form is correctly wrapped with 'product-form' class
    
    if (productForm) {
        // Set the values in the form fields

        var productTypeInput = productForm.querySelector('[name*="product_type"]');
        if (productTypeInput) {
            productTypeInput.value = productType;
        }

        // Check if the price input exists and set its value
        var priceInput = productForm.querySelector('[name*="price"]');
        if (priceInput) {
            priceInput.value = productPrice;
        }

        // Optionally, reset the quantity and total fields here
        var quantityInput = productForm.querySelector('[name*="quantity"]');
        var totalInput = productForm.querySelector('[name*="total"]');
        
        if (quantityInput && totalInput) {
            quantityInput.value = '';  // Reset quantity field
            totalInput.value = '';    // Reset total field
        }

        // Call calculateTotal to update total
        calculateTotal(productForm);
    }
}

// Function to calculate total price based on quantity and product price
function calculateTotal(productForm) {
    var quantity = parseFloat(productForm.querySelector('[name*="quantity"]').value);
    var price = parseFloat(productForm.querySelector('[name*="price"]').value);

    if (!isNaN(quantity) && !isNaN(price)) {
        var total = quantity * price;
        productForm.querySelector('[name*="total"]').value = total.toFixed(2);  // Format the total to 2 decimal places
    } else {
        productForm.querySelector('[name*="total"]').value = '';  // Clear total if inputs are invalid
    }
}



// JavaScript to handle adding products dynamically
document.getElementById("add-product-btn").addEventListener("click", function() {
    let tableBody = document.querySelector("#products-table tbody");
    let rowCount = tableBody.children.length; // Initialize the row count based on existing rows

    let newRow = document.createElement("tr");
    newRow.innerHTML = `
        <td><input type="text" name="products[${rowCount}][product_name]" class="form-control" /></td>
        <td><input type="text" name="products[${rowCount}][product_type]" class="form-control" /></td>
        <td><input type="number" name="products[${rowCount}][quantity]" class="form-control" onchange="updateTotal(this)" /></td>
        <td><input type="text" name="products[${rowCount}][price]" class="form-control" onchange="updateTotal(this)" /></td>
        <td><input type="text" name="products[${rowCount}][total]" class="form-control" readonly /></td>
        <td><button type="button" class="btn btn-danger remove-product-btn">Remove</button></td>
    `;
    
    tableBody.appendChild(newRow);
    attachRemoveListener();
});

// Function to update the total price of a product row
function updateTotal(input) {
    const row = input.closest("tr");
    const quantity = row.querySelector("[name*='[quantity]']").value;
    const price = row.querySelector("[name*='[price]']").value;
    const total = row.querySelector("[name*='[total]']");
    
    if (quantity && price) {
        total.value = (quantity * price).toFixed(2); // Calculate total price
    }
}

// Function to handle removing a product row
function attachRemoveListener() {
    const removeBtns = document.querySelectorAll(".remove-product-btn");
    removeBtns.forEach(btn => {
        btn.addEventListener("click", function() {
            btn.closest("tr").remove();
        });
    });
}

document.addEventListener("DOMContentLoaded", function() {
    attachRemoveListener();
});

