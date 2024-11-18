function getCustomerInventory() {
  const modalButtons = document.querySelectorAll(".customer-button");

  modalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const customerId = this.getAttribute("data-customer-id");
      const customerName = this.getAttribute("data-customer-name");

      const editTitle = document.querySelector("#edit-title");
      const deleteTitle = document.querySelector("#delete-title");

      if (this.title === "Customer Edit") {
        editTitle.textContent = `Editing ${customerName}`;
        const editForm = document.getElementById("editCustomerForm");
        if (!editForm) {
          return;
        }

        editForm.action = `/customer/edit/${customerId}`;

        const fields = {
          customer_name: customerName,
        };

        for (const [id, value] of Object.entries(fields)) {
          const field = document.getElementById(id);
          if (field) {
            field.value = value;
          }
        }
      } else if (this.title === "Customer Delete") {
        deleteTitle.textContent = `Remove ${customerName}?`;
        const deleteForm = document.getElementById("deleteCustomerForm");
        if (!deleteForm) {
          return;
        }
        deleteForm.action = `/customer/delete/${customerId}`;
      }
    });
  });
}
