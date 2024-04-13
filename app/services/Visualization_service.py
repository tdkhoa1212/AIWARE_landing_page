import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which is non-interactive and thread-safe
import matplotlib.pyplot as plt

def generate_signals_plot(data, fpt):
    try:
        plt.style.use('dark_background')

        if fpt is not None and fpt < len(data):
            plt.axvline(x=fpt, color='red', linestyle='--', linewidth=1)
            plt.scatter(fpt, data[fpt], color='red', s=70,  label='Initial degradation time')
        plt.plot(data, label='Signal')
        
        plt.grid(True, color='gray')  # Add grid with gray color

        plt.title('Signal Plot', color='white')
        plt.xlabel('Sample Index', color='white')
        plt.ylabel('Signal Value', color='white')
        plt.legend()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        return image_base64
    except Exception as e:
        print(e)
        return None


