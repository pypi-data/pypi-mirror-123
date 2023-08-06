from django.urls import reverse_lazy

from report_designer.core.actions import (
    ActionGroup,
    SimpleModalAction,
    DropdownActionGroup,
    UpdateDropdownModalAction,
    SimpleAction,
)


class PatternListActionGroup(ActionGroup):
    """
    Группа действий в списке шаблонов
    """

    create = SimpleModalAction(title='Добавить', url=reverse_lazy('report_designer:patterns:create'))


class PatternDropdownActionGroup(DropdownActionGroup):
    """
    Выпадающий список для претензионного дела
    """

    edit = UpdateDropdownModalAction(title='Редактировать основную информацию')


class PatternAddFieldActionGroup(ActionGroup):
    """
    Группа действий в списке шаблонов
    """

    name = 'add_fields_action_group'
    css_classes = 'tree-block-action-btn'
    add = SimpleAction(title='Перенести в шаблон', css_classes='hidden js-rd-add-fields-to-pattern')

    def __init__(self, user, obj=None, **kwargs):
        super().__init__(user, obj, **kwargs)
        self.actions['add'].url = reverse_lazy('report_designer:patterns:add-fields', kwargs={'pk': obj.pk})
