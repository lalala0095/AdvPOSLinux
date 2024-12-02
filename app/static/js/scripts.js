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

// for planner
document.addEventListener('DOMContentLoaded', function () {
    const addBillButton = document.getElementById('add-bill-btn');
    const selectedBillsTable = document.getElementById('selected-bills-table');
    const billDropdown = document.querySelector('.bills-dropdown');
    const amountField = document.querySelector('.bills-amount-field');
    const allocationField = document.getElementById('bills-allocation');

    const addCashFlowButton = document.getElementById('add-cash-flow-btn');
    const selectedCashFlowsTable = document.getElementById('selected-cash-flows-table');
    const cashFlowDropdown = document.querySelector('.cash-flows-dropdown');
    const cfamountField = document.getElementById('cash-flows-amount-field');

    const totalsField = document.getElementById('totals-amount-field');
    const cashFlowTotalsField = document.getElementById('total-cash-flows-amount-field');
    const cashFlowMinusBillsField = document.getElementById('total-cash-flows-minus-bills');

    let rowIndex = 1; // Start from 1 to correctly reference the first row

    // Handle dropdown change and autofill amount
    if (billDropdown) {
        billDropdown.addEventListener('change', function () {
            const selectedBill = billDropdown.value;
            if (selectedBill) {
                fetch(`/bills/get_bills_amount?bills=${encodeURIComponent(selectedBill)}`)
                    .then(response => response.json())
                    .then(data => {
                        amountField.value = data.amount || 0; // Populate the amount field
                        allocationField.value = "";
                    })
                    .catch(error => console.error("Error fetching bill amount:", error));
            } else {
                amountField.value = ""; // Clear the amount field
                allocationField.value = "";
            }
        });
    }

    // Handle dropdown change and autofill cash flow amount
    if (cashFlowDropdown) {
        cashFlowDropdown.addEventListener('change', function () {
            const selectedBill = cashFlowDropdown.value;
            if (selectedBill) {
                fetch(`/bills/get_cash_flows_amount?cash_flows=${encodeURIComponent(selectedBill)}`)
                    .then(response => response.json())
                    .then(data => {
                        cfamountField.value = data.amount || 0; // Populate the amount field
                    })
                    .catch(error => console.error("Error fetching bill amount:", error));
            } else {
                cfamountField.value = ""; // Clear the amount field
            }
        });
    }

    // Add a new bill to the table
    addBillButton.addEventListener('click', function () {
        const selectedBill = billDropdown.value;
        const amount = amountField.value;
        const allocation = allocationField.value;

        if (selectedBill && amount) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${billDropdown.options[billDropdown.selectedIndex].text}</td>
                <td>${amount}</td>
                <td class="allocation-cell">${allocation}</td>
                <td><button type="button" class="btn btn-danger remove-btn">x</button></td>
            `;

            // Add the remove button functionality
            const removeButton = row.querySelector('.remove-btn');
            removeButton.addEventListener('click', function () {
                row.remove(); // Remove the row from the table
            });

            // Add the row to the table
            selectedBillsTable.appendChild(row);

            allocationField.value = ""; 

            updateTotal();

        }
    });

    // Add a new cash flow to the table
    addCashFlowButton.addEventListener('click', function () {
        const selectedCashFlowsTable = document.getElementById('selected-cash-flows-table');
        const amount = cfamountField.value;

        if (selectedCashFlowsTable && amount) {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cashFlowDropdown.options[cashFlowDropdown.selectedIndex].text}</td>
                <td class="cash-flow-amount-cell">${amount}</td>
                <td><button type="button" class="btn btn-danger remove-btn">x</button></td>
            `;

            // Add the remove button functionality
            const removeButton = row.querySelector('.remove-btn');
            removeButton.addEventListener('click', function () {
                row.remove(); // Remove the row from the table
            });

            // Add the row to the table
            selectedCashFlowsTable.appendChild(row);
            updateTotal();
        }
    });
    
    // Update the total allocation
    function updateTotal() {
        let total = 0;
        let cashFlowTotal = 0;
        let cashFlowMinusTotalBills = 0;

        // Select all cells containing the allocations
        const allocationCells = document.querySelectorAll('.allocation-cell');
        const cashFlowCells = document.querySelectorAll('.cash-flow-amount-cell');
        allocationCells.forEach(function(cell) {
            const allocation = parseFloat(cell.textContent) || 0; // Get the allocation value, default to 0
            console.log(allocation)
            total += allocation;
        });

        cashFlowCells.forEach(function(cell) {
            const cashFlowAmount = parseFloat(cell.textContent) || 0; // Get the allocation value, default to 0
            console.log(cashFlowAmount)
            cashFlowTotal += cashFlowAmount;
        });

        // Update the totals field with the calculated total
        totalsField.value = total.toFixed(2);
        cashFlowTotalsField.value =  cashFlowTotal.toFixed(2);
        total_value_final = "₱" + total.toFixed(2);
        total_cashflow_value_final = "₱" + cashFlowTotal.toFixed(2);
        
        totalsField.value = "₱" + total.toFixed(2);
        cashFlowTotalsField.value = total_cashflow_value_final;

        cashFlowMinusBillsField.value = "₱" + (cashFlowTotal - total).toFixed(2);
    }
});


//  for bills_add
document.addEventListener('DOMContentLoaded', function () {
    // Get the bill name dropdown element
    const billNameDropdown = document.getElementById('bill_name_dropdown');
    const amountField = document.getElementById('amount_field');
    const billsDropdown = document.getElementById('bills_dropdown');
    const billsAmountField = document.getElementById('bills_amount_field');

    // Event listener for change event on the dropdown
    if (billNameDropdown) {
        billNameDropdown.addEventListener('change', function () {
            const selectedBill = billNameDropdown.value;
            console.log("Selected bill name:", selectedBill);  // Debug log
            
            if (selectedBill) {
                // Make the API call using Fetch
                fetch('/bills/get_amount?bill_name=' + encodeURIComponent(selectedBill))
                    .then(response => response.json())  // Parse the JSON response
                    .then(data => {
                        console.log(data);  // Debug log for the response
                        amountField.value = data.amount;  // Set the amount in the input field
                    })
                    .catch(error => {
                        console.error("Error fetching amount:", error);
                        alert("Failed to fetch amount: " + error.message);
                    });
            } else {
                console.log("No bill selected");
            }
        });    
    }

    // Event listener for change event on the dropdown
    if (billsDropdown) {
        billsDropdown.addEventListener('change', function () {
            const selectedBill = billsDropdown.value;
            console.log("Selected bill name:", selectedBill);  // Debug log
            
            if (selectedBill) {
                // Make the API call using Fetch
                fetch('/bills/get_bills_amount?bills=' + encodeURIComponent(selectedBill))
                    .then(response => response.json())  // Parse the JSON response
                    .then(data => {
                        console.log(data);  // Debug log for the response
                        billsAmountField.value = data.amount;  // Set the amount in the input field
                    })
                    .catch(error => {
                        console.error("Error fetching amount:", error);
                        alert("Failed to fetch amount: " + error.message);
                    });
            } else {
                console.log("No bill selected");
            }
        });
    }
});

// products adding in orders form
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
                <button id="remove-button" type="button" class="btn btn-danger remove-product-btn">x</button>
            </td>
        `;
        productsTable.appendChild(newRow);

        attachRowListeners(newRow);
    });


    // Remove product rows dynamically and add a new row if all rows are removed
    productsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-product-btn")) {
            e.target.closest("tr").remove();
            updateRowNames();

            // Automatically add a new row if no rows remain
            if (productsTable.children.length === 0) {
                addProductRow();
                const removeButton = document.getElementsByName("products[0][remove-button]");
                removeButton.disabled = true;
            }
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

        // Enable or disable "Remove" buttons based on the number of rows
    function toggleRemoveButtonState() {
        const rows = productsTable.querySelectorAll("tr");
        rows.forEach((row, index) => {
            const removeButton = row.querySelector(".remove-product-btn");
            removeButton.disabled = rows.length === 1; // Disable if it's the only row
        });
    }
    
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

    // Function to add a new product row
    function addProductRow() {
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
                <button name="remove-product-btn" type="button" class="btn btn-danger remove-product-btn">x</button>
            </td>
        `;
        productsTable.appendChild(newRow);

        attachRowListeners(newRow);
        
        if (productsTable.children.length === 0) {
            addProductRow();
            const removeButton = document.getElementsByName("products[0][remove-button]");
            removeButton.disabled = true;            }
    }

    // Add an initial row if none exist
    if (productsTable.children.length === 0) {
        addProductRow();
        const removeButton = document.getElementsByName("products[0][remove-button]");
        removeButton.disabled = true;        
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const statusField = document.getElementById('status');
    const dateSoldContainer = document.getElementById('date-sold-container');
    const dateCancelledContainer = document.getElementById('date-cancelled-container');
    const datePaidContainer = document.getElementById('date-payment-container');

    // Hide all containers first
    dateSoldContainer.style.display = 'none';
    dateCancelledContainer.style.display = 'none';
    datePaidContainer.style.display = 'none';
    
    // Function to toggle the visibility of the date-related fields based on status
    function toggleDateSoldField() {
        const statusValue = document.getElementById('status').value;

        // Show the appropriate field based on the status value
        if (statusValue === 'Sold') {
            dateSoldContainer.style.display = 'block';
            datePaidContainer.style.display = 'block';
            dateCancelledContainer.style.display = 'none';
        } else if (statusValue === 'Cancelled') {
            dateSoldContainer.style.display = 'none';
            datePaidContainer.style.display = 'none';
            dateCancelledContainer.style.display = 'block';
        } else if (statusValue === 'Awaiting Payment') {
            dateSoldContainer.style.display = 'none';
            datePaidContainer.style.display = 'block';
            dateCancelledContainer.style.display = 'none';
        } else {
            dateSoldContainer.style.display = 'none';
            datePaidContainer.style.display = 'none';
            dateCancelledContainer.style.display = 'none';
        }
    }

    // Listen for changes to the status field and toggle the visibility of date-related fields
    if (statusField) {
        statusField.addEventListener('change', toggleDateSoldField);
    }

    // Initial check when the page loads (in case the status is already set)
    toggleDateSoldField();
});


// // // // // this part goes the deductions form 
document.addEventListener('DOMContentLoaded', function () {
    const deductionsTable = document.querySelector("#deductions-table tbody");
    const addDeductionsBtn = document.getElementById("add-deductions-btn");
    const deductionsInput = document.getElementById("deductions-input");

    // Add a deductions row when the "Add" button is clicked
    addDeductionsBtn.addEventListener("click", function () {
        const rowCount = deductionsTable.children.length;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="deductions[${rowCount}][deductions_name]" class="form-control" placeholder="Deductions Name" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="text" name="deductions[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-deductions-btn">x</button>
            </td>
        `;
        deductionsTable.appendChild(newRow);

        attachRowListeners(newRow);
    });


    // Remove deductions rows dynamically and add a new row if all rows are removed
    deductionsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-deductions-btn")) {
            e.target.closest("tr").remove();
            updateRowNames();

            // Automatically add a new row if no rows remain
            if (deductionsTable.children.length === 0) {
                addDeductionsRow();
            }
        }
    });


    // Serialize form data into the hidden input on form submission
    document.querySelector("form").addEventListener("submit", function (e) {
        const rows = deductionsTable.querySelectorAll("tr");
        const deductions = Array.from(rows).map(row => ({
            deductions_name: row.querySelector("input[name*='[deductions_name]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));

        // Set the serialized JSON into the hidden input
        deductionsInput.value = JSON.stringify(deductions);
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
        const rows = deductionsTable.querySelectorAll("tr");
        rows.forEach((row, index) => {
            row.querySelectorAll("input").forEach(input => {
                const name = input.name.replace(/\[\d+\]/, `[${index}]`);
                input.name = name;
            });
        });
    }

    // Function to add a new deductions row
    function addDeductionsRow() {
        const rowCount = deductionsTable.children.length;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="deductions[${rowCount}][deductions_name]" class="form-control" placeholder="Deductions Name" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="text" name="deductions[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-deductions-btn">x</button>
            </td>
        `;
        deductionsTable.appendChild(newRow);

        attachRowListeners(newRow);
    }

    // Add an initial row if none exist
    if (deductionsTable.children.length === 0) {
        addDeductionsRow();
    }
});



// this part goes the charges form 
document.addEventListener('DOMContentLoaded', function () {
    const chargesTable = document.querySelector("#charges-table tbody");
    const addChargesBtn = document.getElementById("add-charges-btn");
    const chargesInput = document.getElementById("charges-input");

    // Add a charges row when the "Add" button is clicked
    addChargesBtn.addEventListener("click", function () {
        const rowCount = chargesTable.children.length;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="charges[${rowCount}][charges_name]" class="form-control" placeholder="Charges Name" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="text" name="charges[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-charges-btn">x</button>
            </td>
        `;
        chargesTable.appendChild(newRow);

        attachRowListeners(newRow);
    });


    // Remove charges rows dynamically and add a new row if all rows are removed
    chargesTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-charges-btn")) {
            e.target.closest("tr").remove();
            updateRowNames();

            // Automatically add a new row if no rows remain
            if (chargesTable.children.length === 0) {
                addChargesRow();
            }
        }
    });


    // Serialize form data into the hidden input on form submission
    document.querySelector("form").addEventListener("submit", function (e) {
        const rows = chargesTable.querySelectorAll("tr");
        const charges = Array.from(rows).map(row => ({
            charges_name: row.querySelector("input[name*='[charges_name]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));

        // Set the serialized JSON into the hidden input
        chargesInput.value = JSON.stringify(charges);
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
        const rows = chargesTable.querySelectorAll("tr");
        rows.forEach((row, index) => {
            row.querySelectorAll("input").forEach(input => {
                const name = input.name.replace(/\[\d+\]/, `[${index}]`);
                input.name = name;
            });
        });
    }

    // Function to add a new charges row
    function addChargesRow() {
        const rowCount = chargesTable.children.length;

        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="charges[${rowCount}][charges_name]" class="form-control" placeholder="Charges Name" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="text" name="charges[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-charges-btn">x</button>
            </td>
        `;
        chargesTable.appendChild(newRow);

        attachRowListeners(newRow);
    }

    // Add an initial row if none exist
    if (chargesTable.children.length === 0) {
        addChargesRow();
    }
});

// Safely pass Python data as JSON
const products = JSON.parse('{{ record["products"] | tojson | safe }}');
const charges = JSON.parse('{{ record["charges"] | tojson | safe }}');
const deductions = JSON.parse('{{ record["deductions"] | tojson | safe }}');

// Populate products
products.forEach(product => {
addProductRow(product.product_name, product.product_type, product.quantity, product.price, product.total);
});

// Populate charges
charges.forEach(charge => {
addChargeRow(charge.charge_name, charge.quantity, charge.price, charge.total);
});

// Populate deductions
deductions.forEach(deduction => {
addDeductionRow(deduction.deduction_name, deduction.quantity, deduction.price, deduction.total);
});