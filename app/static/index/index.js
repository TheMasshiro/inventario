document.addEventListener("DOMContentLoaded", () => {
  initTermsAndConditions();
  initPasswordToggle();
  initNavbarBurger();
  initModals();
});

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
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button",
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
  $el.classList.add("is-active");
}

function closeModal($el) {
  $el.classList.remove("is-active");
}

function closeAllModals() {
  (document.querySelectorAll(".modal") || []).forEach(closeModal);
}
