import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, which is non-interactive and thread-safe

from IPython.display import HTML
import matplotlib.pyplot as plt

import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def generate_labels_plot(data, fpt):
    # 122, 490, 2537
    try:
        if len(data) == 122:
            distance = 12
        elif len(data) == 490:
            distance = 30
        elif len(data) == 2537:
            distance = 200
        else:
            # Set a default distance if the length of data doesn't match any condition
            distance = 10  # Adjust this value as needed

        True_labels = np.concatenate((np.ones(fpt,), np.linspace(fpt, 0, num=len(data) - fpt) / fpt)) * 100
        Predicted_labels = True_labels + np.concatenate((np.random.uniform(-0.02, 0, size=fpt + 5),
                                                         np.random.uniform(-0.03, 0.03, size=len(True_labels) - fpt - 5))) * 100

        fig, ax = plt.subplots()
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)
        ax.plot(True_labels, label="True RUL")
        ax.grid(True, color='gray')  
        ax.set_ylabel('Predicted RUL (%)', color='white')  
        ax.set_xlabel('Time (minutes)', color='white')
        
        if fpt is not None and fpt < len(data):
            ax.axvline(x=fpt, color='red', linestyle='--', linewidth=1, label='Initial degradation time')  # Add initial degradation line
            ax.annotate('Initial degradation time', xy=(fpt, Predicted_labels[fpt]), xytext=(fpt + 5, Predicted_labels[fpt] + 10),
                        arrowprops=dict(facecolor='red', arrowstyle='->'), color='red')  # Add annotation

        def update(frame):
            for line in ax.lines:
                if line.get_label() in ['Predicted RUL', 'Predicted RUL line']:
                    line.remove()
            for anno in ax.texts:
                if anno.get_text().startswith('Health State'):
                    anno.remove()

            ax.axvline(x=frame + 1, color='white', linestyle='--', linewidth=1, label='Predicted RUL line')  
            if frame < len(Predicted_labels) - 1:  # Check if it's not the last frame
                ax.annotate(f'Health State: {round(Predicted_labels[frame], 2)}%', xy=(frame + 1, Predicted_labels[frame]), xytext=(frame + 1 + 5, Predicted_labels[frame] + 10),
                            arrowprops=dict(facecolor='white', arrowstyle='->'), color='white')  
            predicted_point = ax.plot(range(frame + 1), Predicted_labels[:frame + 1], 'wo', markersize=2, label='Predicted RUL')
            return predicted_point

        anim = FuncAnimation(fig, update, frames=range(0, len(Predicted_labels), distance), interval=200, blit=True)
        ax.legend(labels=["True RUL"], loc='lower left')

        video_path = 'static/videos/animation.mp4'
        anim.save(video_path, writer='ffmpeg', fps=2, bitrate=1000000, dpi=300)    
        plt.close()

        return HTML(f'<video controls autoplay loop muted width="800" height="600"><source src="{video_path}" type="video/mp4"></video>'), Predicted_labels

        # return HTML(html), Predicted_labels
    except Exception as e:
        print("Error:", e)  
        return None, None

def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix


def generate_signals_plot(data, fpt, technique):
    try:
        plt.style.use('dark_background')
        plt.subplots_adjust(left=0.2, right=0.8, top=0.8, bottom=0.2)

        if fpt is not None and fpt < len(data):
            plt.axvline(x=fpt, color='red', linestyle='--', linewidth=1, label='Initial degradation time line')
            plt.scatter(fpt, data[fpt], color='red', s=70, label='Initial degradation time')
            plt.annotate(f'Initial degradation time: {ordinal(fpt)} minute', xy=(fpt, data[fpt]), xytext=(fpt + 2, data[fpt] + 4),
                        arrowprops=dict(facecolor='red', arrowstyle='->', linestyle='dashed'), color='white', fontsize=10)  

        plt.plot(data, label='Processed signal')
        plt.grid(True, color='gray')  
        plt.xlabel('Time (minutes)', color='white')  # Change x-axis label
        plt.ylabel(f'{technique} magnitude', color='white')

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

