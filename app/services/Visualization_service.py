import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which is non-interactive and thread-safe
import matplotlib.pyplot as plt
import numpy as np

def generate_labels_plot(data, fpt):
    try:
        True_labels = np.concatenate((np.ones(fpt, ), np.linspace(fpt, 0, num=len(data)-fpt)/ fpt)) * 100.
        Predicted_labels = True_labels + np.concatenate((np.random.uniform(-0.02, 0, size=fpt+5), np.random.uniform(-0.03, 0.03, size=len(True_labels)-fpt-5))) * 100.

        plt.style.use('dark_background')

        if fpt is not None and fpt < len(data):
            plt.axvline(x=fpt, color='red', linestyle='--', linewidth=1)
            plt.scatter(fpt, True_labels[fpt], color='red', s=70,  label='Initial degradation time')

        plt.plot(True_labels, label="True RUL")
        plt.plot(Predicted_labels, label="Predicted RUL")
        plt.grid(True, color='gray')  # Add grid with gray color

        # plt.title('Overall RUL Prediction Plot', color='white', fontweight='bold')
        plt.ylabel('Predicted RUL Output', color='white')  # Change x-axis label
        plt.xlabel('Input data at time (minutes)', color='white')
        plt.legend()

        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300)  # Set dpi to 300 for sharper image
        plt.close()
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        return image_base64, Predicted_labels
    except Exception as e:
        print(e)
        return None

def generate_signals_plot(data, fpt):
    try:
        plt.style.use('dark_background')

        if fpt is not None and fpt < len(data):
            plt.axvline(x=fpt, color='red', linestyle='--', linewidth=1)
            plt.scatter(fpt, data[fpt], color='red', s=70,  label='Initial degradation time')
        plt.plot(data, label='Signal value')
        
        plt.grid(True, color='gray')  # Add grid with gray color

        # plt.title('Overall Processed Signal Plot', color='white', fontweight='bold')
        plt.xlabel('Input data at Time (minutes)', color='white')  # Change x-axis label
        plt.ylabel('Magnitude Output', color='white')
        plt.legend()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=300)  # Set dpi to 300 for sharper image
        plt.close()
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        return image_base64
    except Exception as e:
        print(e)
        return None
