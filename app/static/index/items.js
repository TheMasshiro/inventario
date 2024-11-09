function getItemInventory() {
  const modalButtons = document.querySelectorAll(".js-modal-trigger");
  modalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.getAttribute("data-product-id");
      const productName = this.getAttribute("data-product-name");
      const productPrice = this.getAttribute("data-product-price");
      const productQuantity = this.getAttribute("data-product-quantity");
      const productSupplier = this.getAttribute("data-product-supplier");

      const editTitle = document.querySelector("#edit-title");
      const deleteTitle = document.querySelector("#delete-title");

      if (this.title === "Edit") {
        editTitle.textContent = `Editing ${productName}`;

        const editForm = document.getElementById("editForm");
        editForm.action = `/inventory/edit/${productId}`;

        document.getElementById("product_name").value = productName;
        document.getElementById("price").value = productPrice;
        document.getElementById("quantity").value = productQuantity;
        document.getElementById("supplier_name").value = productSupplier;
      } else if (this.title == "Delete") {
        deleteTitle.textContent = `Remove ${productName}?`;

        const deleteForm = document.getElementById("deleteForm");
        deleteForm.action = `/inventory/delete/${productId}`;
      }
    });
  });
}
