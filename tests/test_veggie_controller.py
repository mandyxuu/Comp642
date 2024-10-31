from models.veggie import UnitPriceVeggie, WeightedVeggie, PackVeggie

def test_list_veggies(client, session):
    session.add(UnitPriceVeggie(name="Tomato", pricePerUnit=2.5, quantity=100))
    session.add(WeightedVeggie(name="Potato", weight=10, weightPerKilo=3.0))
    session.add(PackVeggie(name="Carrot Pack", numOfPack=5, pricePerPack=4.5))
    session.commit()
    
    response = client.get("/list")
    assert response.status_code == 200
    assert b"Tomato" in response.data
    assert b"Potato" in response.data
    assert b"Carrot Pack" in response.data
