import {useState} from 'react';
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000'
})

function QuestionForm() {
    const [question, setQuestion] = useState('');
    const [answer, setAnswer] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        console.log("Question:", question);
        const response =await api.post('/chat', {message: question});
        setAnswer(response.data.answer);

    }

    return (
        <div>
        <form className='form'>
            <input className='form-input' type="text" value={question} onChange={(e) => setQuestion(e.target.value)} />
            <button className='form-button' type="submit" onClick={handleSubmit}>Submit</button>
        </form>
        <div>
            <h2>Answer</h2>
            <p>{answer}</p>
        </div>
        </div>  
    );
}

export default QuestionForm;