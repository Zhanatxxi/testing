### Testing project task

**clone project** : git clone https://github.com/Zhanatxxi/testing.git

**cd testing_Task**

1) ***docker-compose build --no-cache***
2) ***docker-compose up***

## Main app(backend)
**link**:*http://localhost:8080/docs*

### Tag User
**POST sign-up регистрация пользователя** \
**POST sign-in авторизация пользователя**

### Tag Blog
**GET blog получения всех блогов** \
**POST blog создания блога, require Bearer access_token** \
**POST blog/{blog_id} поставить лайк на блок, require Bearer access_token** \
**DELETE blog/{blog_id} убрать лайк с блока, require Bearer access_token**

### Tag Analytic
**GET analytic получения анализа об пользователе и его лайках на блоги**\
**Query parameters date_from and date_to on default today date**

## Sub app(bot)
**link**:*http://localhost:8080/bot/docs* \
**POST generate users, create blogs and set like on user**
