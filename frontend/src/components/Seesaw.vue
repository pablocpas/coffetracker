
<script setup>
import { computed, ref, onMounted } from 'vue'

// Propiedades que recibe este componente desde App.vue
const props = defineProps({
  state: { // 'balanced', 'left', 'right'
    type: String,
    required: true,
    default: 'balanced',
    validator: (value) => ['balanced', 'left', 'right'].includes(value)
  },
  friend1Name: {
    type: String,
    required: true
  },
  friend2Name: {
    type: String,
    required: true
  }
})

// Clase CSS dinámica basada en el estado
const seesawClass = computed(() => {
  return {
    'seesaw-plank': true,
    'state-balanced': props.state === 'balanced',
    'state-left': props.state === 'left',
    'state-right': props.state === 'right'
  }
})

// Ajuste de rotación inversa para mantener los personajes verticales
const personLeftStyle = computed(() => ({
  transform: props.state === 'right' ? 'rotate(-15deg)' : (props.state === 'left' ? 'rotate(15deg)' : 'rotate(0deg)')
}));

const personRightStyle = computed(() => ({
  transform: props.state === 'right' ? 'rotate(-15deg)' : (props.state === 'left' ? 'rotate(15deg)' : 'rotate(0deg)')
}));

// Animación de vapor para las tazas
const showSteam = ref(false);

onMounted(() => {
  // Iniciar la animación de vapor después de un breve retraso
  setTimeout(() => {
    showSteam.value = true;
  }, 500);
});

// Determinar si cada persona tiene café (el que no pagó tiene café)
const leftHasCoffee = computed(() => props.state === 'right' || props.state === 'balanced');
const rightHasCoffee = computed(() => props.state === 'left' || props.state === 'balanced');

</script>

<template>
  <div class="seesaw-container">
    <!-- Nubes de fondo decorativas -->
    <div class="cloud cloud-1"></div>
    <div class="cloud cloud-2"></div>
    
    <div :class="seesawClass">
      <!-- Personaje Izquierda (Amigo 1) -->
      <div class="person person-left" :style="personLeftStyle">
        <div class="coffee-cup" v-if="leftHasCoffee">
          <div class="steam" v-if="showSteam">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div class="head">
          <div class="eyes"></div>
          <div class="smile" :class="{ 'sad': !leftHasCoffee }"></div>
        </div>
        <div class="body"></div>
        <div class="legs"></div>
        <span class="name">{{ friend1Name }}</span>
      </div>

      <!-- Personaje Derecha (Amigo 2) -->
      <div class="person person-right" :style="personRightStyle">
        <div class="coffee-cup" v-if="rightHasCoffee">
          <div class="steam" v-if="showSteam">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
        <div class="head">
          <div class="eyes"></div>
          <div class="smile" :class="{ 'sad': !rightHasCoffee }"></div>
        </div>
        <div class="body friend2-body"></div>
        <div class="legs"></div>
        <span class="name">{{ friend2Name }}</span>
      </div>
    </div>
    
    <div class="seesaw-base">
      <div class="base-shadow"></div>
    </div>
    
    <!-- Granos de café decorativos -->
    <div class="coffee-beans">
      <div class="bean bean-1"></div>
      <div class="bean bean-2"></div>
      <div class="bean bean-3"></div>
    </div>
  </div>
</template>

<style scoped>
.seesaw-container {
  width: 100%;
  max-width: 500px;
  min-width: 280px;
  height: 220px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0;
  position: relative;
  overflow: visible;
}

/* Nubes decorativas */
.cloud {
  position: absolute;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  filter: blur(5px);
  z-index: -1;
}

.cloud-1 {
  width: 80px;
  height: 30px;
  top: 20px;
  left: 10%;
  animation: float 15s ease-in-out infinite;
}

.cloud-2 {
  width: 60px;
  height: 25px;
  top: 40px;
  right: 15%;
  animation: float 12s ease-in-out 2s infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

.seesaw-plank {
  width: 100%;
  height: 25px;
  background: linear-gradient(to bottom, var(--color-secondary), var(--color-primary));
  border-radius: 12px;
  position: relative;
  transition: transform var(--transition-slow);
  transform-origin: center bottom;
  z-index: 2;
  margin-bottom: -10px;
  box-shadow: var(--shadow-md);
  overflow: visible;
}

/* Estados de inclinación */
.state-balanced {
  transform: rotate(0deg);
}
.state-left {
  transform: rotate(-15deg);
}
.state-right {
  transform: rotate(15deg);
}

.seesaw-base {
  width: 70px;
  height: 70px;
  position: relative;
  z-index: 1;
  align-self: center;
}

.seesaw-base::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 35px solid transparent;
  border-right: 35px solid transparent;
  border-bottom: 55px solid var(--color-secondary);
}

.base-shadow {
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 70px;
  height: 10px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  filter: blur(3px);
}

/* Estilos para los personajes */
.person {
  position: absolute;
  bottom: 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: transform var(--transition-slow);
  transform-origin: bottom center;
  z-index: 3;
}

.person-left {
  left: 15%;
}
.person-right {
  right: 15%;
}

.head {
  width: 35px;
  height: 35px;
  background: #FFE0BD;
  border-radius: 50%;
  border: 2px solid rgba(0, 0, 0, 0.1);
  box-shadow: inset 0 -2px 3px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 2;
}

.eyes {
  position: absolute;
  top: 12px;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 4px;
  display: flex;
  justify-content: space-between;
}

.eyes::before, .eyes::after {
  content: '';
  width: 4px;
  height: 4px;
  background: #333;
  border-radius: 50%;
}

.smile {
  position: absolute;
  bottom: 8px;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  height: 6px;
  border-bottom: 2px solid #333;
  border-radius: 0 0 100% 100%;
}

.smile.sad {
  border-bottom: none;
  border-top: 2px solid #333;
  border-radius: 100% 100% 0 0;
  bottom: 10px;
}

.body {
  width: 30px;
  height: 45px;
  background-color: var(--color-accent);
  border-radius: 15px 15px 5px 5px;
  margin-top: -5px;
  border: 2px solid rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.friend2-body {
  background-color: var(--color-success);
}

.legs {
  width: 20px;
  height: 10px;
  margin-top: -2px;
  position: relative;
}

.legs::before, .legs::after {
  content: '';
  position: absolute;
  width: 8px;
  height: 15px;
  background-color: #333;
  border-radius: 5px;
}

.legs::before {
  left: 0;
}

.legs::after {
  right: 0;
}

.name {
  margin-top: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 3px 8px;
  border-radius: var(--border-radius-sm);
  box-shadow: var(--shadow-sm);
  white-space: nowrap;
  z-index: 4;
}

/* Taza de café */
.coffee-cup {
  position: absolute;
  top: -5px;
  right: -25px;
  width: 20px;
  height: 15px;
  background-color: white;
  border: 2px solid var(--color-primary);
  border-radius: 3px 3px 10px 10px;
  z-index: 5;
}

.coffee-cup::before {
  content: '';
  position: absolute;
  right: -8px;
  top: 2px;
  width: 8px;
  height: 8px;
  border: 2px solid var(--color-primary);
  border-radius: 50%;
  border-left: none;
}

.coffee-cup::after {
  content: '';
  position: absolute;
  left: 2px;
  top: 3px;
  width: 12px;
  height: 5px;
  background-color: var(--color-primary);
  border-radius: 2px;
}

/* Animación de vapor */
.steam {
  position: absolute;
  top: -15px;
  left: 5px;
  width: 10px;
  height: 15px;
  display: flex;
  justify-content: space-between;
}

.steam span {
  width: 2px;
  height: 0;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 50%;
  animation: steam 2s ease-out infinite;
}

.steam span:nth-child(1) {
  animation-delay: 0.2s;
}

.steam span:nth-child(2) {
  animation-delay: 0.5s;
}

.steam span:nth-child(3) {
  animation-delay: 0.8s;
}

@keyframes steam {
  0% {
    height: 0;
    opacity: 0;
  }
  30% {
    height: 10px;
    opacity: 0.7;
  }
  100% {
    height: 15px;
    opacity: 0;
    transform: translateY(-15px) scale(1.5);
  }
}

/* Granos de café decorativos */
.coffee-beans {
  position: absolute;
  bottom: 10px;
  width: 100%;
  height: 20px;
  z-index: 0;
}

.bean {
  position: absolute;
  width: 15px;
  height: 10px;
  background-color: var(--color-primary);
  border-radius: 50%;
  transform: rotate(30deg);
}

.bean::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 9px;
  height: 4px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 50%;
}

.bean-1 {
  left: 10%;
  bottom: 5px;
  transform: rotate(15deg);
}

.bean-2 {
  left: 85%;
  bottom: 8px;
  transform: rotate(-20deg);
}

.bean-3 {
  left: 50%;
  bottom: -5px;
  transform: rotate(45deg);
}
</style>
