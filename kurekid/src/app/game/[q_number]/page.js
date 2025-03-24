"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function QuestionPage() {
    const { id } = useParams();
    const [question, setQuestion] = useState(null);

    useEffect(() => {
        async function fetchQuestion() {
            try {
                const res = await fetch(`http://localhost:8000/scenario/${id}`);
                const data = await res.json();
                setQuestion(data);
            } catch (error) {
                console.error("Error fetching question:", error);
            }
        }

        if (id) fetchQuestion();
    }, [id]);

    if (!question) return <p>Loading...</p>;

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold">{question.title}</h1>
            <p className="mt-2">{question.description}</p>
            <h2 className="mt-4 font-semibold">Options:</h2>
            <ul className="list-disc pl-5">
                {Object.values(question.options).map((option) => (
                    <li key={option.id} className="mt-1">
                        {option.title}
                    </li>
                ))}
            </ul>
        </div>
    );
}
