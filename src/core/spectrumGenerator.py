import os
from posixpath import basename
import librosa
import numpy as np
import json

def generate_earwax_spectrum(audio_path):
    # Load audio (preserving original channels)
    y, sr = librosa.load(audio_path, sr=None, mono=False)
    
    # FIX 1: If the audio is mono (1D), duplicate it to create a stereo (2D) array
    if y.ndim == 1:
        y = np.array([y, y])
        
    # 23 milliseconds in samples
    hop_length = int(sr * 0.023) 
    
    spectrum_data = []
    global_peak = 0
    
    # FIX 2: Find absolute loudest point in the audio file for a global reference
    global_ref = np.max(np.abs(y)) 
    
    # Failsafe: Prevent division by zero if an audio file is pure silence
    if global_ref == 0:
        global_ref = 1e-9 

    # Process left and right channels
    for frame_idx in range(0, y.shape[1], hop_length):
        frame_data = {}
        for channel_idx, channel_name in enumerate(["left", "right"]):
            # Get 23ms chunk
            chunk = y[channel_idx, frame_idx:frame_idx + hop_length]
            
            # End of file safeguard
            if len(chunk) == 0:
                break 
                
            # FIX 3: Zero-padding. If chunk is smaller than 1024, pad it with zeros to stop warnings
            if len(chunk) < 1024:
                chunk = np.pad(chunk, (0, 1024 - len(chunk)), mode='constant')

            # Perform FFT and group into 32 Mel bands (using power=1 for linear amplitude)
            stft = np.abs(librosa.stft(chunk, n_fft=1024, hop_length=hop_length))
            # Perform FFT
            stft = np.abs(librosa.stft(chunk, n_fft=1024, hop_length=hop_length))
            
            # Perform FFT
            stft = np.abs(librosa.stft(chunk, n_fft=1024, hop_length=hop_length))
            
            # Revert to standard Mel scale (Jackbox likely uses standard frequency distribution)
            mel_spec = librosa.feature.melspectrogram(S=stft, sr=sr, n_mels=32)
            
            # Back to Decibels! But using the global_ref to preserve the true dynamic range
            db_spec = librosa.amplitude_to_db(mel_spec, ref=global_ref)
            
            # Map a standard -60dB noise floor to our 0-100 visual scale
            normalized = np.interp(db_spec, [-60, 0], [0, 100])
            
            # THE NOISE GATE: If a value is below 10 (very quiet), snap it cleanly to 0
            normalized = np.where(normalized < 10, 0, normalized).astype(int)
            
            # Flatten to 1D array of 32 integers
            band_values = [int(val) for val in np.mean(normalized, axis=1)]
            frame_data[channel_name] = band_values
            
            # Update peak
            local_peak = max(band_values)
            if local_peak > global_peak:
                global_peak = local_peak
                
        if "left" in frame_data and "right" in frame_data:
            spectrum_data.append(frame_data)

    # Format JSON matching Jackbox's structure
    output = {
        "Refresh": 23,
        "Frequencies": spectrum_data,
        "Peak": global_peak
    }
    
    fileName = basename(audio_path).replace(".ogg", ".json")
    
    with open(fileName, "w") as f:
        json.dump(output, f, indent=4)
        

# Using os.path.join for safer pathing, and filtering to ONLY read .ogg files
base_dir = r"E:\SteamLibrary\steamapps\\common\\The Jackbox Party Pack 2\\games\\Earwax\\content\\EarwaxAudio\Audio"
audio_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(".ogg")]

for audio_file in audio_files:
    generate_earwax_spectrum(audio_file)