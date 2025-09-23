function addValidation(inputId, prefix) {
    const passwordInput = document.getElementById(inputId);
    if (!passwordInput) return;

    const timers = {}; // Track timers per requirement

    passwordInput.addEventListener("input", function () {
        const value = passwordInput.value;

        runCheck(value, /[a-z]/, prefix + "-lowercase");
        runCheck(value, /[A-Z]/, prefix + "-uppercase");
        runCheck(value, /\d/, prefix + "-digit");
        runCheck(value, /[!@#$%^&*(),.?":{}|<>]/, prefix + "-special");
        runCheck(value, /.{8,}/, prefix + "-length");
    });

    function runCheck(value, pattern, elementId) {
        const element = document.getElementById(elementId);
        const isValid = pattern.test(value);

        if (isValid) {
            element.classList.add("valid", "visible");
            element.classList.remove("invalid");

            // Reset existing timer
            clearTimeout(timers[elementId]);

            // Remove visibility after 1 second
            timers[elementId] = setTimeout(() => {
                element.classList.remove("visible");
            }, 1000);
        } else {
            // Remove timer and ensure it stays visible if invalid
            clearTimeout(timers[elementId]);
            element.classList.remove("valid", "visible");
            element.classList.add("invalid");
        }
    }
}

addValidation("signin-password", "signin");
addValidation("signup-password", "signup");
