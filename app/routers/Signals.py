from fastapi import APIRouter, Depends, HTTPException
import pickle
import logging
from app.services.Visualization_service import generate_signals_plot, generate_labels_plot
from app.utils.Common_utils import preprocess_signals, predict_time

router = APIRouter()

def get_signals_data(condition: str):  # Data's shape: (122, 32768, 2)
    data = None
    if condition == '35Hz12kN':
        with open('data/XJTU_bearing_dataset/35Hz12kN/Bearing1_1.pkz', 'rb') as f:
            data = pickle.load(f)
    elif condition == '37.5Hz11kN':
        with open('data/XJTU_bearing_dataset/37.5Hz11kN/Bearing2_1.pkz', 'rb') as f:
            data = pickle.load(f)
    elif condition == '40Hz10kN':
        with open('data/XJTU_bearing_dataset/40Hz10kN/Bearing3_1.pkz', 'rb') as f:
            data = pickle.load(f)
    else:
        raise HTTPException(status_code=400, detail="Invalid condition parameter")

    return data


@router.get("/signals/plot")
def get_signals_plot(condition: str, technique: str, axis: str, filter: str):  # Both parameters included
    try:
        fpt = None
        data = get_signals_data(condition)
        processed_data = preprocess_signals(data, technique, axis, filter)
        
        if technique != 'Magnitude':
            fpt = predict_time(processed_data)

        signals_plot = generate_signals_plot(processed_data, fpt)
        labels_plot = generate_labels_plot(processed_data, fpt)
        
        # Return the generated plot as a base64 image within a JSON response
        return {"signals": signals_plot, "labels": labels_plot}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        # Return a general error message to the client
        raise HTTPException(status_code=500, detail="An error occurred while generating the plot.")


