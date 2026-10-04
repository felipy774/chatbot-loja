from backend.main import consultar_estoque

def test_produto_existente():
    resposta = consultar_estoque("Tem arroz 5kg?")
    assert "12 unidades" in resposta

def test_produto_inexistente():
    resposta = consultar_estoque("Tem açúcar?")
    assert "Não encontrei" in resposta