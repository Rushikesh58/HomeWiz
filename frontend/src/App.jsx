import { useState } from 'react'
import './index.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)

  const sendMessage = async () => {
    const userMessage = { role: 'user', text: input }
    setMessages(prev => [...prev, userMessage])
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input, session_id: sessionId }),
    })
    const data = await res.json()
    setSessionId(data.session_id)
    setMessages(prev => [...prev, { role: 'bot', text: data.reply }])
    setInput('')
  }

  return (
    <div className="chat-container">
      <h2>🏘️ Homewiz Chat</h2>
      <div className="chat-box">
        {messages.map((m, i) => (
          <div key={i} className={m.role}>
            <b>{m.role === 'user' ? 'You' : 'Bot'}:</b> {m.text}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && sendMessage()}
        placeholder="Type your message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  )
}

export default App
