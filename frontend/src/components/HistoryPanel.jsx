import { useState, useEffect } from 'react'

import { getHistory } from '../api'



const getLevelColor = (level) => {

  if (level === 'Alto') return '#4ecdc4'

  if (level === 'Medio') return '#f7b731'

  return '#fc5c65'

}



export default function HistoryPanel({ onSelectPrediction, onClose }) {

  const [history, setHistory] = useState([])

  const [loading, setLoading] = useState(true)



  useEffect(() => {

    getHistory().then(data => {

      setHistory(data)

      setLoading(false)

    })

  }, [])



  return (

    <div className="history-overlay">

      <div className="history-panel">

        <div className="history-header">

          <h2 className="history-title">Historial de predicciones</h2>

          <button className="history-close" onClick={onClose}>✕</button>

        </div>



        {loading ? (

          <p className="history-empty">Cargando...</p>

        ) : history.length === 0 ? (

          <p className="history-empty">No hay predicciones guardadas</p>

        ) : (

          <div className="history-list">

            {history.map(pred => (

              <div

                key={pred.id}

                className="history-item"

                onClick={() => onSelectPrediction(pred)}

              >

                <div className="history-item-left">

                  <span

                    className="history-level"

                    style={{ color: getLevelColor(pred.potential_level) }}

                  >

                    {pred.potential_level}

                  </span>

                  <span className="history-genres">

                    {pred.genres || 'Sin géneros'}

                  </span>

                </div>

                <div className="history-item-right">

                  <span

                    className="history-prob"

                    style={{ color: getLevelColor(pred.potential_level) }}

                  >

                    {Math.round(pred.probability * 100)}%

                  </span>

                  <span className="history-date">

                    {new Date(pred.created_at).toLocaleDateString('es-ES')}

                  </span>

                </div>

              </div>

            ))}

          </div>

        )}

      </div>

    </div>

  )

} 

