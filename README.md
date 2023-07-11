# Генератор упражнений по английскому языку

С помощью Streamlit разработано веб-приложение, которое автоматически преобразует предоставленный текст в упражнения по английскому языку.
Это приложение дает возможность пользователям практиковать английский язык на основе их любимых произведений.

На данный момент реализовано генерирование нескольких упражнений, а именно:

- на выбор пропущенного слова в предложении:
    - правильной формы глагола,
    - вспомогательного глагола,
    - подходящего по смыслу слова,
- на заполнение пропусков в предложении:
    - вспомогательным глаголом,
    - определителем,
    - притяжательным местоимением,
- на структуру предложения:
    - тип главного существительного в именной группе (noun phrase),
    - части речи слов в предложении,
    - порядок слов в предложении.

На основе текста "Красная Шапочка" братьев Гримм был подготовлен датасет, включающий каждое предложение, тип упражнения, описание упражнения, преобразованное предложение (само задание), варианты ответов и правильный ответ. Для каждого предложения проверялась возможность генерирования всех разработанных упражнений. Если пользователь не введет свой текст, по умолчанию будет загружен датасет на основе текста "Красная Шапочка".

Развернутое приложение в облаке Streamlit можно посмотреть, перейдя [по ссылке](https://english-language-exercise-generator-ezj3l4gexe6.streamlit.app/).

[`english_exercises_app.py`](https://github.com/apashina/english-language-exercise-generator/blob/main/english_exercises_app.py) - скрипт веб-приложения

[`english_exercises.py`](https://github.com/apashina/english-language-exercise-generator/blob/main/english_exercises.py) - набор функций, осуществляющий преобразования текста

[`english_language_exercise_generator.ipynb`](https://github.com/apashina/english-language-exercise-generator/blob/main/english_language_exercise_generator.ipynb) - тетрадка с более подробным описанием функций

[`data_js.json`](https://github.com/apashina/english-language-exercise-generator/blob/main/data_js.json) - датафрейм с упражнениями по тексту "Красная Шапочка" братьев Гримм

[`Little_Red_Cap_Jacob_and_Wilhelm_Grimm.txt`](https://github.com/apashina/english-language-exercise-generator/blob/main/Little_Red_Cap_Jacob_and_Wilhelm_Grimm.txt) - текст "Красная Шапочка" братьев Гримм
