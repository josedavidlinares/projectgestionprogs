// static/js/main.js
import { createApp } from 'vue';
import { Field, Form, ErrorMessage, configure } from 'vee-validate';
import * as yup from 'yup';  // Para validaciones con yup

// Configuración global de VeeValidate
configure({
    generateMessage: (ctx) => {
        const messages = {
            required: `El campo ${ctx.field} es obligatorio.`,
            email: `El campo ${ctx.field} debe ser un correo electrónico válido.`,
        };
        return messages[ctx.rule.name] || `El campo ${ctx.field} es inválido.`;
    },
});

// Crear la instancia de Vue
const app = createApp({
    data() {
        return {
            formData: {
                email: '',
                phone: '',
                name: '',
            },
        };
    },
});

// Registrar componentes de VeeValidate
app.component('Field', Field);
app.component('Form', Form);
app.component('ErrorMessage', ErrorMessage);

// Usar VeeValidate junto con Vue
app.mount('#app');
