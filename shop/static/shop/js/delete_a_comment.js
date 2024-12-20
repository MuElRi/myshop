document.addEventListener('DOMContentLoaded', function () {
    const csrftoken = Cookies.get('csrftoken');

    // Используем делегирование событий, привязываем к родительскому элементу (например, container для комментариев)
    const commentsContainer = document.querySelector('.comments'); // Родительский элемент для всех комментариев

    // Слушаем событие submit на уровне контейнера
    commentsContainer.addEventListener('submit', function (e) {
        // Проверяем, был ли отправлен именно form для удаления
        if (e.target && e.target.matches('.delete-comment-form')) {
            e.preventDefault();

            const form = e.target;
            const url = form.action; // URL для удаления комментария
            const options = {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrftoken
                },
                mode: 'same-origin'
            };

            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Удаляем элемент комментария из DOM
                        form.closest('.comment').remove();
                         // Обновляем среднюю оценку
                        const averageRatingElement = document.querySelector('.rating');
                        if (averageRatingElement) {
                            if (data.average_rating){
                                averageRatingElement.textContent = `Average rating: ${data.average_rating}`;
                            }
                            else{
                                averageRatingElement.textContent = ``
                            }
                        }
                    } else {
                        alert(data.message || 'Не удалось удалить комментарий.');
                    }
                })
                .catch(error => {
                    console.error('Ошибка:', error);
                    alert('Произошла ошибка при удалении комментария.');
                });
        }
    });
});
