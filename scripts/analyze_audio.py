import streamlit as st
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import pandas as pd

class AudioAnalyzer:
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.y, self.sr = librosa.load(self.file_path, sr=None)
        
        #Parameters
        self.frame_length = 0.032 # 32 ms
        self.hop_length = 0.01 # 10 ms
        self.n_fft = int(self.sr* self.frame_length)
        self.hop_length_samples = int(self.sr* self.hop_length)

    def get_waveform(self):
        print("Plotting Waveform")
                
        #Plot Waveform
        st.markdown("**Waveform**")
        fig, ax = plt.subplots()
        librosa.display.waveshow(self.y, sr=self.sr)
        st.pyplot(fig)
        return 
        

    #Fundamental Frequency
    def get_fundamental_frequency(self):
        
        print("Plotting Fundamental Frequency")
        f0, voiced_flag, voiced_probs = librosa.pyin(self.y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=self.sr, hop_length=self.hop_length_samples)
        
        f0_average = np.mean(f0[voiced_flag])
        
        f0_max = np.max(f0[voiced_flag])
        
        f0_min = np.min(f0[voiced_flag])
        
        f0_range = 12 * np.log2(f0_max / f0_min)
        
        #Plot Fundamental Frequency
        times = librosa.times_like(f0, sr=self.sr, hop_length=self.hop_length_samples)
        
        array_2D = np.array([f0, times]).T
        
        
        df = pd.DataFrame(array_2D, columns=['f0', 'time'])
        st.markdown("**Fundamental Frequency**")
        st.line_chart(df.set_index('time'))
        

            
        
        # self.axs[1].plot(times, f0, label='Fundamental Frequency (f0)')
        # self.axs[1].set_xlabel('Time (s)')
        # self.axs[1].set_ylabel('Frequency (Hz)')
        # self.axs[1].set_title('Fundamental Frequency')
        # self.axs[1].legend()
        print("F0 Average:", f0_average)
        print("F0 Range:", f0_range)
        
        return f0_average, f0_range
    def get_energy_db(self):
        print("Plotting EnergyDB")
        energy = librosa.feature.rms(y=self.y, frame_length=self.n_fft, hop_length=self.hop_length_samples)[0]
        energy_db = librosa.amplitude_to_db(energy, ref=np.max)
        
        threshold_db = -40  # example threshold for pauses
        
        average_energy = np.mean(energy_db)
        pause_frames = energy_db < threshold_db
        
        pause_intervals = librosa.effects.split(self.y, top_db=np.abs(threshold_db), frame_length=self.n_fft, hop_length=self.hop_length_samples)
        
        mean_pause_duration = np.mean(pause_intervals)
        
        # Calculate time in seconds
        frames = range(len(energy_db))
        t = librosa.frames_to_time(frames, sr=self.sr, hop_length=self.hop_length_samples)
        pause_df = pd.DataFrame({'time': t[pause_frames], 'pause_time': energy_db[pause_frames]})
        
        # Create DataFrame for Streamlit
        db_normal_speech = []
        for db in energy_db:
            if  -15 < db < -20:
                db_normal_speech.append(db)
        db_normal_ratio = len(db_normal_speech) / len(energy_db)
        energy_db = pd.DataFrame({'time': t, 'energy_db': energy_db})
        
        st.markdown("**Pause Times**")
        st.line_chart(pause_df.set_index('time'))
        
        st.markdown("---")
        st.markdown("**Energy DB**")
        st.line_chart(energy_db.set_index('time'))

        print("Average Energy:", average_energy)
        print("Mean Pause Duration:", mean_pause_duration)
        print("db_normal_ratio:", db_normal_ratio)

        return average_energy, mean_pause_duration, db_normal_ratio