import { useState, useEffect, useRef } from 'react'

import { sendChatMessage, getChatMessages } from '../api'



const quickQuestions = [

  '¿Por qué obtuvo este resultado?',

  '¿Cómo puedo mejorar el potencial?',

  '¿Qué géneros funcionan mejor en Steam?',

  '¿El precio afecta el éxito?'

]



export default function ChatBot({ sessionId, predictionContext }) {

  const [messages, setMessages] = useState([])

  const [input, setInput] = useState('')

  const [loading, setLoading] = useState(false)

  const bottomRef = useRef(null)



  useEffect(() => {

    if (sessionId) {

      getChatMessages(sessionId).then(msgs => setMessages(msgs))

    }

  }, [sessionId])



  useEffect(() => {

    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })

  }, [messages])



  const sendMessage = async (text) => {

    const messageText = text || input

    if (!messageText.trim() || !sessionId) return



    const userMsg = { role: 'user', content: messageText }

    setMessages(prev => [...prev, userMsg])

    setInput('')

    setLoading(true)



    try {

      const response = await sendChatMessage(sessionId, messageText, predictionContext)

      setMessages(prev => [...prev, { role: 'assistant', content: response.content }])

    } catch (e) {

      setMessages(prev => [...prev, { role: 'assistant', content: 'Error al conectar con el chatbot.' }])

    } finally {

      setLoading(false)

    }

  }



  return (

    <div className="chat-card">

      <h2 className="chat-title">💬 GameVision Assistant</h2>



      <div className="quick-questions">

        {quickQuestions.map((q, i) => (

          <button

            key={i}

            className="quick-btn"

            onClick={() => sendMessage(q)}

            disabled={loading}

          >

            {q}

          </button>

        ))}

      </div>



      <div className="chat-messages">

        {messages.length === 0 && (

          <p className="chat-empty">Hacé una pregunta sobre el resultado del análisis</p>

        )}

        {messages.map((msg, i) => (

          <div key={i} className={`message ${msg.role === 'user' ? 'message-user' : 'message-ai'}`}>

            <div className="message-bubble">

              {msg.content}

            </div>

          </div>

        ))}

        {loading && (

          <div className="message message-ai">

            <div className="message-bubble typing">

              <span></span><span></span><span></span>

            </div>

          </div>

        )}

        <div ref={bottomRef} />

      </div>



      <div className="chat-input-row">

        <input

          type="text"

          className="chat-input"

          placeholder="Escribí tu pregunta..."

          value={input}

          onChange={e => setInput(e.target.value)}

          onKeyDown={e => e.key === 'Enter' && sendMessage()}

          disabled={loading}

        />

        <button

          className="chat-send-btn"

          onClick={() => sendMessage()}

          disabled={loading || !input.trim()}

        >

          Enviar

        </button>

      </div>

    </div>

  )

} 

