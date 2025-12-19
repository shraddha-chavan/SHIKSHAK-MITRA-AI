import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Mic, MicOff } from 'lucide-react';
import { voiceService } from '@/services/voiceService';

const VoiceAssistant = () => {
  const [isEnabled, setIsEnabled] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    const checkSpeaking = () => {
      setIsSpeaking(window.speechSynthesis.speaking);
    };

    const interval = setInterval(checkSpeaking, 100);
    return () => clearInterval(interval);
  }, []);

  const toggleVoice = () => {
    const enabled = voiceService.toggle();
    setIsEnabled(enabled);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="relative">
        {/* Colorful background rings */}
        <div className="absolute inset-0 rounded-full bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 animate-spin" style={{width: '80px', height: '80px'}}></div>
        <div className="absolute inset-1 rounded-full bg-gradient-to-r from-blue-500 via-green-500 to-yellow-500 animate-pulse" style={{width: '72px', height: '72px'}}></div>
        
        <Button
          onClick={toggleVoice}
          size="lg"
          className={`relative rounded-full w-16 h-16 shadow-2xl transition-all duration-500 transform hover:scale-110 ${
            isEnabled 
              ? 'bg-gradient-to-r from-green-400 to-blue-500 animate-bounce' 
              : 'bg-gradient-to-r from-gray-400 to-gray-600'
          }`}
        >
          <div className="relative z-10">
            {isEnabled ? (
              <Mic className={`h-8 w-8 text-white drop-shadow-lg ${
                isSpeaking ? 'animate-pulse scale-125' : 'animate-bounce'
              }`} />
            ) : (
              <MicOff className="h-8 w-8 text-white opacity-70" />
            )}
            
            {/* Rainbow speaking waves */}
            {isSpeaking && (
              <>
                <div className="absolute -inset-4 rounded-full border-4 border-yellow-400 animate-ping opacity-60"></div>
                <div className="absolute -inset-6 rounded-full border-4 border-pink-400 animate-ping opacity-40" style={{animationDelay: '0.2s'}}></div>
                <div className="absolute -inset-8 rounded-full border-4 border-cyan-400 animate-ping opacity-20" style={{animationDelay: '0.4s'}}></div>
              </>
            )}
            
            {/* Bright live indicator */}
            {isEnabled && (
              <div className="absolute -top-2 -right-2 w-4 h-4 bg-gradient-to-r from-red-500 to-orange-500 rounded-full animate-pulse shadow-lg">
                <div className="absolute inset-0 bg-gradient-to-r from-yellow-400 to-red-500 rounded-full animate-ping"></div>
                <div className="absolute inset-1 bg-white rounded-full animate-pulse"></div>
              </div>
            )}
          </div>
        </Button>
        
        {/* Floating particles */}
        {isEnabled && (
          <>
            <div className="absolute top-0 left-0 w-2 h-2 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0s'}}></div>
            <div className="absolute top-2 right-0 w-1 h-1 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.3s'}}></div>
            <div className="absolute bottom-0 left-2 w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce" style={{animationDelay: '0.6s'}}></div>
          </>
        )}
      </div>
      
      {/* Status text - only show when voice is ON */}
      {isEnabled && (
        <div className={`absolute bottom-full right-0 mb-3 text-sm font-bold px-3 py-1 rounded-full shadow-lg ${
          isSpeaking 
            ? 'bg-gradient-to-r from-yellow-400 to-orange-500 text-white animate-pulse' 
            : 'bg-gradient-to-r from-green-400 to-blue-500 text-white'
        }`}>
          {isSpeaking ? '🎤 Speaking...' : '🔊 Voice ON'}
        </div>
      )}
    </div>
  );
};

export default VoiceAssistant;