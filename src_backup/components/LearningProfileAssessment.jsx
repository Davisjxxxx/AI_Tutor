import React, { useState, useEffect } from 'react';

export default function LearningProfileAssessment({ user, onProfileComplete }) {
  const [currentSection, setCurrentSection] = useState(0);
  const [responses, setResponses] = useState({});
  const [assessmentQuestions, setAssessmentQuestions] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const sections = [
    { id: 'learning_style', title: '🎯 Learning Style', description: 'How do you learn best?' },
    { id: 'neurodivergent_screening', title: '🧠 Neurodivergent Profile', description: 'Understanding your unique brain' },
    { id: 'cognitive_strengths', title: '💪 Cognitive Strengths', description: 'What are your superpowers?' },
    { id: 'motivation_preferences', title: '🚀 Motivation Style', description: 'What keeps you engaged?' }
  ];

  useEffect(() => {
    fetchAssessmentQuestions();
  }, []);

  const fetchAssessmentQuestions = async () => {
    try {
      const response = await fetch('http://localhost:9000/api/assessment/questions');
      const data = await response.json();
      setAssessmentQuestions(data);
      setIsLoading(false);
    } catch (error) {
      console.error('Error fetching assessment questions:', error);
      setIsLoading(false);
    }
  };

  const handleResponse = (questionIndex, answer) => {
    const sectionKey = sections[currentSection].id;
    setResponses(prev => ({
      ...prev,
      [sectionKey]: {
        ...prev[sectionKey],
        [questionIndex]: answer
      }
    }));
  };

  const nextSection = () => {
    if (currentSection < sections.length - 1) {
      setCurrentSection(currentSection + 1);
    } else {
      completeAssessment();
    }
  };

  const prevSection = () => {
    if (currentSection > 0) {
      setCurrentSection(currentSection - 1);
    }
  };

  const completeAssessment = async () => {
    try {
      // Transform responses into learning profile format
      const profile = {
        user_id: user?.id || 'anonymous',
        age: 25, // Would get from form
        name: user?.email?.split('@')[0] || 'User',
        learning_style_primary: "visual", // Would derive from responses
        communication_preference: "supportive",
        processing_speed: "moderate",
        attention_profile: "short_bursts",
        motivation_style: "achievement",
        has_adhd: responses.neurodivergent_screening?.[0] === 'yes',
        has_autism: responses.neurodivergent_screening?.[1] === 'yes',
        prefers_structure: true,
        needs_emotional_support: true,
        strong_subjects: ["programming"],
        interest_areas: ["frontend", "ai"],
        short_term_goals: ["Learn React"],
        long_term_goals: ["Become full-stack developer"]
      };

      const response = await fetch('http://localhost:9000/api/profile/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      });

      const result = await response.json();
      if (result.success) {
        onProfileComplete(result);
      }
    } catch (error) {
      console.error('Error creating profile:', error);
    }
  };

  const getCurrentQuestions = () => {
    if (!assessmentQuestions) return [];
    const sectionKey = sections[currentSection].id;
    return assessmentQuestions[sectionKey] || [];
  };

  const isCurrentSectionComplete = () => {
    const questions = getCurrentQuestions();
    const sectionKey = sections[currentSection].id;
    const sectionResponses = responses[sectionKey] || {};
    return questions.every((_, index) => sectionResponses[index] !== undefined);
  };

  if (isLoading) {
    return (
      <div className="bg-darkglass rounded-2xl p-8 shadow-glass backdrop-blur">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-zinc-300">Loading assessment questions...</p>
        </div>
      </div>
    );
  }

  const currentSectionData = sections[currentSection];
  const questions = getCurrentQuestions();
  const progress = ((currentSection + 1) / sections.length) * 100;

  return (
    <div className="bg-darkglass rounded-2xl p-8 shadow-glass backdrop-blur">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-primary">Learning Profile Assessment</h2>
          <span className="text-sm text-zinc-400">
            {currentSection + 1} of {sections.length}
          </span>
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-glass rounded-full h-2 mb-4">
          <div 
            className="bg-gradient-to-r from-primary to-accent h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%` }}
          ></div>
        </div>
        
        <div className="text-center">
          <h3 className="text-xl font-semibold text-white mb-2">
            {currentSectionData.title}
          </h3>
          <p className="text-zinc-300">{currentSectionData.description}</p>
        </div>
      </div>

      {/* Questions */}
      <div className="space-y-6 mb-8">
        {questions.map((question, index) => (
          <div key={index} className="bg-glass rounded-lg p-6">
            <h4 className="text-white font-medium mb-4">{question}</h4>
            
            {/* Multiple choice or scale based on question type */}
            {question.includes('Rate your') ? (
              // Scale questions (1-10)
              <div className="flex items-center space-x-2">
                <span className="text-sm text-zinc-400">1</span>
                {[...Array(10)].map((_, i) => (
                  <button
                    key={i}
                    onClick={() => handleResponse(index, i + 1)}
                    className={`w-8 h-8 rounded-full border-2 text-sm font-medium transition-all ${
                      responses[currentSectionData.id]?.[index] === i + 1
                        ? 'bg-primary border-primary text-white'
                        : 'border-zinc-400 text-zinc-400 hover:border-primary'
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
                <span className="text-sm text-zinc-400">10</span>
              </div>
            ) : question.includes('Do you') ? (
              // Yes/No questions
              <div className="flex space-x-4">
                {['Yes', 'No', 'Sometimes'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handleResponse(index, option.toLowerCase())}
                    className={`px-6 py-2 rounded-lg font-medium transition-all ${
                      responses[currentSectionData.id]?.[index] === option.toLowerCase()
                        ? 'bg-primary text-white'
                        : 'bg-glass text-zinc-300 hover:bg-primary/20'
                    }`}
                  >
                    {option}
                  </button>
                ))}
              </div>
            ) : (
              // Multiple choice questions
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {['a', 'b', 'c', 'd'].map((option) => (
                  <button
                    key={option}
                    onClick={() => handleResponse(index, option)}
                    className={`p-3 rounded-lg text-left transition-all ${
                      responses[currentSectionData.id]?.[index] === option
                        ? 'bg-primary text-white'
                        : 'bg-glass text-zinc-300 hover:bg-primary/20'
                    }`}
                  >
                    {option.toUpperCase()})
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={prevSection}
          disabled={currentSection === 0}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${
            currentSection === 0
              ? 'bg-glass text-zinc-500 cursor-not-allowed'
              : 'bg-glass text-white hover:bg-primary/20'
          }`}
        >
          Previous
        </button>
        
        <button
          onClick={nextSection}
          disabled={!isCurrentSectionComplete()}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${
            !isCurrentSectionComplete()
              ? 'bg-glass text-zinc-500 cursor-not-allowed'
              : currentSection === sections.length - 1
              ? 'bg-accent text-white hover:bg-primary shadow-glass'
              : 'bg-primary text-white hover:bg-accent shadow-glass'
          }`}
        >
          {currentSection === sections.length - 1 ? 'Complete Assessment' : 'Next'}
        </button>
      </div>
    </div>
  );
}