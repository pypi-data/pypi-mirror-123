import pytest

from tj_text.typograph import ru_typus
from tj_text.typograph.chars import NBSP


class TestRuExpressions:
    """Tests for typograph.mixins.RuExpressions class."""

    @pytest.mark.parametrize(
        'word',
        [
            'без',
            'перед',
            'при',
            'через',
            'над',
            'под',
            'про',
            'для',
            'около',
            'среди',
            'из-под',
            'из-за',
            'по-над',
        ],
    )
    def test_expr_rep_positional_spaces_after_long_prepositions(self, word):
        text = (
            f'{word.capitalize()} проверяем{word} предлог {word} неразрывным '
            f'{word}пробелом {word}. {word.capitalize()} тоже.'
        )
        expected_result = (
            f'{word.capitalize()}{NBSP}проверяем{word} предлог {word}{NBSP}неразрывным '
            f'{word}пробелом {word}. {word.capitalize()}{NBSP}тоже.'
        )

        result = ru_typus(text)
        assert result == expected_result

    @pytest.mark.parametrize('word', ['же', 'ли', 'бы', 'б', 'уж'])
    def test_expr_rep_positional_spaces_before_particles(self, word):
        text = f'Проверяем{word} частицу {word} неразрывным {word}пробелом {word}.'
        expected_result = (
            f'Проверяем{word} частицу{NBSP}{word} '
            f'неразрывным {word}пробелом{NBSP}{word}.'
        )

        result = ru_typus(text)

        assert result == expected_result

    @pytest.mark.parametrize(
        'original,expected',
        [
            ('несмотря на', f'несмотря{NBSP}на'),
            ('в отличие от', f'в{NBSP}отличие{NBSP}от'),
            ('в связи с', f'в{NBSP}связи{NBSP}с'),
        ],
    )
    def test_rep_positional_spaces_for_verbose_prepositions(self, original, expected):
        original_text = (
            f'{original.capitalize()} проверяем {original} неразрывным пробелом. '
            f'{original.capitalize()} даже в начале второго предложения.'
        )
        expected_result = (
            f'{expected.capitalize()}{NBSP}проверяем {expected}{NBSP}неразрывным '
            f'пробелом. '
            f'{expected.capitalize()}{NBSP}даже в{NBSP}начале второго предложения.'
        )

        result = ru_typus(original_text)

        assert result == expected_result
