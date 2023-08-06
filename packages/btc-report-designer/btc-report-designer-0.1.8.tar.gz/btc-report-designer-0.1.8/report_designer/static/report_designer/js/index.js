REPORT_DESIGNER = {};


// region Элементы


class RdBaseElement {
    /**
     * Базовый класс элемента
     */

    constructor(container) {
        // Контейнер компонента
        this.container = $(container);

        // Наименование компонента
        this.name = this.container.data('name');
    }

    set_trigger(key, args) {
        /**
         * Установка триггера
         */
        key = [
            this.constructor.name.split(/(?=[A-Z])/).map(v => v.toLowerCase()).join('_'),
            key
        ].join(':');
        args = args ? args : [];
        this.container.trigger(key, new Array(...[this.container, ...args]));
    }
}


class RdAjaxContent extends RdBaseElement {
    /**
     * Базовый класс ajax-контента
     */

    constructor(container) {
        super(container)
        // URL для загрузки содержимого
        this.url = this.container.data('url');

        // Автоматическая загрузка
        this.auto_start = rd_utils.str_to_bool(this.container.data('auto-start'));

        // Прелоадер
        this.enable_preloader = rd_utils.str_to_bool(this.container.data('enable-preloader'));
        this.preloader_class = this.container.data('preloader-class');

        // Инициализация
        this.init();
    }

    init() {
        /**
         * Действия после инициализации
         */
        let element = this;
        if (this.url && this.auto_start) {
            this.loading().done(function () {
                element.post_init();
            });
        } else {
            element.post_init();
        }
    }

    post_init() {
        /**
         * Действия после инициализации
         */
    }

    loading(url, container) {
        /**
         * Загрузка контента
         */
        let dfd = new $.Deferred();
        let element = this;

        // URL для загрузки
        url = url === undefined ? this.url : url;

        // Контейнер для загрузки
        container = container === undefined ? this.container : container;

        // Триггер перед загрузкой контента
        element.set_trigger('preloading');

        // Прелоадер
        element.add_preloader(container);

        // Загрузка контента
        $.when(rd_utils.ajax_get_request(url))
            .then(function (data) {
                container.html(data['html']);
                rd_init.init_elements(container);
                return Promise.all([data]);
            }).then(function (data) {
                // Триггер после загрузки контента
                element.set_trigger('loaded', data);
                element.remove_preloader(container);
                dfd.resolve(data);
            });
        return dfd.promise();
    }

    add_preloader(container) {
        /**
         * Добавление прелоадера
         */
        this._preloader(container, 'add_preloader');
    }

    remove_preloader(container) {
        /**
         * Удаление прелоадера
         */
        this._preloader(container, 'remove_preloader');
    }

    _preloader(container, action) {
        /**
         * Прелоадер
         */
        if (this.enable_preloader) {
            container = container === undefined ? this.container : container;
            rd_utils[action](container, this.preloader_class);
        }
    }
}


class RdDynamicList extends RdAjaxContent {
    /**
     * Динамический список
     */

    post_init() {
        super.post_init();
        let dynamic_content = this;

        // Подключение фильтров
        this.bind_filter_event();

        // Загрузка контента
        this.apply_filter().done(function () {
            /**
             * Применение фильтров для загрузки данных и инициализация пагинации
             */
            dynamic_content.bind_paginate_event();
        });
    }

    // region Фильтрация

    bind_filter_event() {
        /**
         * Отслеживание фильтрации
         */
        let dynamic_content = this;

        // Функция вызова фильтрации
        const filter_function = (e) => {
            e.preventDefault();
            dynamic_content.set_trigger('filter:updated', [dynamic_content, e.target]);
            dynamic_content.apply_filter();
        };

        // Прослушивание фильтров
        let filter_container =  $(this.container).find('.js-rd-dynamic-content-filters');
        filter_container.on('change', 'input,select', filter_function);

        // Прослушивание текстовых фильтров
        filter_container.on('keyup', 'input[type="text"]', filter_function);

        // Прослушивание отчистки фильтров
        $(filter_container).on('click', '.js-rd-filters_clear', function (e) {
            /**
             * Кнопка отчистки фильтров
             */
            e.preventDefault();
            dynamic_content.apply_filter_clear();
        });
    }

    apply_filter_clear() {
        /**
         * Действие отчистки фильтра
         */
        let filter_container =  $(this.container).find('.js-rd-dynamic-content-filters');
        let form = filter_container.find('form');

        // Отключение прослушивания фильтров
        filter_container.off('change keyup click')

        // Сброс значений
        form[0].reset();

        // Инициализация формы и прослушивание изменений
        rd_init.init_elements(form);
        this.bind_filter_event();

        // Перезагрузка
        this.apply_filter();
    }

    apply_filter(query) {
        /**
         * Применение фильтров
         */
        // Контейнер с даннными
        let ajax_content = rd_utils.get_from_rd_store('ajax_contents', this.name);

        // URL с параметрами поиска
        let url = `${ajax_content.url}?${query ? query : this.get_content_url_query()}`;

        // Загрузка ajax-content
        return ajax_content.loading(url);
    }

    // endregion Фильтрация

    // region Пагинация

    bind_paginate_event() {
        /**
         * Отслеживание пагинации
         */
        let dynamic_content = this;

        // Функция вызова фильтрации
        const paginate_function = (e) => {
            e.preventDefault();
            dynamic_content.set_trigger('paginate:updated', [dynamic_content, e.target]);
            dynamic_content.apply_paginate(e.currentTarget);
        };

        // Прослушивание фильтров
        $(this.container).on(
            'click',
            '.js-rd-dynamic-content-pagination a.js-pagination-page',
            paginate_function
        );

        // Прослушивание фильтров
        $(this.container).on(
            'change',
            '.js-rd-dynamic-content-pagination select.js-pagination-count',
            paginate_function
        );
    }

    apply_paginate(target) {
        /**
         * Применение пагинации
         */
        // Контейнер с даннными
        let ajax_content = rd_utils.get_from_rd_store('ajax_contents', this.name);

        // URL с параметрами поиска
        let value = $(target).val() || $(target).data('value');
        let url = `${ajax_content.url}?${this.get_content_url_query()}&${$(target).data('key')}=${value}`;

        // Создание прелоадера
        ajax_content.loading(url);
    }

    // endregion Пагинация

    get_content_url_query() {
        /**
         * Получение параметров URL для фильтрации
         */
        // Виджеты для сериализации значений
        let widgets = ['input', 'select'];

        // Строка поиска
        return $(this.container).find(`.js-rd-dynamic-content-filters ${widgets.join()}`).serialize();
    }
}


// endregion Элементы


// region Функции


const rd_utils =  {
    /**
     * Вспомогательные функции
     */

    // region Вспомогательные функции

    str_to_bool: function(str) {
        /**
        Перевод из строки в булево значение
         */
        if (typeof str === 'boolean') { return str }
        if (typeof str !== 'string') { return false }
        return String(str).toLowerCase().trim() === 'true';
    },

    create_or_get_rd_store: function (key) {
        /**
         * Создание или получение объекта по ключу в хранилище конструктора
         */
        if (!REPORT_DESIGNER.hasOwnProperty(key)) {
            REPORT_DESIGNER[key] = [];
        }
        return REPORT_DESIGNER[key];
    },

    add_to_rd_store: function (key, obj) {
        /**
         * Добавление элемента в хранилище конструктора
         */
        rd_utils.create_or_get_rd_store(key).push(obj);
    },

    add_unique_to_rd_store: function (key, value) {
        /**
         * Добавление уникального значения в хранилище конструктора
         */
        let array = rd_utils.create_or_get_rd_store(key);
        if(array.indexOf(value) === -1) {
            array.push(value);
        }
    },

    remove_from_rd_store: function (key, obj) {
        /**
         * Удаление элемента из хранилища конструктора
         */
        let array = rd_utils.create_or_get_rd_store(key);
        let index = array.indexOf(obj);
        if (index > -1) {
            array.splice(index, 1);
        }
    },

    get_from_rd_store(key, name) {
        /**
         * Поиск по наименованию в хранилище конструктора
         */
        return rd_utils.create_or_get_rd_store(key).find(obj => obj.name === name);
    },

    remove_element(container, selector, only_child=false) {
        /**
         * Удаление элемента из контейнера по селектору
         */
        $(container)[only_child ? 'children' : 'find'](`.${selector}`).remove();
    },

    // endregion Вспомогательные функции

    // region Ajax запросы

    ajax_request: function(url, type, data) {
        /**
         * Ajax запрос
         */
        let ajax_data = {
            url: url,
            type: type,
            dataType: 'json',
            async: 'true',
        };

        let csrftoken = $('[name=csrfmiddlewaretoken]').val();
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(type.toUpperCase()) && !this.crossDomain) {
            data = data === undefined ? {} : data;
            if (!data.hasOwnProperty('csrfmiddlewaretoken')) {
                data['csrfmiddlewaretoken'] = csrftoken;
            }
            ajax_data['data'] = data;
            ajax_data['beforeSend'] = function(xhr, settings) { xhr.setRequestHeader("X-CSRFToken", csrftoken); }
        }
        return $.ajax(ajax_data);
    },

    ajax_get_request: function (url) {
        /**
         * Ajax GET запрос
         */
        return rd_utils.ajax_request(url, 'GET');
    },

    ajax_post_request: function (url, data) {
        /**
         * Ajax POST запрос
         */
        return rd_utils.ajax_request(url, 'POST', data);
    },

    processing_ajax_data_response: function(data) {
        /**
         * Обработка ответа после успешного ajax-post запроса
         */
        if (data['redirect_url']) {
            /*
            Перенаправление на указанный URL
             */
            window.location.replace(data['redirect_url']);
        } else if (data['dependents']) {
            /*
            Действия с зависимыми объектами
             */
            data['dependents'].forEach(function (item) {
                let dependent_key = item['dependent_key'];
                let dependent_name = item['dependent_name'];

                let element = rd_utils.get_from_rd_store(dependent_key, dependent_name);
                switch (dependent_key) {
                    case 'dynamic_contents':
                        // Чистка фильтров вызовет перезагрузку списка
                        element.apply_filter_clear();
                        break;
                    case 'ajax_contents':
                        element.loading();
                        break;
                }
            });
        }
    },

    // endregion Ajax запросы

    // region Модальные окна

    open_modal: function(html, container, modal_lg) {
        /**
         * Открытие модальной формы
         */
        // Получение контейнера модального окна
        container = container === undefined ? $('#report-designer-modal') : container;
        container.toggleClass('modal-lg', typeof modal_lg === 'boolean' ? modal_lg : false);
        container.find('.modal-content').html(html);
        rd_init.init_elements(container);
        container.modal('show');
    },

    ajax_open_modal_form(url, container, modal_lg) {
        /**
         * Заггрузка и открытие модальной формы
         */
        var dfd = new $.Deferred();
        $.when(rd_utils.ajax_get_request(url))
            .then(function(data) {
                rd_utils.open_modal(data['html'], container, modal_lg);
                dfd.resolve(data);
            });
        return dfd.promise();
    },

    // endregion Модальные окна

    // region Прелоадер

    add_underlay: function (container, added_element_class, with_top_offset) {
        /**
         * Создание подложки, закрываюищей контент контейнера со скроллом
         */
        let element = $('<div>', {'class': added_element_class, 'styles': 'visibility: hidden;'});
        $(container).css('position', 'relative');
        if (with_top_offset) {
            element.css('top', $(container).scrollTop());
        }
        element.appendTo($(container));
        if (element.css('position') === 'absolute') {
            $(container).css('min-height', `${element.height()}px`);
        }
        element.css('visibility', '');
    },

    remove_underlay: function (container, removed_element_class) {
        /**
         * Удаление подложки, закрываюищей контент контейнера со скроллом
         */
        rd_utils.remove_element(container, removed_element_class, true);
        $(container).css('position', '');
    },

    add_preloader: function (container, preloader_class) {
        /**
         * Добавление прелоадера
         */
        if (preloader_class !== undefined && !$(container).children(`.${preloader_class}`).length) {
            rd_utils.add_underlay(container, preloader_class);
        }
    },

    remove_preloader: function (container, preloader_class) {
        /**
         * Удаление прелоадера
         */
        if (preloader_class !== undefined) {
            rd_utils.remove_underlay(container, preloader_class);
        }
    },

    // endregion Прелоадер
}


const rd_init = {
    /**
     * Инициализация компонентов
     */

    init_elements: function(container) {
        /**
         * Инициализация элементов
         */
        rd_init.init_ajax_contents(container);
        rd_init.init_dynamic_list(container);
        rd_init.init_select2(container);
        rd_init.init_draggable(container);
        rd_init.init_droppable(container);
        rd_init.init_table_sortable(container);
    },

    init_draggable: function (container) {
        /**
         * Инициализация draggable
         */
        let options = {
            // Возврат элемента (invalid для возврата при перетаскивании не в облесть для перетаскивания)
            revert: 'invalid',
            // Создание клона элемента, вместо использования позиционирования основного элемента
            helper: 'clone',
            // Добавление клона элемента к тегу body
            appendTo: 'body',
            // Z-index при создании элементов
            zIndex: 3,
            // Добавление дефолтных классов
            addClasses: false,
            // Отключение скролла (при включенном скролле идет бесконечный скролл по всем направлениям)
            scroll: false,
        }
        container.find('.js-rd-draggable').draggable(options);
    },

    init_droppable: function (container) {
        /**
         * Инициализация draggable и droppable
         */
        let options = {
            activeClass: 'rd-droppable-active-container',
            greedy: true,
        }
        container.find('.js-rd-droppable').droppable(
            options,
            {
                 accept: function (element) {
                     // Только для перетаскиваемых объектов
                     if (!element.hasClass('js-rd-draggable')) {
                         return false;
                     }
                     // Отключение действий принимаемоей области для дочерних объектов
                     return !($(this).find(element).length);
                 },
                 activate: function(e, ui) {
                     // Добавление элемента для создания визуальной области для перетаскивания
                     rd_utils.add_underlay(e.target, 'rd-droppable-active', true);
                 },
                 deactivate: function(e, ui) {
                     // Удаление визуальной области для перетаскивания
                     rd_utils.remove_underlay(e.target, 'rd-droppable-active');
                 },
                 over: function (e, ui) {
                     // Добавление класса к визуальной области для перетаскивания
                     $(e.target).children('.rd-droppable-active').addClass('rd-hover');
                 },
                 out: function (e, ui) {
                     // Удаление класса у визуальной области для перетаскивания
                     $(e.target).children('.rd-droppable-active').removeClass('rd-hover');
                 }
            }
        );
    },

    init_table_sortable: function (container) {
        /**
         * Инициализация sortable
         */
        let options = {
            appendTo: document.body,
            axis: "y",
            containment: "parent",
            forceHelperSize: true,
            revert: 100,
            handle: '.js-rd-table-sortable',
            forcePlaceholderSize: true,
            tolerance: 'pointer',
        }
        container.find('.js-rd-table-sortable').sortable(
            options,
            {
                activate: function (event, ui) {
                    $(ui.helper).addClass('rd-sortable-tr');
                },
                deactivate: function (event, ui) {
                    $(ui.item).removeClass('rd-sortable-tr');
                },
                helper: function(e, tr) {
                    let tds = $(tr).children();
                    $(tr).children().each(function (index) {
                      $(this).width(tds.eq(index).width());
                    });
                    return tr;
                },
            }
        );
    },

    init_ajax_contents: function (container) {
        /**
         * Инициализация RdAjaxContent
         */
        $(container).find('.js-rd-ajax-content').each(function (key, value) {
            let ajax_content = new RdAjaxContent($(value));
            rd_utils.add_to_rd_store('ajax_contents', ajax_content)
        });
    },

    init_dynamic_list: function (container) {
        /**
         * Инициализация RdDynamicList
         */
        $(container).find('.js-rd-dynamic-content').each(function (key, value) {
            let dynamic_content = new RdDynamicList($(value));
            rd_utils.add_to_rd_store('dynamic_contents', dynamic_content)
        });
    },

    init_select2: function(container) {
        /**
         * Инициализация Select2
         */
        let base_options = {
            language: 'ru',
            minimumResultsForSearch: -1,
            width: '100%',
        }

        $(container).find('select').each(function (key, value) {
            let element = $(value);

            // Модальное окно
            let modal_parent = element.closest('#report-designer-modal');
            element.djangoSelect2({
                ...base_options,
                ...(element.hasClass('js-rd-select-search') && {minimumResultsForSearch: 1}),
                ...($(modal_parent).length && {dropdownParent: $(modal_parent).find('.modal-content')}),
            });
        });
    }
}


function report_designer() {
    /**
     * Конструктор отчетов
     */

    // region Перетаскивание объектов

    $(document).on('dragstart', '.js-rd-draggable', function (e, ui) {
        /**
         * Действия, при перетаскивании элемента
         */
        // Установка класса, для перетаскиваемого объекта
        $(ui.helper).addClass('tree-branch-drag');
    });

    // endregion Перетаскивание объектов

    // region Сортировка строк в таблицах

    $(document).on('sortupdate', '.js-rd-table-sortable', function (e, ui) {
        /**
         * Действия, после изменения порядка строк в таблице
         */
        let url = $(ui.item).data('change-order-url');
        if (url) {
            // Получение нового значения
            let trs = $(e.target).find('tr[data-order]');
            let order = trs.filter(`[data-order="${$(ui.item).data('order')}"]`).index();
            let data_post = {'pk': $(ui.item).data('pk'), 'order': order};

            // Отправка запроса с новым значением на указанный URL из строки
            $.when(rd_utils.ajax_post_request(url, data_post)).then(function (data) {
                // Обработка успешного ответа
                rd_utils.processing_ajax_data_response(data);
            });
        }
    });

    // endregion Сортировка строк в таблицах

    // region Модальные формы

    $(document).on('click', '.js-rd-ajax-load-modal-btn', function (e) {
        /**
         * Загрузка модального окна по кнопке
         */
        e.preventDefault();
        rd_utils.ajax_open_modal_form(
            $(this).attr('href'),
            undefined,
            rd_utils.str_to_bool($(this).data('modal-lg'))
        )
    });

    $(document).on('submit', '.js-rd-ajax-form', function (e) {
        /**
         * Отправка ajax формы
         */
        e.preventDefault();

        let form = $(this);
        let container = form.parent();

        // Параметры формы и отправка
        $.when(rd_utils.ajax_post_request(form.attr('action'), form.serializeArray()))
            .then(function (data) {
                let success = data['success'];
                let html = data['html'];

                if (!success) {
                    container.html(html);
                    rd_init.init_elements(container);
                } else {
                    let modal = container.closest('#report-designer-modal');
                    if (modal) {
                        modal.modal('hide');
                    }
                    form.trigger('rd_modal_form:success', data);
                }
            });
    });

    $(document).on('rd_modal_form:success', '.js-rd-ajax-form-create', function (e, data) {
        /**
         * Действия после успешного сохранения ajax-формы
         */
        rd_utils.processing_ajax_data_response(data);
    });

    // endregion Модальные формы

    // region Дерево таблиц в шаблоне

    $(document).on('click', '.js-subtree-btn', function (e) {
        /**
         * Загрузка веток дерева по клику на кнопку раскрытия ветки
         */
        let btn = $(this);
        let tree_branch = btn.closest('.js-tree-branch');
        let tree_content = tree_branch.children('.js-tree-content');
        let tree = tree_content.closest('.js-rd-pattern-tables');

        // Уже загружено
        let is_exists = tree_content.length;
        let is_hidden = is_exists && tree_content.is(':hidden');

        if (!is_exists) {
            // Если список еще не загружен - загрузка списка
            $.when(rd_utils.ajax_get_request(btn.data('url'))).then(function (data) {
                // Установка списка в соответствующий пункт
                tree_branch.append(data['html']);
                rd_init.init_elements(tree_branch);

                // Выставление уже отмеченных чекбоксов
                let selector = rd_utils.create_or_get_rd_store('selected_fields_to_pattern').map(
                    pk => `.js-rd-field-to-pattern[data-pk="${pk}"]`
                ).join(',');
                $(tree_branch).find(selector).prop('checked', true);
            });
        } else {
            // Если список уже загружен, в зависимости от флага, скрытие или показ списка
            is_hidden ? tree_content.show() : tree_content.hide();
        }
        btn.toggleClass('open', !is_exists || is_hidden);
    });

    // endregion Дерево таблиц в шаблоне


    // region Добавление таблицы в шаблон

    $(document).on('drop', '.js-rd-pattern-tables', function (e, ui) {
        /**
         * Добавление / удаление таблицы в шаблоне
         */
        // Перетаскиваемый объект
        let element = $(ui.draggable);
        let url = element.closest('.js-tree-content[data-action-url]').data('action-url');
        let data_post = {'table': element.data('pk')};

        // Добавление прелоадера до отправки запроса (при успешном ответе прелоадер удалится при загрузке данных)
        let ajax_content = rd_utils.get_from_rd_store('ajax_contents', 'pattern_tables');
        ajax_content.add_preloader();

        // Отправка запроса на добавление/удаление таблицы в шаблоне
        $.when(rd_utils.ajax_post_request(url, data_post)).then(function (data) {
            switch (data['success']) {
                case true:
                    // Обработка успешного ответа
                    rd_utils.processing_ajax_data_response(data);
                    break;
                case false:
                    // Показ модального окна при ошибке
                    rd_utils.open_modal(data['html']);
                    ajax_content.remove_preloader();
            }
        });
    });

    // endregion Добавление таблицы в шаблон

    // region Добавление полей в шаблон

    $(document).on('change', '.js-rd-field-to-pattern', function (e, ui) {
        /**
         * Действия, после выбора поля для переноса в дереве полей в шаблоне
         */
        let checkbox = $(this);
        let is_checked = checkbox.is(':checked');
        let pk = checkbox.attr('data-pk');
        let selected_fields_store = 'selected_fields_to_pattern';
        let tree = checkbox.closest('.js-rd-pattern-tables');

        // Добавление / удаление выбранного чекбокса в хранилище
        is_checked ?
            rd_utils.add_to_rd_store(selected_fields_store, pk) :
            rd_utils.remove_from_rd_store(selected_fields_store, pk);

        // Поиск всех чекбоксов в дереве с таким же наименованием
        tree.find(`.js-rd-field-to-pattern[data-pk="${pk}"]:not(:disabled)`)
            .prop('checked', is_checked);

        // Скрытие показ кнопки добавления полей в шаблон
        // Если ни одно поле не выбрано, кнопка не показывается
        tree.parent()
            .find('.js-rd-add-fields-to-pattern')
            .toggleClass('hidden', !tree.find('.js-rd-field-to-pattern:checked:not(:disabled)').length);
    });

    $(document).on('click', '.js-rd-add-fields-to-pattern', function (e) {
        /**
         * Добавление выбранных полей в шаблон
         */
        e.preventDefault();

        // Выбранные поля
        let selected_fields = rd_utils.create_or_get_rd_store('selected_fields_to_pattern');
        if (selected_fields) {
            // Прелоадер для таблиц
            let pattern_tables = rd_utils.get_from_rd_store('ajax_contents', 'pattern_tables');
            pattern_tables.add_preloader();

            // URL запроса
            let url = $(this).attr('href');

            // Подготовка данных и отправка запроса
            let data = {'selected_fields[]': selected_fields.map(Number)};
            $.when(rd_utils.ajax_post_request(url, data)).then(function (data) {
                // Обработка успешного ответа
                rd_utils.processing_ajax_data_response(data);
            });
        }
    });

    // endregion Добавление полей в шаблон
}

// endregion Функции

$(document).ready(function () {
    if(document.getElementById('report-designer')){
        rd_init.init_elements($('#report-designer'));
        report_designer();
    }
});




