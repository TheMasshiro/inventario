function getItemInventory() {
  const modalButtons = document.querySelectorAll(".inventory-button");

  modalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.getAttribute("data-product-id");
      const productName = this.getAttribute("data-product-name");
      const productPrice = this.getAttribute("data-product-price");
      const productStock = this.getAttribute("data-product-stock");
      const productSupplier = this.getAttribute("data-product-supplier");

      const editTitle = document.querySelector("#edit-title");
      const deleteTitle = document.querySelector("#delete-title");

      if (this.title === "Inventory Edit") {
        editTitle.textContent = `Editing ${productName}`;
        const editForm = document.getElementById("editInventoryForm");
        if (!editForm) {
          return;
        }

        editForm.action = `/inventory/edit/${productId}`;

        const fields = {
          product_name: productName,
          price: productPrice,
          stock: productStock,
          supplier_name: productSupplier,
        };

        for (const [id, value] of Object.entries(fields)) {
          const field = document.getElementById(id);
          if (field) {
            field.value = value;
          }
        }
      } else if (this.title === "Inventory Delete") {
        deleteTitle.textContent = `Remove ${productName}?`;
        const deleteForm = document.getElementById("deleteInventoryForm");
        if (!deleteForm) {
          return;
        }
        deleteForm.action = `/inventory/delete/${productId}`;
      }
    });
  });
}
