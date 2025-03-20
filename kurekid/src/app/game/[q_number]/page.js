'use client'

import { useParams } from 'next/navigation'


const questions = {
  '1': {
    id: 1,
    title: "What is your name",
    coverImage: "cover.png",
    coverVideo: null,
    options: [
      {
        id: 1,
        correctOption: false,
        text: "Option 1",
        img: "img.png",
      },
      {
        id: 2,
        correctOption: true,
        text: "Option 2",
        img: "img.png"
      },
      {
        id: 3,
        correctOption: false,
        text: "Option 3",
        img: "img.png"
      },
      {
        id: 4,
        correctOption: false,
        text: "Option 4",
        img: "img.png"
      }
    ],
    correctOptionId: 2
  },
  '2': {
    id: 2,
    title: "What are you doing",
    coverImage: "cover.png",
    coverVideo: null,
    options: [
      {
        id: 1,
        correctOption: false,
        text: "Option 1",
        img: "img.png",
      },
      {
        id: 2,
        correctOption: false,
        text: "Option 2",
        img: "img.png"
      },
      {
        id: 3,
        correctOption: true,
        text: "Option 3",
        img: "img.png"
      },
      {
        id: 4,
        correctOption: false,
        text: "Option 4",
        img: "img.png"
      }
    ],
    correctOptionId: 2
  }
}

function optionClicked(data) {
  if (data.correctOption) {
    console.log("YAAAA!! Correct!")
  }
  console.log("option id: " + data.id);

}

function Option({ option }) {
  return (
    <button onClick={()=>optionClicked(option)}>
      <h5>{option.id}</h5>
      <h2>{option.text}</h2>
    </button>
  )
}

function Question({ question_id }) {
  const questionData = questions[question_id];
  if (!questionData) { return ( <h3>Question {question_id} not found!</h3> ) }

  return (
    <div>

      <h1>{ questionData.title }</h1>

      <div className='options'>

        {
          questionData.options.map( (option) => ( <Option key={option.id} option={option}></Option> ) )
        }

      </div>

    </div>
  )

}


export default function Page() {
  const { q_number } = useParams();

  return (
    <>
      <h1>Hi {q_number}</h1>
      <Question question_id={q_number}></Question>
    </>
  )
}