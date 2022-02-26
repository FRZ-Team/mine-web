const form = document.getElementById('form_input');
const username = document.getElementById('name');
const email = document.getElementById('email');
const password = document.getElementById('password');
const password2 = document.getElementById('passwordagain');


const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success')
}

const setSuccess = (element, message)  => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('success');
    inputControl.classList.remove('error');
};

const isValidEmail = email => {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}
const isValidPassword = password => {
    const re1 = /^(([^<>()[\]\\.,;:'+=\s@"])+(\.[^<>()[\]\\.,;:\s@"]+)*)$/;
    return re1.test(String(password).toLowerCase());
}

form.addEventListener('submit', e => {

    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();

    if(usernameValue === '') {
         e.preventDefault();
        setError(username, 'Нужен имя пользователя');
    } else {
        setSuccess(username,'');
    }

    if(emailValue === '') {
         e.preventDefault();
        setError(email, 'Нужна почта');
    } else if (!isValidEmail(emailValue)) {
         e.preventDefault();
        setError(email, 'Не правильный контекст почты');
    } else {
        setSuccess(email,'');
    }


    if(passwordValue === '') {
         e.preventDefault();
        setError(password, 'Нужен пароль');
    } else if (passwordValue.length <= 8 ) {
         e.preventDefault();
        setError(password, 'Пароль должен быть больше 8 символов.')
    }else if (!isValidPassword(passwordValue)){
         e.preventDefault();
        setError(password, "Пароль не должен содержать(\" \"\ ' \ ' \ @\= \+)")
    } else {
        setSuccess(password,'');
    }

    if(password2Value === '') {
         e.preventDefault();
        setError(password2, 'Повторите пароль');
    } else if (password2Value !== passwordValue) {
         e.preventDefault();
        setError(password2, "Пароли не совпадают");
    } else {
        setSuccess(password2,'');
    }


});







