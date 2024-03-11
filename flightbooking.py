from fastapi import FastAPI

app = FastAPI()

FLIGHTS = [
    {'id': 1, 'flight-number': 111, 'departure': 'EDI', 'arrival': 'LAX', 'date': '31/05/2024', 'time': '20:00', 'general-cost': 399.99},
    {'id': 2, 'flight-number': 222, 'departure': 'EDI', 'arrival': 'DXB', 'date': '11/10/2024', 'time': '17:30', 'general-cost': 199.99},
    {'id': 3, 'flight-number': 333, 'departure': 'DXB', 'arrival': 'LAX', 'date': '27/12/2024', 'time': '23:00', 'general-cost': 1999.99},
    {'id': 4, 'flight-number': 444, 'departure': 'EDI', 'arrival': 'MXP', 'date': '11/01/2025', 'time': '06:00', 'general-cost': 299.99},
    {'id': 5, 'flight-number': 555, 'departure': 'EDI', 'arrival': 'GIG', 'date': '25/02/2025', 'time': '21:45', 'general-cost': 1349.99}
]

@app.get('/')
async def first_flight():
    return {'message': 'Welcome abord!'}

@app.get('/flights')
async def get_all_flights():
    return FLIGHTS

@app.get('/flights/{flight_id}')
async def get_flight_by_id(flight_id):
    flight = f'Flight with the id {flight_id} not found'
    for f in FLIGHTS:
        if str(f['id']) == flight_id:
            flight= f
            break
    return flight