question = """
Пожалуйста, отправьте свой вопрос в одном сообщении:)
"""

answer = """
Пожалуйста, отправьте ответ в одном сообщении.
"""

message_after_question_with_avg_answer_time = """
Спасибо за Ваш вопрос. Я обязательно отвечу в ближайшее время.
Среднее время ответа: {answer_time}.
Идентификационный номер Вашего вопроса: {question_id}.
"""

message_after_question = """
Спасибо за Ваш вопрос. Я обязательно отвечу в ближайшее время.
Идентификационный номер Вашего вопроса: {question_id}.
"""


def get_message_after_question(data):
    """ Выбираем нужное сообщение """
    if data['avg_answer_time']:
        return message_after_question_with_avg_answer_time.format(answer_time=data['avg_answer_time'],
                                                                  question_id=data['question_id'])
    else:
        return message_after_question.format(question_id=data['question_id'])


question_to_admin = """
Новый вопрос от пользователя {username} № {question_id}!
<pre>{question}</pre>
"""
