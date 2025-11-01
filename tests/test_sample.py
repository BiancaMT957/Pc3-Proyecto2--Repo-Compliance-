from auditor.main import saludo

def test_saludo_basico():
    assert saludo() == "Hola, mundo!"
