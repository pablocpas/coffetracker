
<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import Seesaw from './components/Seesaw.vue'

// --- Estado Reactivo ---
const lastPayer = ref(null) // Quién pagó último ('YOUR_NAME', 'FRIEND_NAME', null)
const isLoading = ref(true)
const errorMsg = ref('')
const showConfetti = ref(false)
const coffeeCount = ref(0)

// --- Nombres (¡¡IMPORTANTE!! Edita estos valores) ---
// Deben coincidir exactamente con los del backend (app.py)
const friend1 = "CAÑO"  // <-- CAMBIA ESTO
const friend2 = "BARRIO" // <-- CAMBIA ESTO

// --- URL de la API (ajusta si es necesario) ---
const apiUrl = 'http://localhost:5000/api' // O la IP/dominio de tu backend

// --- Lógica ---
// Función para obtener el último pagador al cargar
const fetchLastPayer = async () => {
  isLoading.value = true
  errorMsg.value = ''
  try {
    // Añadimos un timestamp para evitar caché en algunas configuraciones
    const response = await axios.get(`${apiUrl}/last_payer?t=${Date.now()}`)
    lastPayer.value = response.data.last_payer
    
    // Incrementar contador de café para animación
    coffeeCount.value += 1
    
    console.log("Último pagador recibido:", lastPayer.value)
  } catch (error) {
    console.error("Error al obtener el último pagador:", error.response?.data || error.message)
    errorMsg.value = `Error al conectar con el servidor (${apiUrl}). ¿Está el backend funcionando?`
  } finally {
    isLoading.value = false
  }
}

// Función para registrar un pago
const pay = async (payerName) => {
  isLoading.value = true // Mostrar feedback mientras se procesa
  errorMsg.value = ''
  try {
    const response = await axios.post(`${apiUrl}/pay`, { payer_name: payerName })
    if (response.data.success) {
        lastPayer.value = payerName // Actualiza el estado local inmediatamente
        console.log("Pago registrado por:", payerName)
        
        // Mostrar confeti al registrar un pago exitoso
        showConfetti.value = true
        setTimeout(() => {
          showConfetti.value = false
        }, 3000)
        
        // Incrementar contador de café
        coffeeCount.value += 1
    } else {
        // Esto no debería ocurrir si el backend devuelve un error HTTP, pero por si acaso
        errorMsg.value = response.data.error || 'Error desconocido al registrar el pago.'
    }
  } catch (error) {
    console.error("Error al registrar el pago:", error.response?.data || error.message)
    errorMsg.value = `Error al registrar el pago: ${error.response?.data?.error || error.message}`
  } finally {
    isLoading.value = false
  }
}

// --- Ciclo de vida ---
onMounted(() => {
  fetchLastPayer() // Llama a la API cuando el componente se monta
})

// --- Propiedades Computadas (para el balancín) ---
const seesawState = computed(() => {
  if (!lastPayer.value) {
    return 'balanced' // Estado inicial o sin pagos
  } else if (lastPayer.value === friend1) {
    return 'left' // Inclinado hacia la izquierda (Amigo 1)
  } else if (lastPayer.value === friend2) {
    return 'right' // Inclinado hacia la derecha (Amigo 2)
  } else {
    return 'balanced'; // Estado por defecto si el nombre no coincide (puede indicar error)
  }
})

// Mensaje de estado con emojis
const statusMessage = computed(() => {
  if (!lastPayer.value && !isLoading.value && !errorMsg.value) {
    return '¡Nadie ha pagado todavía! ¿A quién le toca el honor? ☕'
  } else if (lastPayer.value && !isLoading.value) {
    return `¡El último café lo pagó ${lastPayer.value}! 🎉`
  }
  return ''
})

// Generar confeti
const generateConfetti = () => {
  const confettiElements = []
  const colors = ['#e76f51', '#2a9d8f', '#e9c46a', '#264653', '#f4a261']
  
  for (let i = 0; i < 50; i++) {
    const left = Math.random() * 100
    const width = Math.random() * 10 + 5
    const height = Math.random() * 10 + 5
    const bg = colors[Math.floor(Math.random() * colors.length)]
    const delay = Math.random() * 3
    
    confettiElements.push({
      left: `${left}%`,
      width: `${width}px`,
      height: `${height}px`,
      background: bg,
      delay: `${delay}s`
    })
  }
  
  return confettiElements
}

const confetti = ref(generateConfetti())

// Regenerar confeti cada vez que se muestra
watch(showConfetti, (newVal) => {
  if (newVal) {
    confetti.value = generateConfetti()
  }
})
</script>

<template>
  <div class="coffee-tracker">
    <!-- Confeti -->
    <div v-if="showConfetti" class="confetti-container">
      <div 
        v-for="(c, index) in confetti" 
        :key="index" 
        class="confetti"
        :style="{
          left: c.left,
          width: c.width,
          height: c.height,
          background: c.background,
          animationDelay: c.delay
        }"
      ></div>
    </div>
    
    <!-- Decoración de granos de café -->
    <div class="coffee-decoration">
      <div class="coffee-bean bean-1"></div>
      <div class="coffee-bean bean-2"></div>
      <div class="coffee-bean bean-3"></div>
    </div>
    
    <div class="header">
      <h1>☕ ¿Quién pagó el último café? ☕</h1>
      <div class="coffee-counter">
        <span class="coffee-icon">☕</span>
        <span class="count">{{ coffeeCount }}</span>
      </div>
    </div>

    <div v-if="isLoading && !lastPayer" class="loading">
      <div class="loading-spinner"></div>
      <p>Consultando el oráculo cafetero...</p>
    </div>
    
    <div v-if="errorMsg" class="error">
      <p><strong>¡Ups! Algo fue mal:</strong></p>
      <p>{{ errorMsg }}</p>
    </div>

    <div v-show="!isLoading || lastPayer" class="content animate-fadeIn">
      <!-- Pasa el estado calculado al componente del balancín -->
      <Seesaw :state="seesawState" :friend1Name="friend1" :friend2Name="friend2" />

      <div class="buttons">
        <button 
          @click="pay(friend1)" 
          :disabled="isLoading"
          class="button button-primary"
        >
          <span class="button-icon">☕</span>
          <span>Pagó {{ friend1 }}</span>
        </button>
        
        <button 
          @click="pay(friend2)" 
          :disabled="isLoading"
          class="button button-secondary"
        >
          <span class="button-icon">☕</span>
          <span>Pagó {{ friend2 }}</span>
        </button>
      </div>

      <div class="status-container">
        <p v-if="statusMessage" class="status-message animate-slideUp">
          {{ statusMessage }}
        </p>
        <p v-if="isLoading && lastPayer" class="status-message loading">
          <span class="loading-dots">Actualizando quién pagó</span>
        </p>
      </div>
    </div>
    
    <footer class="footer">
      <p>CoffeeTracker v2.0 - Mantén la cuenta de quién invita al café</p>
    </footer>
  </div>
</template>

<style scoped>
.coffee-tracker {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2.5rem;
  max-width: 700px;
  margin: 2rem auto;
  background-color: var(--color-background);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-lg);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.header {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}

h1 {
  color: var(--color-primary);
  margin-bottom: 1rem;
  font-weight: 700;
  font-size: 2rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
}

.coffee-counter {
  display: flex;
  align-items: center;
  background-color: var(--color-secondary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.coffee-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.count {
  font-size: 1.1rem;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  background-color: rgba(255, 255, 255, 0.8);
  box-shadow: var(--shadow-sm);
  font-weight: 500;
  color: var(--color-text);
  width: 100%;
  max-width: 400px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  margin: 2rem 0;
  padding: 1.5rem;
  border-radius: var(--border-radius-md);
  color: var(--color-danger);
  background-color: rgba(230, 57, 70, 0.1);
  border: 1px solid rgba(230, 57, 70, 0.3);
  width: 100%;
  max-width: 400px;
}

.error p {
  margin-bottom: 0.5rem;
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-top: 1rem;
}

.buttons {
  margin-top: 2.5rem;
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  justify-content: center;
}

.button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--border-radius-md);
  color: white;
  transition: all var(--transition-normal);
  box-shadow: var(--shadow-md);
  min-width: 180px;
}

.button-icon {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

.button-primary {
  background-color: var(--color-primary);
}

.button-primary:hover {
  background-color: #5a3530;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.button-secondary {
  background-color: var(--color-accent);
}

.button-secondary:hover {
  background-color: #d05a3e;
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.button:disabled {
  background-color: var(--color-text-light);
  cursor: not-allowed;
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

.status-container {
  margin-top: 2rem;
  min-height: 3rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.status-message {
  font-size: 1.2rem;
  color: var(--color-text);
  font-weight: 500;
  background-color: rgba(255, 255, 255, 0.7);
  padding: 0.8rem 1.5rem;
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
}

.status-message.loading {
  font-style: italic;
  color: var(--color-text-light);
}

.loading-dots::after {
  content: '...';
  animation: dots 1.5s infinite;
}

@keyframes dots {
  0%, 20% { content: '.'; }
  40% { content: '..'; }
  60%, 100% { content: '...'; }
}

.footer {
  margin-top: 3rem;
  font-size: 0.9rem;
  color: var(--color-text-light);
  width: 100%;
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

/* Decoración de granos de café */
.coffee-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.coffee-bean {
  position: absolute;
  width: 30px;
  height: 20px;
  background-color: var(--color-primary);
  border-radius: 50%;
  opacity: 0.1;
}

.coffee-bean::after {
  content: '';
  position: absolute;
  top: 6px;
  left: 6px;
  width: 18px;
  height: 8px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
}

.bean-1 {
  top: 15%;
  left: 10%;
  transform: rotate(30deg);
}

.bean-2 {
  top: 20%;
  right: 15%;
  transform: rotate(-20deg);
}

.bean-3 {
  bottom: 15%;
  left: 20%;
  transform: rotate(45deg);
}

/* Confeti */
.confetti-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
  z-index: 10;
}

.confetti {
  position: absolute;
  top: -20px;
  animation: confetti-fall 3s ease-in forwards;
}

@keyframes confetti-fall {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(720deg);
    opacity: 0;
  }
}

/* Responsive */
@media (max-width: 600px) {
  .coffee-tracker {
    padding: 1.5rem;
    margin: 1rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
  
  .buttons {
    flex-direction: column;
    gap: 1rem;
  }
  
  .button {
    width: 100%;
  }
}
</style>
