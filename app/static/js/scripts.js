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

//  planner scripts

document.addEventListener('DOMContentLoaded', function () {
    const addCashFlowButton = document.getElementById('add-selected-cash-flows');
    const selectedCashFlowsTable = document.getElementById('selected-cash-flows-table');
    const selectAllCashFlowsButton = document.getElementById('select-all-cash-flows');
    const removeAllCashFlowsButton = document.getElementById('remove-all-cash-flows');
    const searchBox = document.getElementById('search-cash-flows');
    const cashFlowsTableBody = document.getElementById('cash-flows-table-body');
    // const cashFlowCheckboxes = document.querySelectorAll('.cash-flow-checkbox');

    const addBillButton = document.getElementById('add-selected-bills');
    const selectedBillsTable = document.getElementById('selected-bills-table');
    const totalsField = document.getElementById('totals-amount-field');
    const selectAllButton = document.getElementById('select-all-bills');
    const removeAllButton = document.getElementById('remove-all-bills');

    const totalBillsField = document.getElementById('totals-amount-field');
    const cashFlowTotalsField = document.getElementById('total-cash-flows-amount-field');
    const cashFlowMinusBillsField = document.getElementById('cash-flows-minus-bills');

    let filteredRows = Array.from(cashFlowsTableBody.rows);  // Cache the rows to handle filtered results

    // Handle adding selected cash flows to the planner table
    addCashFlowButton.addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('.cash-flow-checkbox:checked');
        const formContainer = document.getElementById('cash-flows-fields-container'); // Container for hidden inputs
        let index = formContainer.childElementCount / 2; // Assuming 2 inputs per cash flow (name, amount)
        
        checkboxes.forEach(checkbox => {
            const cashFlowId = checkbox.dataset.id;
            const amount = parseFloat(checkbox.dataset.amount);
            const cashFlowName = checkbox.closest('tr').cells[1].textContent;
        
            // Add new row with cash flow info
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${cashFlowName}</td>
                <td>₱${amount.toFixed(2)}</td>
                <td><button type="button" class="btn btn-danger remove-btn">Remove</button></td>
            `;
        
            // Add the hidden input for cash flow ID directly inside the row
            const idInput = document.createElement('input');
            idInput.type = 'hidden';
            idInput.name = `cash_flows-${index}-cash_flow_id`;
            idInput.value = cashFlowId;
            row.appendChild(idInput);
        
            row.querySelector('.remove-btn').addEventListener('click', function () {
                row.remove();
        
                // Remove corresponding hidden inputs in the form container
                formContainer.querySelector(`[name="cash_flows-${index}-cash_flow_name"]`).remove();
                formContainer.querySelector(`[name="cash_flows-${index}-amount"]`).remove();
                formContainer.querySelector(`[name="cash_flows-${index}-cash_flow_id]"`).remove();
        
                updateTotal();
            });
        
            selectedCashFlowsTable.appendChild(row);
        
            // Add hidden inputs for cash flows (name and amount)
            const nameInput = document.createElement('input');
            nameInput.type = 'hidden';
            nameInput.name = `cash_flows-${index}-cash_flow_name`;
            nameInput.value = cashFlowName;
        
            const amountInput = document.createElement('input');
            amountInput.type = 'hidden';
            amountInput.name = `cash_flows-${index}-amount`;
            amountInput.value = amount;
        
            formContainer.appendChild(nameInput);
            formContainer.appendChild(amountInput);
        
            index++;
            checkbox.checked = false; // Uncheck the checkbox
        });
        
        selectAllCashFlowsButton.checked = false;
        updateTotal(); // Update totals
    });
    
    
    

    // Update the total calculation
    function updateTotal() {
        let total = 0;
        let totalBills = 0;

        // Sum up all allocations for cash flows
        const rows = selectedCashFlowsTable.querySelectorAll('tr');
        rows.forEach(row => {
            const amount = parseFloat(row.cells[1].textContent.replace('₱', '').trim()) || 0;
            total += amount;
        });

        // Update the total field for cash flows
        cashFlowTotalsField.value = `₱${total.toFixed(2)}`;

        // Sum up all bills and their allocations
        const rowsBills = selectedBillsTable.querySelectorAll('tr');
        rowsBills.forEach(row => {
            const amount = parseFloat(row.cells[1].textContent.replace('₱', '').trim()) || 0;
            const allocationInput = row.querySelector('.allocation-input');
            const allocationAmount = allocationInput ? parseFloat(allocationInput.value) : 0;
            totalBills += allocationAmount;  // Use the allocation amount
        });

        // Update the total field for bills
        totalBillsField.value = `₱${totalBills.toFixed(2)}`;

        // Calculate the difference between cash flows and bills
        const cashFlowMinusBillsValue = total - totalBills;
        cashFlowMinusBillsField.value = `₱${cashFlowMinusBillsValue.toFixed(2)}`;
    }

    // Select or deselect all checkboxes for cash flows based on visibility
    selectAllCashFlowsButton.addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('.cash-flow-checkbox');
        const isAllChecked = Array.from(filteredRows).every(row => row.querySelector('.cash-flow-checkbox').checked);

        filteredRows.forEach(row => {
            const checkbox = row.querySelector('.cash-flow-checkbox');
            checkbox.checked = !isAllChecked; // Toggle the state for visible rows
        });
    });

    // Remove all selected cash flows from the planner table
    removeAllCashFlowsButton.addEventListener('click', function () {
        const rows = selectedCashFlowsTable.querySelectorAll('tr');
        rows.forEach(row => row.remove());
        updateTotal(); // Update total after removing all rows
    });

    // Search functionality for cash flows
    searchBox.addEventListener('input', function () {
        const searchTerm = searchBox.value.toLowerCase();
        filteredRows = Array.from(cashFlowsTableBody.rows).filter(row => {
            const cashFlowName = row.cells[1].textContent.toLowerCase();
            if (cashFlowName.includes(searchTerm)) {
                row.style.display = '';
                return true;  // Row matches search term
            } else {
                row.style.display = 'none';
                return false;  // Row doesn't match search term
            }
        });
        
        updateSelectAllState();
    });

    // Update the "Select All" button state based on visible rows
    function updateSelectAllState() {
        const checkboxes = document.querySelectorAll('.cash-flow-checkbox');
        const allVisibleChecked = filteredRows.every(row => row.style.display === 'none' || row.querySelector('.cash-flow-checkbox').checked);
        
        selectAllCashFlowsButton.disabled = filteredRows.length === 0; // Disable if no rows are visible
        selectAllCashFlowsButton.textContent = allVisibleChecked ? 'Deselect All' : 'Select All';
    }

    // Initialize the state for select all button when page loads
    updateSelectAllState();
});

document.addEventListener('DOMContentLoaded', function () {
    const addBillButton = document.getElementById('add-selected-bills');
    const selectedBillsTable = document.getElementById('selected-bills-table');
    const totalsField = document.getElementById('totals-amount-field');
    const selectAllButton = document.getElementById('select-all-bills');
    const removeAllButton = document.getElementById('remove-all-bills');

    const addCashFlowButton = document.getElementById('add-selected-cash-flows');
    const selectedCashFlowsTable = document.getElementById('selected-cash-flows-table');
    const selectAllCashFlowsButton = document.getElementById('select-all-cash-flows');
    const removeAllCashFlowsButton = document.getElementById('remove-all-cash-flows');
    const searchBox = document.getElementById('search-cash-flows');
    const cashFlowsTableBody = document.getElementById('cash-flows-table-body');

    const totalBillsField = document.getElementById('totals-amount-field');
    const cashFlowTotalsField = document.getElementById('total-cash-flows-amount-field');
    const cashFlowMinusBillsField = document.getElementById('cash-flows-minus-bills');
    const billsMinusCashFlowValueField = document.getElementById('bills-minus-cash-flows');
    
    // Handle the search filter for bills
    document.getElementById('search-bills').addEventListener('input', function () {
        const searchValue = this.value.toLowerCase();
        const rows = document.querySelectorAll('#bills-table-body tr');

        rows.forEach(row => {
            const billNameCell = row.cells[1]; // Bill name in second column
            const billName = billNameCell.textContent.toLowerCase();
            row.style.display = billName.includes(searchValue) ? '' : 'none';
        });

        // Update the Select All state after search
        updateSelectAllState();
    });

    // Handle adding selected bills to the planner table
    addBillButton.addEventListener('click', function () {
        const checkboxes = document.querySelectorAll('.bill-checkbox:checked');
        const billsFieldsContainer = document.getElementById('bills-fields-container'); // For dynamically adding hidden fields

        checkboxes.forEach(checkbox => {
            const billId = checkbox.dataset.id;
            const amount = parseFloat(checkbox.dataset.amount);
            const billName = checkbox.closest('tr').cells[1].textContent;

            // Create a new row in the Selected Bills table
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${billName}</td>
                <td>₱${amount.toFixed(2)}</td>
                <td><input type="number" class="form-control allocation-input" placeholder="Set Budget" value="${amount.toFixed(2)}"></td>
                <td><button type="button" class="btn btn-danger remove-btn">Remove</button></td>
                <input type="hidden" name="bills-${billId}[bill_id]" value="${billId}">
            `;

            // Add event listener for removing a row
            row.querySelector('.remove-btn').addEventListener('click', function () {
                row.remove(); // Remove the row
                document.querySelector(`#bills-${billId}`).remove(); // Remove the hidden field
                updateTotal(); // Recalculate total when a row is removed
            });

            selectedBillsTable.appendChild(row);

            // Add a hidden field to the form for this bill
            const index = billsFieldsContainer.children.length; // Determine next field index
            const hiddenFields = document.createElement('div');
            hiddenFields.id = `bills-${billId}`; // ID to track and remove dynamically
            hiddenFields.innerHTML = `
                <input type="hidden" name="bills-${index}-bill_id" value="${billId}">
                <input type="hidden" name="bills-${index}-bill_name" value="${billName}">
                <input type="hidden" name="bills-${index}-amount" value="${amount.toFixed(2)}">
                <input type="hidden" name="bills-${index}-allocation" value="${amount.toFixed(2)}">
            `;

            billsFieldsContainer.appendChild(hiddenFields);

            // Uncheck the checkbox after adding
            checkbox.checked = false;
        });

        selectAllButton.checked = false; // Uncheck "Select All" after adding
        updateTotal(); // Update the total amounts
    });


    // Update the total calculation
    function updateTotal() {
        let total = 0;
        let totalBills = 0;

        // Sum up all allocations for cash flows
        const rows = selectedCashFlowsTable.querySelectorAll('tr');
        rows.forEach(row => {
            const amount = parseFloat(row.cells[1].textContent.replace('₱', '').trim()) || 0;
            total += amount;
        });

        // Update the total field for cash flows
        cashFlowTotalsField.value = `₱${total.toFixed(2)}`;

        // Sum up all bills and their allocations
        const rowsBills = selectedBillsTable.querySelectorAll('tr');
        rowsBills.forEach(row => {
            const amount = parseFloat(row.cells[1].textContent.replace('₱', '').trim()) || 0;
            const allocationInput = row.querySelector('.allocation-input');
            const allocationAmount = allocationInput ? parseFloat(allocationInput.value) : 0;
            totalBills += allocationAmount;
        });

        // Update the total field for bills
        totalBillsField.value = `₱${totalBills.toFixed(2)}`;

        // Calculate the difference between cash flows and bills
        const cashFlowMinusBillsValue = total - totalBills;
        cashFlowMinusBillsField.value = `₱${cashFlowMinusBillsValue.toFixed(2)}`;

        const billsMinusCashFlowValue = totalBills - total;
        billsMinusCashFlowValueField.value = `₱${billsMinusCashFlowValue.toFixed(2)}`;

    }

    // Listen for changes in allocation inputs to update total
    selectedBillsTable.addEventListener('input', function (event) {
        if (event.target.classList.contains('allocation-input')) {
            updateTotal(); // Recalculate total when an allocation input changes
        }
    });

    // Select or deselect all checkboxes
    selectAllButton.addEventListener('change', function () {
        const checkboxes = document.querySelectorAll('.bill-checkbox');
        const visibleCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.closest('tr').style.display !== 'none');
        const isAllChecked = visibleCheckboxes.every(checkbox => checkbox.checked);

        visibleCheckboxes.forEach(checkbox => {
            checkbox.checked = !isAllChecked;
        });
    });

    // Remove all selected bills from the planner table
    removeAllButton.addEventListener('click', function () {
        const rows = selectedBillsTable.querySelectorAll('tr');
        rows.forEach(row => row.remove());
        updateTotal(); // Update total after removing all rows
    });

    // Update Select All checkbox state based on visible rows
    function updateSelectAllState() {
        const checkboxes = document.querySelectorAll('.bill-checkbox');
        const visibleCheckboxes = Array.from(checkboxes).filter(checkbox => checkbox.closest('tr').style.display !== 'none');
        const selectedRows = visibleCheckboxes.filter(checkbox => checkbox.checked);

        selectAllButton.checked = visibleCheckboxes.length === selectedRows.length;
    }

    // Listen for individual checkboxes changes to update Select All state
    document.querySelector('#bills-table-body').addEventListener('change', function (event) {
        if (event.target.classList.contains('bill-checkbox')) {
            updateSelectAllState(); // Update the Select All state
        }
    });
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