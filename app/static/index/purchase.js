function initPurchase() {
  const modalButtons = document.querySelectorAll(".purchase-button");

  modalButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const productId = this.getAttribute("data-product-id");
      console.log("Product ID: ", productId);
    });
  });
}
