<template>
  <main class="modelzoo">
    <header class="header">
      <p class="eyebrow">Model Zoo</p>
      <h1>Sketch-to-prediction lab</h1>
      <p class="lede">
        Draw a digit, release your cursor, and the PyTorch model will respond
        instantly with its guess.
      </p>
    </header>

    <section class="lab">
      <div class="canvas-card">
        <div class="canvas-header">
          <div>
            <p class="tiny-label">Canvas</p>
            <h3>Draw a digit</h3>
          </div>
          <button class="pill-btn" type="button" @click="clearCanvas">
            Clear
          </button>
        </div>
        <div
          class="canvas-shell"
          ref="canvasShell"
          @pointerdown="startDrawing"
          @pointermove="drawStroke"
          @pointerup="stopDrawing"
          @pointerleave="stopDrawing"
        >
          <canvas ref="canvasEl"></canvas>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
      </div>

      <div class="predictions-card">
        <div class="canvas-header">
          <div>
            <p class="tiny-label">Model output</p>
            <h3>Top guesses</h3>
          </div>
          <span class="pill" :class="{ 'pill--busy': isLoading }">
            {{ isLoading ? "Thinking..." : "Ready" }}
          </span>
        </div>
        <div class="bars">
          <div v-for="(label, idx) in labels" :key="label" class="bar-row">
            <span class="bar-label">{{ label }}</span>
            <div class="bar-track">
              <div
                class="bar-fill"
                :style="{ width: barWidth(predictions[idx]) }"
              ></div>
            </div>
            <span class="bar-value">{{ toPct(predictions[idx]) }}</span>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";

const canvasEl = ref(null);
const canvasShell = ref(null);
const ctx = ref(null);
const drawing = ref(false);
const lastPos = ref({ x: 0, y: 0 });
const isLoading = ref(false);
const error = ref("");

const labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];
const predictions = ref(Array(10).fill(0));

const resizeCanvas = () => {
  const canvas = canvasEl.value;
  const shell = canvasShell.value;
  if (!canvas || !shell) return;
  const rect = shell.getBoundingClientRect();
  canvas.width = rect.width;
  canvas.height = rect.height;
  ctx.value = canvas.getContext("2d");
  ctx.value.lineWidth = 18;
  ctx.value.lineCap = "round";
  ctx.value.strokeStyle = "#fafafa";
};

const getPosition = (event) => {
  const canvas = canvasEl.value;
  if (!canvas) return { x: 0, y: 0 };
  const rect = canvas.getBoundingClientRect();
  const clientX = event.clientX ?? event.touches?.[0]?.clientX ?? 0;
  const clientY = event.clientY ?? event.touches?.[0]?.clientY ?? 0;
  return {
    x: clientX - rect.left,
    y: clientY - rect.top,
  };
};

const startDrawing = (event) => {
  if (!ctx.value) return;
  drawing.value = true;
  lastPos.value = getPosition(event);
};

const drawStroke = (event) => {
  if (!drawing.value || !ctx.value) return;
  const nextPos = getPosition(event);
  ctx.value.beginPath();
  ctx.value.moveTo(lastPos.value.x, lastPos.value.y);
  ctx.value.lineTo(nextPos.x, nextPos.y);
  ctx.value.stroke();
  lastPos.value = nextPos;
};

const stopDrawing = async () => {
  if (!drawing.value) return;
  drawing.value = false;
  await sendToModel();
};

const clearCanvas = () => {
  if (ctx.value && canvasEl.value) {
    ctx.value.clearRect(0, 0, canvasEl.value.width, canvasEl.value.height);
    predictions.value = Array(10).fill(0);
  }
};

const sendToModel = async () => {
  if (!canvasEl.value) return;
  isLoading.value = true;
  error.value = "";
  try {
    const dataUrl = canvasEl.value.toDataURL("image/png");
    const form = new FormData();
    form.append("image", dataUrl);
    const res = await fetch("/process_number", {
      method: "POST",
      body: form,
    });
    if (!res.ok) {
      throw new Error(`Model error (${res.status})`);
    }
    const json = await res.json();
    if (Array.isArray(json.predictions) && json.predictions.length === 10) {
      predictions.value = json.predictions;
    }
  } catch (err) {
    error.value = err?.message || "Unable to reach the model.";
  } finally {
    isLoading.value = false;
  }
};

const barWidth = (val) => `${Math.min(1, Math.max(0, val)) * 100}%`;
const toPct = (val) => `${(val * 100).toFixed(1)}%`;

onMounted(() => {
  resizeCanvas();
  window.addEventListener("resize", resizeCanvas);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeCanvas);
});
</script>

<style scoped>
.modelzoo {
  max-width: 1100px;
  margin: 0 auto;
  padding: 4rem 1.5rem 5rem;
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.8rem;
  color: var(--muted-text);
  margin-bottom: 0.8rem;
}

.header h1 {
  margin: 0 0 0.5rem;
  font-size: clamp(2.1rem, 5vw, 3rem);
}

.lede {
  color: var(--muted-text);
  line-height: 1.6;
  margin: 0;
  max-width: 720px;
}

.lab {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.canvas-card,
.predictions-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1.25rem;
  padding: 1.25rem;
}

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tiny-label {
  text-transform: uppercase;
  letter-spacing: 0.2em;
  font-size: 0.75rem;
  color: var(--muted-text);
  margin: 0 0 0.25rem;
}

.pill-btn {
  border-radius: 999px;
  padding: 0.55rem 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: transparent;
  color: var(--text-color);
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.pill-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-1px);
}

.pill {
  border-radius: 999px;
  padding: 0.4rem 0.8rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--muted-text);
  font-size: 0.9rem;
}

.pill--busy {
  border-color: var(--accent);
  color: var(--accent);
}

.canvas-shell {
  background: #05070d;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1rem;
  min-height: 340px;
  width: 100%;
  overflow: hidden;
  touch-action: none;
}

.canvas-shell canvas {
  width: 100%;
  height: 100%;
  display: block;
}

.error {
  color: #ff9494;
  margin-top: 0.75rem;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.bar-row {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 0.6rem;
}

.bar-label {
  width: 1.5rem;
  color: var(--muted-text);
}

.bar-track {
  height: 12px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 999px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.2s ease;
}

.bar-value {
  width: 3.5rem;
  color: var(--muted-text);
  text-align: right;
  font-variant-numeric: tabular-nums;
}

@media (max-width: 640px) {
  .modelzoo {
    padding: 3rem 1.25rem 4rem;
  }
}
</style>
