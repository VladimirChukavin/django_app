(function () {
    document.addEventListener('DOMContentLoaded', function () {
        const targetElement = document.querySelector('.popup');
        const popupButtons = document.querySelectorAll('.open-popup');
        const buttonSubmit = document.querySelector('.form__submit');

        function handlePopupClose(act) {
            act.addEventListener('click', (e) => {
                if (e.target === act) {
                    act.classList.remove('popup--open');
                    act.classList.add('popup--close');
                }
            })
        }

        for (let i = 0; i < popupButtons.length; i++) {
            popupButtons[i].addEventListener('click', function (e) {
                e.preventDefault();
                targetElement.classList.remove('popup--close');
                targetElement.classList.add('popup--open');
            })
        }

        handlePopupClose(targetElement);
        handlePopupClose(buttonSubmit);
    });
})();
