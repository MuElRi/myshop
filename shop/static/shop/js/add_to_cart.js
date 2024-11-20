document.addEventListener('DOMContentLoaded', (event) => {
    const csrftoken = Cookies.get('csrftoken');

    // Получаем все кнопки "add-to-cart"
    const addToCartButtons = document.querySelectorAll('a.add-to-cart');

    addToCartButtons.forEach(addButton => {
        addButton.addEventListener('click', function(e) {
            e.preventDefault();

            const url = addButton.dataset.url;
            var options = {
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            };

            // Добавляем данные в тело запроса
            var formData = new FormData();
            formData.append('id', addButton.dataset.id);
            formData.append('action', addButton.dataset.action);
            options['body'] = formData;

            // Отправляем HTTP-запрос
            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data['status'] === 'ok') {
                        var previousAction = addButton.dataset.action;

                        // Переключаем текст кнопки и data-action
                        var action = previousAction === 'add' ? 'remove' : 'add';
                        addButton.dataset.action = action;
                        addButton.innerHTML = action === 'add' ? 'Add to cart' : 'In cart';
                    }
                });
        });
    });

//    const updateCartContainers = document.querySelectorAll('.update-cart')
//    updateCartContainers.forEach(container=> {
//        const form = container.querySelector('form')
//        form.addEventListener('submit', function(e) {
//            e.preventDefault();  // Останавливаем стандартное поведение формы
//            const url = form.action
//            console.log(url)
//            var formData = new FormData(form);
//            formData.append('id', form.dataset.id);
//            formData.append('action', form.dataset.action);
//            fetch(url, {
//                method: 'POST',
//                body: formData,
//                headers:{ 'X-CSRFToken': csrftoken },
//                mode: 'same-origin'
//            })
//                .then(response => response.text())
//                .then(html => {
//                    console.log(3)
//                    container.innerHTML = html
//                })
//                .catch(error => console.error('Ошибка:', error));
//        });
//    });
    const updateCartContainers = document.querySelectorAll('.update-cart')
    updateCartContainers.forEach(container=> {
        container.addEventListener('submit', function(e) {

            e.preventDefault();  // Останавливаем стандартное поведение формы
            const form = container.querySelector('form')
            const url = form.action
            console.log(url)
            var formData = new FormData(form)

            options = {
                method: 'POST',
                body: formData,
                headers:{ 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            }

            fetch(url, options)
                .then(response => response.text())
                .then(html => {
                    console.log(3)
                    container.innerHTML = html
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});

