import importlib

import pytest

from gaphor.plugins.diagramexport import gaphorconvert


def test_help_output(capsys):
    with pytest.raises(SystemExit, match="0"):
        gaphorconvert.main(["--help"])

    captured = capsys.readouterr()
    assert "--help" in captured.out
    assert "--verbose" in captured.out
    assert "--use-underscores" in captured.out
    assert "--dir=directory" in captured.out
    assert "--format=format" in captured.out
    assert "--regex=regex" in captured.out


@pytest.fixture
def model():
    return importlib.resources.files("test-models") / "all-elements.gaphor"


def test_export_pdf(tmp_path, model):
    gaphorconvert.main(["-v", "-d", str(tmp_path), str(model)])

    model_path = tmp_path / "New model"

    assert model_path.exists()
    assert (model_path / "main.pdf").exists()


def test_export_png(tmp_path, model):
    gaphorconvert.main(["-v", "-f", "png", "-d", str(tmp_path), str(model)])

    model_path = tmp_path / "New model"

    assert model_path.exists()
    assert (model_path / "main.png").exists()


def test_export_svg(tmp_path, model):
    gaphorconvert.main(["-v", "-f", "svg", "-d", str(tmp_path), str(model)])

    model_path = tmp_path / "New model"

    assert model_path.exists()
    assert (model_path / "main.svg").exists()
