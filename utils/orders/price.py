def rounding (number, digits=0):
    return float(f"{number:.{digits}f}")


def get_price_with_discount(price, discount):
    """ Получаем стоимость с учетом скидки """
    disc_price = 100 - discount
    convers_price = (price * disc_price) / 100
    return rounding(convers_price, 1)
