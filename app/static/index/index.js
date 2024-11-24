document.addEventListener("DOMContentLoaded", () => {
  initTermsAndConditions();
  initPasswordToggle();
  initNavbarBurger();
  initModals();
  initNotification();
  getItemInventory();
  getSupplierInventory();
  getCustomerInventory();
  initSearch("product");
  initSearch("supplier");
  initSearch("customer");
  initSearch("purchase");
  calculateProductTotal();
});

function calculateProductTotal() {
  const formatCurrency = (value) => {
    return `₱${value.toLocaleString("en-US", {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })}`;
  };

  const rows = document.querySelectorAll("tr#purchase-tr");
  const grandTotalElement = document.getElementById("grand-total");
  let grandTotal = 0;

  rows.forEach((row) => {
    const quantityInput = row
      .querySelector('input[name="product_id"]')
      ?.parentElement?.querySelector('input[type="number"]');
    const priceCell = row.querySelector("td:nth-child(2)");
    const totalSpan = row.querySelector('span[id^="total-"]');

    if (quantityInput && priceCell && totalSpan) {
      const priceText = priceCell.textContent.trim();
      const price = parseFloat(priceText.replace(/[^0-9.-]+/g, ""));

      quantityInput.addEventListener("input", function () {
        const quantity = parseInt(this.value) || 0;
        const total = price * quantity;
        totalSpan.textContent = formatCurrency(total);

        // Recalculate grand total
        grandTotal = 0;
        rows.forEach((r) => {
          const rowTotal = r.querySelector('span[id^="total-"]').textContent;
          const value = parseFloat(rowTotal.replace(/[^0-9.-]+/g, ""));
          grandTotal += value;
        });

        grandTotalElement.textContent = `Grand Total: ${formatCurrency(grandTotal)}`;
      });
    }
  });
}

function adjustStock(button, adjustment) {
  const input = button.closest(".field").querySelector("input");
  let currentValue = parseInt(input.value, 10);
  if (isNaN(currentValue)) currentValue = 0;

  const maxValue = parseInt(input.getAttribute("max"), 10);
  const minValue = parseInt(input.getAttribute("min"), 10);

  let newValue = currentValue + adjustment;

  if (newValue > maxValue) {
    newValue = maxValue;
  }
  if (newValue < minValue) {
    newValue = minValue;
  }

  input.value = newValue;
}

function initTermsAndConditions() {
  const agreeButton = document.getElementById("agree-to-terms");
  const termsCheckbox = document.querySelector("#terms-checkbox input");

  if (agreeButton && termsCheckbox) {
    agreeButton.addEventListener("click", () => {
      termsCheckbox.checked = true;
    });
  }
}

function initPasswordToggle() {
  // Find all password fields
  const passwordFields = document.querySelectorAll(".password-field");

  passwordFields.forEach((input) => {
    const toggleBtn =
      input.parentElement.nextElementSibling.querySelector(".button");
    const icon = toggleBtn.querySelector("i");

    if (toggleBtn) {
      toggleBtn.addEventListener("click", () => {
        const isPassword = input.type === "password";
        input.type = isPassword ? "text" : "password";
        icon.classList.replace(
          `fa-eye${isPassword ? "" : "-slash"}`,
          `fa-eye${isPassword ? "-slash" : ""}`,
        );
      });
    }
  });
}

function initNavbarBurger() {
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0,
  );

  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      const target = el.dataset.target;
      const $target = document.getElementById(target);
      el.classList.toggle("is-active");
      $target.classList.toggle("is-active");
    });
  });
}

function initModals() {
  (document.querySelectorAll(".js-modal-trigger") || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const $target = document.getElementById(modal);
    $trigger.addEventListener("click", () => {
      openModal($target);
    });
  });

  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button[type='button']",
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");
    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeAllModals();
    }
  });
}

function openModal($el) {
  if (typeof $el === "string") {
    $el = document.getElementById($el);
  }
  if ($el) {
    $el.classList.add("is-active");
  }
}

function closeModal($el) {
  if (typeof $el === "string") {
    $el = document.getElementById($el);
  }
  if ($el) {
    $el.classList.remove("is-active");
  }
}

function closeAllModals() {
  (document.querySelectorAll(".modal") || []).forEach(closeModal);
}

function initNotification() {
  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      $delete.addEventListener("click", () => {
        $notification.parentNode.removeChild($notification);
      });
    },
  );
}
