"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import './App.css';

export default function Page() {
    const [questions, setQuestions] = useState([]);

    useEffect(() => {
        async function fetchQuestions() {
            try {
                // Fetch all question IDs
                const res = await fetch("http://localhost:8000/scenario/all");
                const questionIds = await res.json();
                console.log(questionIds);

                // Fetch question details (title) for each ID
                const questionDetails = await Promise.all(
                    questionIds.map(async (id, index) => {
                        console.log(id);
                        const qRes = await fetch(`http://localhost:8000/scenario/${id}`);
                        const qData = await qRes.json();
                        console.log(qRes)
                        return { number: index + 1, id, title: qData.title };
                    })
                );

                setQuestions(questionDetails);
            } catch (error) {
                console.error("Error fetching questions:", error);
            }
        }

        fetchQuestions();
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">These are the questions.</h1>
            <ul className="list-disc pl-5">
                {questions.map((q) => (
                    <li key={q.id} className="mb-2">
                        <Link href={`/game/${q.id}`} className="text-blue-500 hover:underline">
                            {q.number}. {q.title}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}
