# Гайд по запуску приложения

1) Клонируем репозиторий
2) Заходим в файл main.py
3) Удаляем комментарий со строчки ```create_tables(engine)``` - это создаст нашу базу данных при запуске
4) Запускаем приложение
- Вводим в терминал из директории проекта python .\main.py
- Запускаем при помощи интерфейса: в файле main.py нажимаем на зеленый треугольник возле проверки if __name__ = "__main__"
5) Закрываем приложение и комментируем строчку обратно


# Workflow приложения
1) Выполняем регистрацию
 - В базе данных происходит хэширование пароля
 - Весь функционал регистрации прописан в файле auth_crud
2) Попадаем на основной экран приложения
 - Изменять размеры экрана нельзя потому что нет динамической подгонки постов под другие разрешения
 - В одной строке может храниться 4 поста размера 250x300(размер указан в файле const.py)
 - Поиск публикаций других пользователей по хэштэгам
 - После создания поста можно зайти в карточку и там добавить пост в избранное, либо сохранить фотку себе на компьютер.
    Важно, что лучше выполнять сохранение на рабочий стол(так точно будет работать корректно)
3) Профиль пользователя:
- Пользователь может изменить свои данные(имя и пароль), также можно изменить что-то одно
- Можно загрузить свою аватарку 
- Создание поста, с картинкой, описанием и хэштэгами
- Просмотр своих опубликованных постов
- Просмотр сохраненных постов
4) Горячие клавиши приложения на основном экране:
- ctrl + p - открывает профиль пользователя
- ctrl + f - поиск постов
- ctrl + a - показывает все посты
- ctrl + q - закрывает приложение