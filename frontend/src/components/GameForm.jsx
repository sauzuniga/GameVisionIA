import { useState } from 'react'

import { predictGame } from '../api'



const initialForm = {

  price_initial: 9.99,

  is_free: 0,

  release_year: 2026,

  release_month: 6,

  genre_Indie: 0,

  genre_Casual: 0,

  genre_Action: 0,

  genre_Adventure: 0,

  genre_Simulation: 0,

  genre_Strategy: 0,

  genre_RPG: 0,

  genre_Early_Access: 0,

  genre_Free_To_Play: 0,

  cat_Single_player: 0,

  cat_Multi_player: 0,

  cat_PvP: 0,

  cat_Co_op: 0,

  cat_Online_PvP: 0,

  cat_Online_Co_op: 0,

  cat_Shared_Split_Screen: 0,

  cat_Shared_Split_Screen_PvP: 0,

  cat_Shared_Split_Screen_Co_op: 0

}



const genres = [

  { key: 'genre_Indie', label: 'Indie' },

  { key: 'genre_Casual', label: 'Casual' },

  { key: 'genre_Action', label: 'Action' },

  { key: 'genre_Adventure', label: 'Adventure' },

  { key: 'genre_Simulation', label: 'Simulation' },

  { key: 'genre_Strategy', label: 'Strategy' },

  { key: 'genre_RPG', label: 'RPG' },

  { key: 'genre_Early_Access', label: 'Early Access' },

]



const categories = [

  { key: 'cat_Single_player', label: 'Single-player' },

  { key: 'cat_Multi_player', label: 'Multi-player' },

  { key: 'cat_PvP', label: 'PvP' },

  { key: 'cat_Co_op', label: 'Co-op' },

  { key: 'cat_Online_PvP', label: 'Online PvP' },

  { key: 'cat_Online_Co_op', label: 'Online Co-op' },

  { key: 'cat_Shared_Split_Screen', label: 'Split Screen' },

  { key: 'cat_Shared_Split_Screen_PvP', label: 'Split Screen PvP' },

  { key: 'cat_Shared_Split_Screen_Co_op', label: 'Split Screen Co-op' },

]



const months = [

  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',

  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'

]



export default function GameForm({ onResult }) {

  const [form, setForm] = useState(initialForm)

  const [loading, setLoading] = useState(false)

  const [error, setError] = useState(null)



  const handleIsFree = (checked) => {

    setForm(prev => ({

      ...prev,

      is_free: checked ? 1 : 0,

      genre_Free_To_Play: checked ? 1 : 0,

      price_initial: checked ? 0 : 9.99

    }))

  }



  const handleChip = (key) => {

    if (key === 'genre_Free_To_Play') {

      const newVal = form.genre_Free_To_Play === 1 ? 0 : 1

      setForm(prev => ({

        ...prev,

        genre_Free_To_Play: newVal,

        is_free: newVal,

        price_initial: newVal ? 0 : 9.99

      }))

      return

    }

    setForm(prev => ({ ...prev, [key]: prev[key] === 1 ? 0 : 1 }))

  }



  const handleSubmit = async () => {
  const price = parseFloat(form.price_initial)
  const year = parseInt(form.release_year)

  if (isNaN(price) || price < 0) {
    setError('El precio debe ser un número válido mayor a 0')
    return
  }
  if (isNaN(year) || year < 2000 || year > 2100) {
    setError('El año debe estar entre 2000 y 2100')
    return
  }

  const generosSeleccionados = genres.some(g => form[g.key] === 1) || form.genre_Free_To_Play === 1
  const modosSeleccionados = categories.some(c => form[c.key] === 1)

  if (!generosSeleccionados) {
    setError('Seleccioná al menos un género')
    return
  }
  if (!modosSeleccionados) {
    setError('Seleccioná al menos un modo de juego')
    return
  }

  setLoading(true)
  setError(null)
  try {
    const result = await predictGame({
      ...form,
      price_initial: price,
      release_year: year
    })
    onResult(result)
  } catch (_) {
    setError('Error al conectar con el servidor')
  } finally {
    setLoading(false)
  }
}


  return (

    <div className="form-card">

      <h2 className="form-title">Datos del juego</h2>



      <div className="form-section">

        <label className="form-label">Precio (USD)</label>

        <div className="price-row">

          <input

            type="number"

            className="form-input"

            value={form.price_initial}

            min={0}

            step={0.01}

            disabled={form.is_free === 1}

            onChange={e => setForm(prev => ({ ...prev, price_initial: e.target.value }))}

          />

          <label className="toggle-label">

            <input

              type="checkbox"

              checked={form.is_free === 1}

              onChange={e => handleIsFree(e.target.checked)}

            />

            <span className="toggle-text">Gratis</span>

          </label>

        </div>

      </div>



      <div className="form-section">

        <label className="form-label">Año de lanzamiento</label>

        <input

          type="number"

          className="form-input"

          value={form.release_year}

          min={2000}

          max={2030}

          onChange={e => setForm(prev => ({ ...prev, release_year: e.target.value }))}

        />

      </div>



      <div className="form-section">

        <label className="form-label">Mes de lanzamiento</label>

        <select

          className="form-input"

          value={form.release_month}

          onChange={e => setForm(prev => ({ ...prev, release_month: parseInt(e.target.value) }))}

        >

          {months.map((m, i) => (

            <option key={i + 1} value={i + 1}>{m}</option>

          ))}

        </select>

      </div>



      <div className="form-section">

        <label className="form-label">Géneros</label>

        <div className="chips-grid">

          {genres.map(g => (

            <button

              key={g.key}

              className={`chip ${form[g.key] === 1 ? 'chip-active' : ''}`}

              onClick={() => handleChip(g.key)}

              type="button"

            >

              {g.label}

            </button>

          ))}

          <button

            className={`chip ${form.genre_Free_To_Play === 1 ? 'chip-active' : ''}`}

            onClick={() => handleChip('genre_Free_To_Play')}

            type="button"

          >

            Free To Play

          </button>

        </div>

      </div>



      <div className="form-section">

        <label className="form-label">Modos de juego</label>

        <div className="chips-grid">

          {categories.map(c => (

            <button

              key={c.key}

              className={`chip ${form[c.key] === 1 ? 'chip-active' : ''}`}

              onClick={() => handleChip(c.key)}

              type="button"

            >

              {c.label}

            </button>

          ))}

        </div>

      </div>



      {error && <p className="form-error">{error}</p>}



      <button

        className="submit-btn"

        onClick={handleSubmit}

        disabled={loading}

      >

        {loading ? 'Analizando...' : 'Analizar potencial'}

      </button>

    </div>

  )

} 

