function getSupplierInventory() {
  const modalButtons = document.querySelectorAll(".supplier-button");

  modalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const supplierId = this.getAttribute("data-supplier-id");
      const companyName = this.getAttribute("data-supplier-company_name");
      const supplierName = this.getAttribute("data-supplier-supplier_name");
      const supplierEmail = this.getAttribute("data-supplier-email");
      const supplierPhone = this.getAttribute("data-supplier-phone");
      const supplierStatus = this.getAttribute("data-supplier-status");

      const editTitle = document.querySelector("#edit-title");
      const deleteTitle = document.querySelector("#delete-title");

      if (this.title === "Supplier Edit") {
        console.log("Edit button clicked");
        editTitle.textContent = `Editing ${supplierName} from ${companyName}`;
        const editForm = document.getElementById("editSupplierForm");
        if (!editForm) {
          return;
        }

        editForm.action = `/suppliers/edit/${supplierId}`;

        const fields = {
          company_name: companyName,
          supplier_name: supplierName,
          email: supplierEmail,
          phone: supplierPhone,
          status: supplierStatus,
        };

        for (const [id, value] of Object.entries(fields)) {
          const field = document.getElementById(id);
          if (field) {
            field.value = value;
          }
        }
      } else if (this.title == "Supplier Delete") {
        deleteTitle.textContent = `Remove ${supplierName} from ${companyName}?`;
        const deleteForm = document.getElementById("deleteSupplierForm");
        if (!deleteForm) {
          return;
        }
        deleteForm.action = `/suppliers/delete/${supplierId}`;
      }
    });
  });
}
