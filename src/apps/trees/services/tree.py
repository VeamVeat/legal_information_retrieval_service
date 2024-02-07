import copy
import re
import string

from words2numsrus import NumberExtractor


class NormalizedDateService:
    """
    Сервис нормализации даты
    """
    @staticmethod
    def _prepare_day_of_month(day: str):
        if len(day) == 2:
            return day

        if len(day) == 1:
            return f'0{day}'

    @staticmethod
    def _prepare_month(month: str):
        data_mapping = {
            'января': '01',
            'февраля': '02',
            'марта': '03',
            'апреля': '04',
            'мая': '05',
            'июня': '06',
            'июля': '07',
            'августа': '08',
            'сентября': '09',
            'октября': '10',
            'ноября': '11',
            'декабря': '12'
        }
        months = list(data_mapping.keys())

        if month in months:
            return data_mapping.get(month)

    def get_normalized_date(self, merged_trees: dict):
        _NAME_KEY = "ДатаДокумента"

        document_data = merged_trees.get(_NAME_KEY).strip().split()

        day_month = self._prepare_day_of_month(document_data[0])
        month = self._prepare_month(document_data[1])
        year = document_data[2]

        merged_trees[_NAME_KEY] = f'{day_month}.{month}.{year}'


class NormalizedTimeFrames:
    """
    Сервис нормализации времени
    """
    @staticmethod
    def _get_structure_data(number: int, word: str) -> str:
        structure_data = ['0', '0', '0', '0']

        variations_word = {
            0: ('года', 'годы', 'лет', 'годов', 'году', 'годам', 'годом', 'годами', 'годе', 'году', 'годах'),
            1: ('месяц', 'месяцы', 'месяца', 'месяцу', 'месяцам', 'месяцем', 'месяцами', 'месяцах', 'месяце'),
            2: ('неделя', 'недель', 'недели', 'неделям', 'неделе', 'неделю', 'неделей', 'неделях'),
            3: ('дня', 'дни', 'день', 'дней', 'дню', 'дням', 'днём', 'днями', 'дне', 'днях')
        }

        for key, variation_word in variations_word.items():
            if word in variation_word:
                structure_data[key] = number
                break

        return '_'.join(structure_data)

    @staticmethod
    def delete_special_symbol(due_date: str):
        chars = re.escape(string.punctuation)
        return re.sub('[' + chars + ']', '', due_date)

    def get_normalized_time(self, merged_trees: dict):
        payment = merged_trees.get("Оплата")
        if payment is None:
            return ''

        due_date = payment.get("СрокОплаты")
        if due_date is None:
            return ''

        deleted_special_symbol = self.delete_special_symbol(due_date)

        extractor = NumberExtractor()
        prepared_due_date = extractor.replace(deleted_special_symbol).strip().split()

        structure_data = ''

        for index, value in enumerate(prepared_due_date[:-1]):
            next_value = prepared_due_date[index + 1]

            if value.isdigit():
                structure_data = self._get_structure_data(value, next_value)
            if next_value in ('полгода', 'полугода'):
                structure_data = '0_6_0_0'

        merged_trees["Оплата"]["СрокОплаты"] = structure_data


class MergedTreesService:
    """
    Сервис мёрджа деревьев
    """
    @staticmethod
    def get_merged_trees(one_tree: dict, two_tree: dict):
        for key, value in two_tree.items():
            if key in two_tree:
                one_tree[key].update(two_tree.get(key))

        return copy.deepcopy(one_tree)


class PostProcessingService:
    """
    Сервис нормализаии смёрдженного дерева
    """
    @staticmethod
    def normalize(merged_trees: dict):

        NormalizedDateService().get_normalized_date(merged_trees=merged_trees)
        NormalizedTimeFrames().get_normalized_time(merged_trees=merged_trees)

        return merged_trees


class TreeService:
    """
    Входной сервис
    """
    def __init__(self):
        self._merged_trees_service = MergedTreesService()
        self._post_processing_service = PostProcessingService()

    def process(self, one_tree: dict, two_tree: dict):
        merged_trees = self._merged_trees_service.get_merged_trees(one_tree=one_tree, two_tree=two_tree)
        return self._post_processing_service.normalize(merged_trees=merged_trees)
