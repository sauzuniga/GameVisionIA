import { useState } from 'react'

import GameForm from './components/GameForm'

import ResultPanel from './components/ResultPanel'

import ChatBot from './components/ChatBot'

import HistoryPanel from './components/HistoryPanel'

import './App.css'



function App() {

  const [prediction, setPrediction] = useState(null)

  const [sessionId, setSessionId] = useState(null)

  const [showHistory, setShowHistory] = useState(false)

  const [formKey, setFormKey] = useState(0)

  const handlePredictionResult = (result) => {

    setPrediction(result)

    setSessionId(result.session_id)

  }



  const handleSelectHistory = (pred) => {

    setPrediction(pred)

    setSessionId(pred.session_id)

    setShowHistory(false)

  }

  const handleReset = () => {
  setPrediction(null)
  setSessionId(null)
  setFormKey(prev => prev + 1)
  }

  const buildPredictionContext = () => {

    if (!prediction) return ''

    return `El juego analizado tiene una probabilidad de éxito comercial del ${(prediction.probability * 100).toFixed(1)}%, con un potencial ${prediction.potential_level}. Clase predicha: ${prediction.predicted_class === 1 ? 'Exitoso' : 'No exitoso'}.`

  }



  return (

    <div className="app-container">

      <header className="app-header">

        <div className="header-content">

          <h1 className="app-title" onClick={handleReset} style={{ cursor: 'pointer' }}>
            <span className="title-game">Game</span>
            <span className="title-vision">Vision</span>
            <span className="title-ia"> IA</span>
          </h1>

          <p className="app-subtitle">Predicción de potencial comercial en Steam</p>

        </div>

        <button className="history-btn" onClick={() => setShowHistory(true)}>

          📋 Historial

        </button>

      </header>



      <main className="app-main">

        <div className="left-panel">

          <GameForm key={formKey} onResult={handlePredictionResult} />

        </div>



        <div className="right-panel">

          {prediction ? (

            <>

              <ResultPanel prediction={prediction} />

              <ChatBot

                sessionId={sessionId}

                predictionContext={buildPredictionContext()}

              />

            </>

          ) : (

            <div className="empty-state">

              <div className="empty-icon">🎮</div>

              <p>Ingresá los datos de tu juego para ver el análisis</p>

            </div>

          )}

        </div>

      </main>



      {showHistory && (

        <HistoryPanel

          onSelectPrediction={handleSelectHistory}

          onClose={() => setShowHistory(false)}

        />

      )}

    </div>

  )

}



export default App 

