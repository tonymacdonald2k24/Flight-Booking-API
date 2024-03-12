from fastapi import FastAPI, File, UploadFile
from io import StringIO
import pandas as pd

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

@app.post('/flights/{flight_id}/bulk')
def upload(flight_id, file: UploadFile = File(...)):
    try:
        passenger_list_bin = file.file.read()
        passenger_list_str = passenger_list_bin.decode("utf-8")
        passenger_list_df = pd.read_csv(StringIO(passenger_list_str))
        rows, cols = passenger_list_df.shape
        # replace missing age with zero and convert to int
        passenger_list_df.fillna({'Age': 0}, inplace=True)
        passenger_list_df['Age'] = passenger_list_df['Age'].astype(int)
        # replace missing SeatNumber with zero and convert to int
        passenger_list_df.fillna({'SeatNumber': 0}, inplace=True)
        passenger_list_df['SeatNumber'] = passenger_list_df['SeatNumber'].astype(int)
        # assing missing seats
        empty_seats = passenger_list_df['SeatNumber'] == 0
        # empty_seats_index_list = passenger_list_df.loc[empty_seats, 'SeatNumber'].tolist()
        passenger_list_df.loc[empty_seats, 'SeatNumber'] = passenger_list_df.loc[empty_seats].index + 1
        # remove invalid rows (rows without addenger name)
        passenger_list_df = passenger_list_df[passenger_list_df['Name'].notna()]
        # update title according to gender
        gender_male = passenger_list_df['Gender'] == 'Male'
        gender_female = passenger_list_df['Gender'] == 'Female'
        passenger_list_df.loc[gender_male, 'Title'] = 'Mr'
        passenger_list_df.loc[gender_female, 'Title'] = 'Ms'
        passenger_list_df
        # update gender according to tile
        title_mr = passenger_list_df['Title'] == 'Mr'
        title_ms = passenger_list_df['Title'] == 'Ms'
        gender_none = passenger_list_df['Gender'].isnull()
        passenger_list_df.loc[title_mr & gender_none, 'Gender'] = 'Male'
        passenger_list_df.loc[title_ms & gender_none, 'Gender'] = 'Female'
        passenger_list_df.to_csv(f'flight_id_{flight_id}_{file.filename}')
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    # return {"message": passenger_list_str}
    return {"message": f"Successfully uploaded {file.filename} with {rows} rows of passenger data."}

@app.get('/flights/{flight_id}/passengers')
async def get_passengers_by_flight_id(flight_id):
    try:
        flight = None
        for f in FLIGHTS:
            if str(f['id']) == flight_id:
                flight = f
                break
        general_cost = flight['general-cost']
        df = pd.read_csv(f'flight_id_{flight_id}_passengers.csv')
        passenger_count = df.shape[0]
        general_passenger_count = df[df['PassengerType'] == 'General']['SeatNumber'].count()
        discount_passenger_count = df[df['PassengerType'] == 'Discount']['SeatNumber'].count()
        airline_passenger_count = df[df['PassengerType'] == 'Airline']['SeatNumber'].count()
    except Exception:
        return {"message": "There was an error reading the file"}
    return  {
        'passenger-count': passenger_count,
        'general-passenger-count': str(general_passenger_count),
        'general-passenger-revenue': str(general_passenger_count * general_cost),
        'discount-passenger-count': str(discount_passenger_count),
        'discount-passenger-revenue': str(discount_passenger_count * general_cost * 0.85),
        'airline-passenger-count': str(airline_passenger_count),
        'airline-passenger-revenue': str(airline_passenger_count * general_cost * 0.1)
    }