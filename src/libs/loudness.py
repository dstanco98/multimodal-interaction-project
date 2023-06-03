import wave
import sys
import pyaudio
import audioop
import numpy as np

class Loudness():
    """
    Compute the RMS level of the audio data.
    """
    
    def __init__(self, width=2, normalization=32767) -> None:
        """
        Args:
            width (int): Width of the audio data. Default is 2.
            normalization (int): Normalization of the audio data. 
                Default is 32767.
                The division by 32767 is performed in the code to normalize the 
                RMS (Root Mean Square) value of the audio data.
                In audio processing, the values of audio samples are typically 
                represented as signed 16-bit integers, with a range from -32768 
                to 32767.
        """
        self.width = width
        self.normalization = normalization
    
    
    def compute_loudness(self, data)->float:
        """
        Compute the rms level of the audio data.
        Return the root-mean-square of the fragment, i.e. sqrt(sum(S_i^2)/n).
        This is a measure of the power in an audio signal.
        
        Args:
            data (bytes): Audio data.
            width (int): Width of the audio data.
        
        Returns:
            rms (float): Root Mean Square (RMS) level of the audio data.
                Value is between 0 and 1.
        """
        data = np.frombuffer(data, dtype=np.int16)
        data = np.amax(data)
        return audioop.rms(data, self.width) / self.normalization
    
    
    def display_loudness(self, data)->None:
        """
        Print the rms level of the audio data.
        # NOTE! In the future this methodwill used to give a visual feedback
        
        Args:
            data (bytes): Audio data.
        """
        rms = self.compute_loudness(data)
        if rms >= 0.5:
            print('Attention!!! There is a lot of noise, the RMS value is %.3f' % rms)
        pass