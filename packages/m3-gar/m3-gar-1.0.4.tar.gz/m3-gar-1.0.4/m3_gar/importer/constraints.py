from copy import (
    deepcopy,
)

from django.db import (
    connections,
    models,
)

from m3_gar import (
    config,
)


def get_simple_field(field):
    """
    Возвращает упрощённую копию переданного поля с отключенными индексами,
    уникальными ограничениями и проверками внешних ключей
    """

    new_field = deepcopy(field)

    new_field._unique = False
    new_field.db_index = False

    if any((
        isinstance(field, models.ForeignKey),
        isinstance(field, models.ManyToManyField) and field.remote_field.through is None,
    )):
        new_field.db_constraint = False

    return new_field


def get_simple_fields(model):
    """
    Возвращает пары (поле, упрощённая копия поля) для всех собственных полей модели
    """

    fields = model._meta.get_fields(include_parents=False, include_hidden=False)

    for field in fields:
        if field.concrete:
            yield field, get_simple_field(field)


def change_constraints_for_model(model, field_from, field_to):
    """
    Производит преобразование поля field_from на field_to модели model
    в БД для записей ГАР

    Args:
        model: модель
        field_from: исходное поле
        field_to: новое поле

    Returns:
        список выполненных sql-запросов

    """
    con = connections[config.DATABASE_ALIAS]
    ed = con.schema_editor(collect_sql=True)

    ed.alter_field(model, field_from, field_to)

    return ed.collected_sql


def remove_constraints_from_model(model):
    """
    Удаляет ограничения и индексы модели
    """
    for field, simple_field in get_simple_fields(model=model):
        yield change_constraints_for_model(model=model, field_from=field, field_to=simple_field)


def restore_constraints_for_model(model):
    """
    Восстанавливает ограничения и индексы модели
    """
    for field, simple_field in get_simple_fields(model=model):
        yield change_constraints_for_model(model=model, field_from=simple_field, field_to=field)
