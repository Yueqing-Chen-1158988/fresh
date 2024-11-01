import pytest
from models.vegetable_premadeBox import Vegetable, PremadeBox

@pytest.fixture
def test_vegetable_init():
    vegetable = Vegetable('Carrot', 1.99, 'kg')
    assert vegetable.name == 'Carrot'
    assert vegetable.price_per_unit == 1.99
    assert vegetable.unit == 'kg'

def test_vegetable_str():
    vegetable = Vegetable('Carrot', 1.99, 'kg')
    assert str(vegetable) == 'Vegetable(Carrot, Price per kg: 1.99)'

def test_premade_box_init():
    premade_box = PremadeBox('Medium Box', 19.99)
    assert premade_box.size == 'Medium Box'
    assert premade_box.price == 19.99

def test_premade_box_str():
    premade_box = PremadeBox('Medium Box', 19.99)
    assert str(premade_box) == 'PremadeBox(Size: Medium Box, Price: 19.99)'
