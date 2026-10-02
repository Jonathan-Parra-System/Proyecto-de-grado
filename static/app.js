document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-password-toggle]").forEach((button) => {
        const input = document.getElementById(button.dataset.passwordToggle);
        if (!input) return;

        button.addEventListener("click", () => {
            const visible = input.type === "password";
            input.type = visible ? "text" : "password";
            button.textContent = visible ? "Ocultar" : "Mostrar";
            button.setAttribute("aria-pressed", String(visible));
        });
    });

    document.querySelectorAll("[data-password-policy]").forEach((input) => {
        input.addEventListener("input", () => {
            const password = input.value;
            let message = "";
            if (password && !/\p{Lu}/u.test(password)) {
                message = "Incluye al menos una letra mayúscula.";
            } else if (password && !/[^\p{L}\p{N}\s]/u.test(password)) {
                message = "Incluye al menos un símbolo.";
            } else if (/\d{3,}/.test(password) && hasConsecutiveDigits(password)) {
                message = "No uses tres números consecutivos, como 123 o 321.";
            }
            input.setCustomValidity(message);
        });
    });
});

function hasConsecutiveDigits(value) {
    for (let index = 0; index <= value.length - 3; index += 1) {
        const digits = value.slice(index, index + 3);
        if (!/^\d{3}$/.test(digits)) continue;
        const firstStep = Number(digits[1]) - Number(digits[0]);
        const secondStep = Number(digits[2]) - Number(digits[1]);
        if (Math.abs(firstStep) === 1 && firstStep === secondStep) return true;
    }
    return false;
}
