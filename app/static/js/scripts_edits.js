document.addEventListener('DOMContentLoaded', function () {
    const productsTable = document.querySelector("#products-table tbody");
    const addProductBtn = document.getElementById("add-product-btn");
    const productsInput = document.getElementById("products-input");

    const deductionsTable = document.querySelector("#deductions-table tbody");
    const addDeductionsBtn = document.getElementById("add-deductions-btn");
    const deductionsInput = document.getElementById("deductions-input");

    const chargesTable = document.querySelector("#charges-table tbody");
    const addChargesBtn = document.getElementById("add-charges-btn");
    const chargesInput = document.getElementById("charges-input");

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

    // Attach row listeners to all existing rows after page loads
    function attachListenersToAllRows(table) {
        const rows = table.querySelectorAll("tr");
        rows.forEach(row => {
            attachRowListeners(row);
        });
    }

    // Add a product row when the "Add" button is clicked
    addProductBtn.addEventListener("click", function () {
        addProductRow();
    });

    // Handle the "Remove" button click for products
    productsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-product-btn")) {
            const row = e.target.closest("tr");
            row.remove();
            updateRowNames(productsTable);

            // If no rows are left, add an empty row
            if (productsTable.children.length === 0) {
                addProductRow();
            }
        }
    });

    // Add a deduction row when the "Add" button is clicked
    addDeductionsBtn.addEventListener("click", function () {
        addDeductionsRow();
    });

    // Handle the "Remove" button click for deductions
    deductionsTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-deduction-btn")) {
            const row = e.target.closest("tr");
            row.remove();
            updateRowNames(deductionsTable);

            // If no rows are left, add an empty row
            if (deductionsTable.children.length === 0) {
                addDeductionsRow();
            }
        }
    });

    // Add a charge row when the "Add" button is clicked
    addChargesBtn.addEventListener("click", function () {
        addChargesRow();
    });

    // Handle the "Remove" button click for charges
    chargesTable.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-charge-btn")) {
            const row = e.target.closest("tr");
            row.remove();
            updateRowNames(chargesTable);

            // If no rows are left, add an empty row
            if (chargesTable.children.length === 0) {
                addChargesRow();
            }
        }
    });

    // Serialize form data into the hidden input on form submission
    document.querySelector("form").addEventListener("submit", function () {
        const rows = productsTable.querySelectorAll("tr");
        const products = Array.from(rows).map(row => ({
            product_name: row.querySelector("input[name*='[product_name]']").value,
            product_type: row.querySelector("input[name*='[product_type]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));
        productsInput.value = JSON.stringify(products);

        const deductionRows = deductionsTable.querySelectorAll("tr");
        const deductions = Array.from(deductionRows).map(row => ({
            deduction_name: row.querySelector("input[name*='[deduction_name]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));
        deductionsInput.value = JSON.stringify(deductions);

        const chargeRows = chargesTable.querySelectorAll("tr");
        const charges = Array.from(chargeRows).map(row => ({
            charge_name: row.querySelector("input[name*='[charge_name]']").value,
            quantity: row.querySelector("input[name*='[quantity]']").value,
            price: row.querySelector("input[name*='[price]']").value,
            total: row.querySelector("input[name*='[total]']").value,
        }));
        chargesInput.value = JSON.stringify(charges);
    });

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
                <input type="number" name="products[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-product-btn" id="remove-deduction-btn">Remove</button>
            </td>
        `;
        productsTable.appendChild(newRow);
        attachRowListeners(newRow);

        // Log names and IDs of the form fields in the newly added row
        const inputs = newRow.querySelectorAll("input");
        inputs.forEach(input => {
            console.log(`Field Name: ${input.name}, Field ID: ${input.id}`);
        });
    }

    // Function to add a new deduction row
    function addDeductionsRow() {
        const rowCount = deductionsTable.children.length;
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="deductions[${rowCount}][deduction_name]" class="form-control" placeholder="Deduction Name" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="number" name="deductions[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-deduction-btn" id="remove-deduction-btn">Remove</button>
            </td>
        `;
        deductionsTable.appendChild(newRow);
        attachRowListeners(newRow);
    }

    // Function to add a new charge row
    function addChargesRow() {
        const rowCount = chargesTable.children.length;
        const newRow = document.createElement("tr");
        newRow.innerHTML = `
            <td>
                <input type="text" name="charges[${rowCount}][charge_name]" class="form-control" placeholder="Charge Name" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][quantity]" class="form-control" placeholder="Quantity" min="1" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][price]" class="form-control" placeholder="Price" step="0.01" min="0" required />
            </td>
            <td>
                <input type="number" name="charges[${rowCount}][total]" class="form-control" placeholder="Total" readonly />
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-charge-btn" id="remove-deduction-btn">Remove</button>
            </td>
        `;
        chargesTable.appendChild(newRow);
        attachRowListeners(newRow);
    }

    // Update row input names after a row is removed
    function updateRowNames(table) {
        const rows = table.querySelectorAll("tr");
        rows.forEach((row, index) => {
            row.querySelectorAll("input").forEach(input => {
                const name = input.name.replace(/\[\d+\]/, `[${index}]`);
                input.name = name;
            });
        });
    }

    // Add an initial row if no rows exist
    if (productsTable.children.length === 0) {
        addProductRow();
    }
    if (deductionsTable.children.length === 0) {
        addDeductionsRow();
    }
    if (chargesTable.children.length === 0) {
        addChargesRow();
    }

    // Ensure that row listeners are attached to all existing rows
    attachListenersToAllRows(productsTable);
    attachListenersToAllRows(deductionsTable);
    attachListenersToAllRows(chargesTable);
    
    // Add event listener to log name and id when an input field is clicked
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('click', function () {
            console.log(`Field Name: ${input.name}, Field ID: ${input.id}`);
        });
    });

});
