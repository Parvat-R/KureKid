"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import './App.css';

export default function QuestionPage() {
    const { q_number } = useParams();
    const [question, setQuestion] = useState(null);
    const [isCorrect, setIsCorrect] = useState(false);
    const [isWrong, setIsWrong] = useState(false);
    const [showTransition, setShowTransition] = useState(false);
    const router = useRouter();

    const id = q_number;

    useEffect(() => {
        async function fetchQuestion() {
            try {
                const res = await fetch(`http://localhost:8000/scenario/${id}`);
                const data = await res.json();
                setQuestion(data);
                setIsCorrect(false);
                setIsWrong(false);
                setShowTransition(false);
            } catch (error) {
                console.error("Error fetching question:", error);
            }
        }

        if (id) fetchQuestion();
    }, [id]);

    function optionClicked(option) {
        if (option.correct) {
            setIsCorrect(true);
            setShowTransition(true);
            
            // Delayed navigation to create a smooth transition
            setTimeout(() => {
                const nextQuestion = (parseInt(q_number) + 1) % 40;
                router.push(`/game/${nextQuestion}`);
            }, 2000);
        } else {
            setIsWrong(true);
            
            // Remove shake after animation
            setTimeout(() => {
                setIsWrong(false);
            }, 1000);
        }
    }

    if (!question) return <p>Loading adventure...</p>;

    return (
        <div className={`p-6 
            ${isCorrect ? 'correct-answer' : ''} 
            ${showTransition ? 'transition-out' : ''} 
            ${isWrong ? 'wrong-answer shake' : ''}`
        }>
            {showTransition && (
                <div className="celebration-overlay">
                    <div className="confetti"></div>
                    <div className="celebration-message">Correct! Great Job!</div>
                </div>
            )}
            <h1 className="text-2xl font-bold">{question.title}</h1>
            <p className="mt-2">{question.description}</p>
            <h2 className="mt-4 font-semibold">Choose Your Answer:</h2>
            <div className="options-container">
                {Object.values(question.options).map((option) => (
                    <button 
                        key={option.id} 
                        className="option" 
                        onClick={() => optionClicked(option)}
                    >
                        {option.title}
                    </button>
                ))}
            </div>
        </div>
    );
}