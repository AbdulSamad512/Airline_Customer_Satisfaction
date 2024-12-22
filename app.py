from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load the pickle model
with open("lgbm_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            # Extract inputs
            departure_delay = float(request.form["Departure_Delay"])
            arrival_delay = float(request.form["Arrival_Delay"])
            online_boarding = int(request.form["Online_Boarding"])
            inflight_wifi_service = int(request.form["Inflight_wifi_service"])
            travel_class = int(request.form["Class"])
            travel_type = int(request.form["Type_of_Travel"])
            inflight_entertainment = int(request.form["Inflight_entertainment"])
            seat_comfort = int(request.form["Seat_Comfort"])
            leg_room_service = int(request.form["Leg_room_service"])
            onboard_service = int(request.form["On_board_service"])
            cleanliness = int(request.form["Cleanliness"])
            ease_of_online_booking = int(request.form["Ease_of_online_Booking"])

            # Calculate delay ratio
            flight_distance = 500  # Example constant
            delay_ratio = (departure_delay + arrival_delay) / (flight_distance + 1)

            # Prepare data
            data = [
                online_boarding,
                delay_ratio,
                inflight_wifi_service,
                travel_class,
                travel_type,
                inflight_entertainment,
                flight_distance,
                seat_comfort,
                leg_room_service,
                onboard_service,
                cleanliness,
                ease_of_online_booking,
            ]

            # Make prediction
            prediction = model.predict([data])
            output = prediction[0]

            return render_template("index.html", prediction=output)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
