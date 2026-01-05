
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.fft import fft, ifft, fftfreq

def generate_messy_data(num_points=1000, noise_amplitude=0.5, anomaly_amplitude=5.0):
    """
    Generates a synthetic dataset with a baseline, noise, and anomalies.
    """
    x = np.linspace(0, 100, num_points)
    
    # 1. Baseline: A slowly varying curve
    baseline = 5 * np.sin(x / 20) + 10 * np.cos(x / 50) + 20
    
    # 2. Anomalies (peaks)
    anomalies = np.zeros_like(x)
    # Add a few sharp peaks at specific locations
    anomalies[150:160] = np.linspace(0, anomaly_amplitude, 10) # Rising peak
    anomalies[160:170] = np.linspace(anomaly_amplitude, 0, 10) # Falling peak
    anomalies[400:410] = anomaly_amplitude * np.exp(-((x[400:410] - x[405])**2) / 2) # Gaussian peak
    anomalies[700:705] = anomaly_amplitude * 0.8 # Sharp spike
    
    # 3. Noise
    noise = noise_amplitude * np.random.randn(num_points)
    
    # Combine all components
    messy_data = baseline + anomalies + noise
    
    return x, messy_data, baseline, anomalies

def fourier_baseline_correction(data, sampling_rate, cutoff_frequency_ratio=0.05):
    """
    Estimates the baseline using a low-pass filter in the frequency domain.
    
    Args:
        data (np.array): The input messy data.
        sampling_rate (float): The sampling rate of the data (e.g., 1 if x is uniformly spaced).
        cutoff_frequency_ratio (float): Ratio of the maximum frequency to keep for the baseline.
                                        Lower values result in a smoother baseline.
    Returns:
        np.array: The estimated baseline.
    """
    N = len(data)
    yf = fft(data) # Perform Fast Fourier Transform
    xf = fftfreq(N, 1 / sampling_rate) # Get the frequencies corresponding to the FFT output

    # Create a low-pass filter: keep only low frequencies for the baseline
    # Frequencies are symmetric, so we filter both positive and negative parts
    cutoff_index = int(N * cutoff_frequency_ratio)
    
    # Zero out high-frequency components
    yf_filtered = np.copy(yf)
    yf_filtered[cutoff_index : N - cutoff_index] = 0
    
    baseline_fft = ifft(yf_filtered) # Perform Inverse Fast Fourier Transform
    
    # The result of ifft can have small imaginary components due to numerical precision,
    # so we take the real part.
    return np.real(baseline_fft)

def detect_anomalies(data_corrected, threshold_std_dev=3):
    """
    Detects anomalies in the baseline-corrected data using a standard deviation threshold.
    
    Args:
        data_corrected (np.array): Data after baseline subtraction.
        threshold_std_dev (float): Number of standard deviations from the mean to consider an anomaly.
    
    Returns:
        tuple: Indices of detected anomalies and their values.
    """
    # Calculate mean and standard deviation of the corrected data
    mean_corrected = np.mean(data_corrected)
    std_corrected = np.std(data_corrected)
    
    # Define upper and lower bounds for normal data
    upper_bound = mean_corrected + threshold_std_dev * std_corrected
    lower_bound = mean_corrected - threshold_std_dev * std_corrected
    
    # Identify points outside these bounds as anomalies
    anomaly_indices = np.where((data_corrected > upper_bound) | (data_corrected < lower_bound))[0]
    anomaly_values = data_corrected[anomaly_indices]
    
    return anomaly_indices, anomaly_values

# --- Main execution ---
if __name__ == "__main__":
    num_points = 1000
    sampling_rate = 1 # Assuming uniform sampling
    
    # 1. Generate messy data
    x, messy_data, true_baseline, true_anomalies = generate_messy_data(num_points=num_points)
    
    # 2. Perform Fourier Transform based baseline correction
    estimated_baseline = fourier_baseline_correction(messy_data, sampling_rate, cutoff_frequency_ratio=0.01)
    
    # 3. Get baseline-corrected data (residuals)
    baseline_corrected_data = messy_data - estimated_baseline
    
    # 4. Detect anomalies in the baseline-corrected data
    # We can use find_peaks for positive deviations, and similar logic for negative ones
    # Or simply threshold the absolute value of the corrected data
    
    # Option A: Using statistical thresholding on absolute deviations
    anomaly_indices_stat, anomaly_values_stat = detect_anomalies(baseline_corrected_data, threshold_std_dev=3)
    
    # Option B: Using scipy.signal.find_peaks for positive peaks (anomalies)
    # We need to adjust parameters like height and prominence based on expected anomaly characteristics
    # For simplicity, let's use a dynamic height threshold based on std dev of corrected data
    peak_height_threshold = np.std(baseline_corrected_data) * 2.5 # A heuristic threshold
    
    positive_anomaly_indices, _ = find_peaks(baseline_corrected_data, height=peak_height_threshold, distance=10) #
    negative_anomaly_indices, _ = find_peaks(-baseline_corrected_data, height=peak_height_threshold, distance=10) # Find dips by inverting
    
    # Combine positive and negative anomalies from find_peaks
    anomaly_indices_peaks = np.unique(np.concatenate((positive_anomaly_indices, negative_anomaly_indices)))
    anomaly_values_peaks = messy_data[anomaly_indices_peaks]

    # --- Visualization ---
    plt.figure(figsize=(15, 10))

    # Plot 1: Original Messy Data with True Baseline and Anomalies
    plt.subplot(3, 1, 1)
    plt.plot(x, messy_data, label='Original Messy Data', alpha=0.7)
    plt.plot(x, true_baseline, label='True Baseline', linestyle='--', color='green')
    plt.scatter(x[true_anomalies != 0], messy_data[true_anomalies != 0], color='red', marker='o', s=50, label='True Anomalies', zorder=5)
    plt.title('1. Original Messy Data with True Components')
    plt.legend()
    plt.grid(True)

    # Plot 2: Estimated Baseline and Baseline-Corrected Data
    plt.subplot(3, 1, 2)
    plt.plot(x, messy_data, label='Original Messy Data', alpha=0.7)
    plt.plot(x, estimated_baseline, label='Estimated Baseline (FFT)', color='orange', linestyle='-')
    plt.plot(x, baseline_corrected_data, label='Baseline-Corrected Data', color='purple', alpha=0.7)
    plt.title('2. FFT Baseline Correction')
    plt.legend()
    plt.grid(True)

    # Plot 3: Baseline-Corrected Data with Detected Anomalies
    plt.subplot(3, 1, 3)
    plt.plot(x, baseline_corrected_data, label='Baseline-Corrected Data', color='purple')
    plt.scatter(x[anomaly_indices_stat], baseline_corrected_data[anomaly_indices_stat], 
                color='red', marker='x', s=100, label='Detected Anomalies (Statistical)', zorder=5)
    plt.scatter(x[anomaly_indices_peaks], baseline_corrected_data[anomaly_indices_peaks], 
                color='green', marker='o', s=50, facecolors='none', edgecolors='green', label='Detected Anomalies (find_peaks)', zorder=4)
    plt.axhline(peak_height_threshold, color='gray', linestyle=':', label='Peak Height Threshold')
    plt.axhline(-peak_height_threshold, color='gray', linestyle=':')
    plt.title('3. Anomaly Detection on Baseline-Corrected Data')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

    print(f"Number of anomalies detected by statistical thresholding: {len(anomaly_indices_stat)}")
    print(f"Number of anomalies detected by scipy.signal.find_peaks: {len(anomaly_indices_peaks)}") 