
// Validar Formulario https://jqueryvalidation.org/ #########################################
$(document).ready(function () {
    var typingTimer;
    var doneTypingInterval = 2000;

    function setupDelayedValidation() {
        $(this)
            .on("keyup", function () {
                clearTimeout(typingTimer);
                var element = this;
                typingTimer = setTimeout(function () {
                    $(element).valid();
                }, doneTypingInterval);
            })
            .on("keydown", function () {
                clearTimeout(typingTimer);
            });
    }
    $.validator.addMethod("validname", function (value, element) {
        return this.optional(element) || expressions.name.test(value);
    });

    $.validator.addMethod("validemail", function (value, element) {
        return this.optional(element) || expressions.email.test(value);
    });

    $.validator.addMethod("validusername", function (value, element) {
        return this.optional(element) || expressions.username.test(value);
    });

    $.validator.addMethod("validpassword", function (value, element) {
        $("#lockIcon").removeClass("fa-lock").addClass("fa-lock-open");
        return this.optional(element) || expressions.password.test(value);
    });

    // Validacion del formulario de registro ##################################################
    try {
        $("[data-validate-singup]").validate({
            rules: {
                last_name: { required: true, minlength: 5, validname: true },
                username: { required: true, minlength: 5, validusername: true },
                email: { required: true, validemail: true, email: true },
                password1: { required: true, minlength: 8, validpassword: true },
                password2: { required: true, validpassword: true, equalTo: "#password1" },
            },
            messages: {
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
                    validusername: "El nombre de usuario debe contener solo letras, numeros y guiones. El nombre de usuario no puede comenzar por numeros o guiones.",
                    minlength: "Escribe al menos 5 letras.",
                },
                email: {
                    required: "Ingresa tu correo electrónico.",
                    validemail: "Ingresa un correo electrónico válido",
                    email: "Ingresa un correo electrónico válido",
                },
                password1: {
                    required: "Ingresa una contraseña.",
                    validpassword:
                        "La contraseña debe tener al menos: <ul class='m-0'><li>8 caracteres</li><li>1 letra mayúscula</li><li>1 letra minúscula</li><li>1 número <li>1 carácter especial (!@#$%)</li></ul>",
                    minlength: "Tu contraseña debe tener al menos 8 caracteres.",
                },
                password2: {
                    required: "Confirma tu contraseña.",
                    validpassword: "Completa la contraseña",
                    equalTo: "Las contraseñas aun no son iguales. 🧐😬",
                },
            },
            // onkeyup: function (element) {
            //     $(element).valid();
            // },
            errorPlacement: function (error, element) {
                // var $div = $("<div>").addClass("text-white bg-danger p-2 rounded").append(error.text());
                // $div.insertAfter(element.parent());
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
                    alertSToast('center', 10000, 'error', message);
                }
            },
            submitHandler: function (form) {
                jsonSubmit({
                    target: form,
                    preventDefault: function () {},
                });
            },
        });
        $("[data-validate-singup] input").each(setupDelayedValidation);
    } catch (error) {
        console.error("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ah ocurrido un error #304.`);
    }


    // Validacion del formulario de perfil ##################################################
    try {
        $("[data-validate-profile]").validate({
            rules: {
                usernameChanged: { minlength: 5, validusername: true },
                first_nameChanged: { minlength: 3, validname: true },
                last_nameChanged: { minlength: 5, validname: true },
                emailChanged: { validemail: true, email: true },
                firmaBlog: { minlength: 8 },
                passwordSend: { required: true, minlength: 8, validpassword: true },
                newPass: { minlength: 8, validpassword: true },
                confNewPass: { minlength: 8, equalTo: "#newPass" },
            },
            messages: {
                usernameChanged: {
                    validusername: "El nombre de usuario debe contener solo letras, numeros y guiones. El nombre de usuario no puede comenzar por numeros o guiones. No utilices espacios u otros caracteres especiales",
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
                    minlength: "Este campo es Opcional. <br>Debe tener al menos 8 Caracteres. Se pueden incluir caracteres especiales.",
                },
                passwordSend: {
                    required: "Confirma tu contraseña Actual.",
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
                    equalTo: "Escribe de nuevo tu Nueva contraseña. 🧐😬",
                },
            },
            errorPlacement: function (error, element) {
                error.addClass("bg-danger text-white p-2 rounded fs-8 text-start");
                error.insertAfter(element.parent());
            },
            highlight: function (element) {
                $(element).addClass("is-invalid");
            },
            unhighlight: function (element) {
                $(element).removeClass("is-invalid");
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
    } catch (error) {
        console.error("Error Inesperado: ", error);
        alertSToast("center", 8000, "error", `😥 Ah ocurrido un error #304.`);
    }
});