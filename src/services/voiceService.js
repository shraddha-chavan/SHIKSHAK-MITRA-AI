class VoiceService {
  constructor() {
    this.synthesis = window.speechSynthesis;
    this.isEnabled = false;
    this.previousScores = {};
    this.voice = null;
    this.initVoice();
  }

  initVoice() {
    const voices = this.synthesis.getVoices();
    this.voice = voices.find(voice => voice.lang === 'en-US') || voices[0];
    
    if (!this.voice) {
      this.synthesis.addEventListener('voiceschanged', () => {
        const voices = this.synthesis.getVoices();
        this.voice = voices.find(voice => voice.lang === 'en-US') || voices[0];
      });
    }
  }

  speak(text, priority = false) {
    if (!this.isEnabled && !priority) return;
    
    if (this.synthesis.speaking) {
      this.synthesis.cancel();
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = this.voice;
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    this.synthesis.speak(utterance);
  }

  enable() {
    this.isEnabled = true;
    this.speak("Voice assistant activated. I will notify you of score changes and provide suggestions.", true);
  }

  disable() {
    this.isEnabled = false;
    this.synthesis.cancel();
  }

  toggle() {
    if (this.isEnabled) {
      this.disable();
    } else {
      this.enable();
    }
    return this.isEnabled;
  }

  checkScoreDrops(currentScores) {
    if (!this.isEnabled) return;

    Object.keys(currentScores).forEach(scoreType => {
      const current = currentScores[scoreType];
      const previous = this.previousScores[scoreType];

      if (previous && current < previous) {
        const drop = previous - current;
        const dropPercentage = (drop / previous) * 100;

        if (dropPercentage >= 10) {
          this.announceScoreDrop(scoreType, current, dropPercentage);
        }
      } else if (previous && current > previous) {
        const increase = current - previous;
        const increasePercentage = (increase / previous) * 100;

        if (increasePercentage >= 10) {
          this.announceScoreIncrease(scoreType, current, increasePercentage);
        }
      }
    });

    this.previousScores = { ...currentScores };
  }

  announceScoreDrop(scoreType, currentScore, dropPercentage) {
    const message = `Alert! ${scoreType.replace('_', ' ')} score has dropped by ${Math.round(dropPercentage)}% to ${currentScore}%. `;
    const suggestion = this.getAISuggestion(scoreType);
    
    this.speak(message + suggestion, true);
  }

  announceScoreIncrease(scoreType, currentScore, increasePercentage) {
    const message = `Great! ${scoreType.replace('_', ' ')} score has improved by ${Math.round(increasePercentage)}% to ${currentScore}%. `;
    const encouragement = this.getEncouragement(scoreType);
    
    this.speak(message + encouragement, true);
  }

  getAISuggestion(scoreType) {
    const suggestions = {
      attention_score: "Try using interactive questioning techniques to regain student attention.",
      engagement_score: "Consider incorporating visual aids or hands-on activities to boost engagement.",
      participation_score: "Encourage more student participation with group discussions or peer activities.",
      overall_engagement: "Take a short break or change teaching method to re-energize the class.",
      comprehension_score: "Slow down the pace and check for understanding more frequently."
    };

    return suggestions[scoreType] || "Consider adjusting your teaching approach to improve student response.";
  }

  getEncouragement(scoreType) {
    const encouragements = {
      attention_score: "Students are becoming more focused. Keep up the good work!",
      engagement_score: "Excellent! Your teaching methods are working well.",
      participation_score: "Students are participating more actively. Great job!",
      overall_engagement: "The class energy is improving. Continue with this approach.",
      comprehension_score: "Students are understanding better. Your explanations are effective."
    };

    return encouragements[scoreType] || "Keep up the excellent teaching!";
  }

  announceWelcome() {
    if (this.isEnabled) {
      this.speak("Welcome to teacher mode. Voice assistant is ready to help monitor your class performance.");
    }
  }

  announceScores(scores) {
    if (!this.isEnabled) return;
    
    const message = `Current scores: Engagement ${scores.overall_engagement}%, Attention ${scores.attention_score}%, Participation ${scores.participation_score}%.`;
    this.speak(message);
  }
}

export const voiceService = new VoiceService();