from texts.emoji import success_em, error_em

question = """
Пожалуйста, отправьте свой вопрос в одном сообщении:)
"""

answer = """
Пожалуйста, отправьте ответ в одном сообщении.
"""

message_after_question_with_avg_answer_time = """
{success_em} Спасибо за Ваш вопрос. Я обязательно отвечу в ближайшее время.
Среднее время ответа: {answer_time}.
Идентификационный номер Вашего вопроса: {question_id}.
"""

message_after_question = """
{success_em} Спасибо за Ваш вопрос. Я обязательно отвечу в ближайшее время.
Идентификационный номер Вашего вопроса: {question_id}.
"""


def get_message_after_question(data):
    """ Выбираем нужное сообщение """
    if data['avg_answer_time']:
        return message_after_question_with_avg_answer_time.format(success_em=success_em,
                                                                  answer_time=data['avg_answer_time'],
                                                                  question_id=data['question_id'])
    else:
        return message_after_question.format(success_em=success_em,
                                             question_id=data['question_id'])


question_to_admin = """
{speaker_em} Новый вопрос от пользователя {username} № {question_id}!
    <pre>{question}</pre>
"""

answer_to_user = """
Ответ на Ваш вопрос № {question_id}\n 
<code>- {question}</code>\n
    <pre>- {answer}</pre>
"""

answer_to_admin = f"""
{success_em} Ответ успешно отправлен пользователю!
"""

answer_to_admin_error = f"""
{error_em} Не удалось отправить ответ пользователю!
"""
