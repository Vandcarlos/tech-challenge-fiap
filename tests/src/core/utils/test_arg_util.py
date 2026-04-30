from core.utils import arg_util as sut


def test_get_arg(monkeypatch):
    monkeypatch.setattr(sut.sys, "argv", ["script.py", "--TEST_ARG", "test_value"])

    value = sut.get_arg("TEST_ARG")
    assert value == "test_value", "Deve retornar o valor correto do argumento"

    missing_value = sut.get_arg("MISSING_ARG")
    assert missing_value is None, "Deve retornar None para argumentos ausentes"
