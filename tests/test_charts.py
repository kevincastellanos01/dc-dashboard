import pandas as pd

from utils.charts import bar


def test_vertical_bars_follow_row_order():
    frame = pd.DataFrame({"location": ["B", "A"], "count": [1, 2]})
    figure = bar(frame, "location", "count", "Title", value_title="Count")
    assert figure.layout.xaxis.type == "category"
    assert list(figure.layout.xaxis.categoryarray) == ["B", "A"]
    assert figure.layout.yaxis.title.text == "Count"


def test_horizontal_bars_put_the_first_row_at_the_top():
    frame = pd.DataFrame({"label": ["First", "Second"], "percent": [20, 9]})
    figure = bar(frame, "label", "percent", "Title", horizontal=True, value_title="Percent")
    assert figure.layout.yaxis.type == "category"
    assert list(figure.layout.yaxis.categoryarray) == ["Second", "First"]
    assert figure.layout.xaxis.title.text == "Percent"
