from fastapi import APIRouter, Depends, HTTPException
import pickle
import logging
import json
import numpy as np
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
def get_signals_plot(condition: str, technique: str, axis: str, filter: str):  
    try:
        fpt = None
        data = get_signals_data(condition)
        processed_data = preprocess_signals(data, technique, axis, filter)
        
        if technique != 'Magnitude':
            fpt = predict_time(processed_data)

        signals_plot = generate_signals_plot(processed_data, fpt)
        labels_plot, predicted_labels = generate_labels_plot(processed_data, fpt)

        processed_data_json = [round(value, 2) for value in processed_data.tolist()]
        predicted_labels_json = [round(value, 2) for value in predicted_labels.tolist()]

        return {"plotted_signals": signals_plot, "plotted_labels": labels_plot, \
                "processed_signals": processed_data_json, "predicted_labels": predicted_labels_json}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while generating the plot.")



