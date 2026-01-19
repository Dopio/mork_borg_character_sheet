document.addEventListener('DOMContentLoaded', function() {
    const createBtn = document.getElementById('create-character');

    createBtn.addEventListener('click', async function() {
        try {
            const response = await fetch('http://localhost:8000/characters/empty', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: prompt('Введите имя персонажа:', 'Герой')
                })
            });

            if (response.ok) {
                const data = await response.json();
                // Переходим на страницу персонажа
                window.location.href = `/character.html?id=${data.id}`;
            } else {
                alert('Ошибка при создании персонажа');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Не удалось создать персонажа');
        }
    });
});
