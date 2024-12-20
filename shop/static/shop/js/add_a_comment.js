document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = Cookies.get('csrftoken'); // Получаем CSRF-токен

    const commentForm = document.querySelector('.comment-form');
    commentForm.addEventListener('submit', function (e) {
        e.preventDefault(); // Останавливаем стандартное поведение формы

        const formData = new FormData(commentForm);
        const url = commentForm.action;

        const options = {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrftoken
            },
            mode: 'same-origin'
        };

        fetch(url, options)
            .then(response => response.json()) // Получаем JSON-ответ
            .then(data => {
                if (data.success) {
                    // Обновляем комментарии на странице
                    const commentsHeader = document.querySelector('.comments h3'); // Находим элемент <h3>
                    commentsHeader.insertAdjacentHTML('afterend', data.comment_html); // Добавляем HTML нового комментария

                    // Обновляем среднюю оценку
                    const averageRatingElement = document.querySelector('.rating');
                    if (averageRatingElement) {
                        averageRatingElement.textContent = `Average rating: ${data.average_rating}`;
                    }

                    commentForm.reset(); // Сбрасываем форму после успешной отправки
                } else {
                    alert('Не удалось добавить комментарий. Проверьте данные формы.');
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Произошла ошибка. Повторите попытку позже.');
            });
    });
});
