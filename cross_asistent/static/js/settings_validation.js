$(document).ready(function () {
    var typingTimer;

    function setupDelayedValidation(selector) {
        $(selector)
            .find("input")
            .each(function () {
                $(this)
                    .on("input", function () {
                        clearTimeout(typingTimer);
                        var element = this;
                        typingTimer = setTimeout(function () {
                            $(element).valid();
                        }, 5000);
                    })
                    .on("keydown", function () {
                        clearTimeout(typingTimer);
                    });
            });
    }

    function createValidation(selector, rules, messages) {
        try {
            $(selector).validate({
                rules: rules,
                messages: messages,
                errorPlacement: function (error, element) {
                    error.addClass("bg-danger text-white p-2 rounded fs-8");
                    error.insertAfter(element.parent());
                },
                highlight: function (element) {
                    $(element).addClass("is-invalid").removeClass("is-valid");
                },
                unhighlight: function (element) {
                    $(element).addClass("is-valid").removeClass("is-invalid");
                    $("#lockIcon").removeClass("fa-lock-open").addClass("fa-lock");
                },
                invalidHandler: function (event, validator) {
                    var errors = validator.numberOfInvalids();
                    if (errors) {
                        var message =
                            errors == 1
                                ? "Llena correctamente el campo resaltado 🧐🤔😬"
                                : "Llena correctamente los " + errors + " campos resaltados 🧐🤔😬";
                        alertSToast("center", 10000, "error", message);
                    }
                },
                submitHandler: function (form) {
                    jsonSubmit({
                        target: form,
                        preventDefault: function () {},
                    });
                },
            });
            setupDelayedValidation(`${selector} input`);
        } catch (error) {
            console.error("Error Inesperado: ", error);
            alertSToast("center", 8000, "error", `😥 Ah ocurrido un error #304.`);
        }
    }

    // Reglas y mensajes comunes
    var commonRules = {
        first_name: { required: true, minlength: 3, validname: true },
        last_name: { required: true, minlength: 5, validname: true },
        username: { required: true, minlength: 5, validusername: true },
        email: { required: true, validemail: true, email: true },
    };

    var commonMessages = {
        first_name: {
            required: "Ingresa tu nombre.",
            validname: "Escribe palabras sin caracteres especiales (!@#$%^&:)",
            minlength: "Tu nombre debe tener al menos 3 letras.",
        },
        last_name: {
            required: "Ingresa tus apellidos.",
            validname: "Escribe palabras sin caracteres especiales (!@#$%^&:)",
            minlength: "Escribe al menos 5 letras.",
        },
        username: {
            required: "Ingresa un nombre de usuario.",
            validusername:
                "El nombre de usuario debe contener solo letras, numeros y guiones. El nombre de usuario no puede comenzar por numeros o guiones.",
            minlength: "Escribe al menos 5 letras.",
        },
        email: {
            required: "Ingresa tu correo electrónico.",
            validemail: "Ingresa un correo electrónico válido",
            email: "Ingresa un correo electrónico válido",
        },
    };

    // Validación para el formulario de registro
    createValidation(
        "[data-validate-singup]",
        {
            ...commonRules,
            password1: { required: true, minlength: 8, validpassword: true },
            password2: { required: true, validpassword: true, equalTo: "#password1" },
        },
        {
            ...commonMessages,
            password1: {
                required: "Ingresa una contraseña.",
                validpassword:
                    "La contraseña debe tener al menos: <ul class='m-0'><li>8 caracteres</li><li>1 letra mayúscula</li><li>1 letra minúscula</li><li>1 número <li>1 carácter especial (!@#$%)</li><li>No puede contener guiones</li></ul>",
                minlength: "Tu contraseña debe tener al menos 8 caracteres.",
            },
            password2: {
                required: "Confirma tu contraseña.",
                validpassword: "Completa la contraseña",
                equalTo: "Las contraseñas aún no son iguales. 🧐😬",
            },
        }
    );

    // Validación para el formulario de crear usuario
    createValidation(
        "[data-validate-createuser]",
        {
            ...commonRules,
            password: { required: true, minlength: 8, validpassword: true },
        },
        {
            ...commonMessages,
            password: {
                required: "Ingresa una contraseña.",
                validpassword:
                    "La contraseña debe tener al menos: <ul class='m-0'><li>8 caracteres</li><li>1 letra mayúscula</li><li>1 letra minúscula</li><li>1 número <li>1 carácter especial (!@#$%)</li><li>No puede contener guiones</li></ul>",
                minlength: "Tu contraseña debe tener al menos 8 caracteres.",
            },
        }
    );

    // Validación para el formulario de perfil
    createValidation(
        "[data-validate-profile]",
        {
            usernameChanged: { minlength: 5, validusername: true },
            first_nameChanged: { minlength: 3, validname: true },
            last_nameChanged: { minlength: 5, validname: true },
            emailChanged: { validemail: true, email: true },
            firmaBlog: { minlength: 8 },
            passwordSend: { required: true, minlength: 8, validpassword: true },
            newPass: { minlength: 8, validpassword: true },
            confNewPass: { minlength: 8, equalTo: "#newPass" },
        },
        {
            usernameChanged: {
                validusername:
                    "El nombre de usuario debe contener solo letras, números y guiones. El nombre de usuario no puede comenzar por números o guiones. No utilices espacios u otros caracteres especiales.",
                minlength: "Escribe al menos 5 letras.",
            },
            first_nameChanged: {
                validname: "Escribe tu nombre sin caracteres especiales (!@#$%^&:)",
                minlength: "Tu nombre debe tener al menos 3 letras.",
            },
            last_nameChanged: {
                validname: "Escribe tu apellido sin caracteres especiales (!@#$%^&:)",
                minlength: "Escribe al menos 5 letras.",
            },
            emailChanged: {
                validemail: "Ingresa un correo electrónico válido",
                email: "Ingresa un correo electrónico válido",
            },
            firmaBlog: {
                minlength:
                    "Este campo es Opcional. <br>Debe tener al menos 8 Caracteres. Se pueden incluir caracteres especiales.",
            },
            passwordSend: {
                required: "Confirma tu contraseña actual.",
                minlength: "Tu contraseña debe tener al menos 8 caracteres.",
                validpassword: 'Completa la contraseña ("Mayusculas", "m", 0-9, !@#$)',
            },
            newPass: {
                minlength: "Tu nueva contraseña debe tener al menos 8 caracteres.",
                validpassword:
                    "La nueva contraseña debe tener al menos: <ul class='m-0'><li>8 caracteres</li><li>1 letra mayúscula</li><li>1 letra minúscula</li><li>1 número <li>1 carácter especial (!@#$%)</li></ul>",
            },
            confNewPass: {
                minlength: "Tu nueva contraseña debe tener al menos 8 caracteres.",
                equalTo: "Escribe de nuevo tu nueva contraseña. 🧐😬",
            },
        }
    );
});
