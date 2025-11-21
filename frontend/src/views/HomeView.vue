<template>
  <main class="home">
    <section class="hero">
      <p class="eyebrow">Personal Playground</p>
      <h1>Hi, I'm Luis — I make thoughtful ML demos & tools.</h1>
      <p class="hero__text">
        I enjoy pairing clean UX with practical models so people can feel what AI
        is capable of. My current sandbox is a digit-recognition lab that lets
        anyone sketch a number and watch a Torch model respond in real time.
      </p>
      <div class="hero__cta">
        <a
          class="btn btn--primary"
          :href="modelZooUrl"
          target="_blank"
          rel="noopener"
        >
          Launch Model Zoo
        </a>
        <button class="btn btn--ghost" type="button" @click="scrollToContact">
          Say hello
        </button>
      </div>
    </section>

    <section class="highlights">
      <article
        v-for="highlight in highlights"
        :key="highlight.title"
        :class="['highlight', { 'highlight--accent': highlight.accent }]"
      >
        <div class="highlight__heading">
          <p class="eyebrow">{{ highlight.eyebrow }}</p>
          <h3>{{ highlight.title }}</h3>
        </div>
        <p>{{ highlight.description }}</p>
        <a
          v-if="highlight.href"
          class="text-link"
          :href="highlight.href"
          target="_blank"
          rel="noopener"
        >
          {{ highlight.cta || "Learn more" }}
        </a>
      </article>
    </section>

    <section class="focus">
      <div class="section-heading">
        <p class="eyebrow">What I care about</p>
        <h2>Building with intention</h2>
        <p>
          These are the principles steering my experiments. Every prototype is a
          chance to demystify machine learning and make it feel approachable.
        </p>
      </div>
      <div class="focus__grid">
        <article v-for="item in focusAreas" :key="item.title" class="focus-card">
          <h4>{{ item.title }}</h4>
          <p>{{ item.description }}</p>
        </article>
      </div>
    </section>

    <section class="contact" id="contact">
      <div>
        <p class="eyebrow">Let's connect</p>
        <h2>Have an idea, dataset, or collaboration?</h2>
        <p>
          I'm always up for jam sessions around human-in-the-loop tools, playful
          prototypes, or anything that brings ML to life.
        </p>
      </div>
      <div class="contact__links">
        <a
          v-for="link in contactLinks"
          :key="link.label"
          class="contact__link"
          :href="link.url"
          target="_blank"
          rel="noopener"
        >
          <span>{{ link.label }}</span>
          <strong>{{ link.value }}</strong>
        </a>
      </div>
    </section>
  </main>
</template>

<script setup>
import { MODEL_ZOO_URL } from "@/constants/links";

const modelZooUrl = MODEL_ZOO_URL;

const highlights = [
  {
    eyebrow: "Latest build",
    title: "Model Zoo",
    description:
      "A Flask + Torch lab that captures your sketch strokes, normalizes them, and streams them into my MNIST classifier for instant feedback.",
    href: modelZooUrl,
    cta: "Try the demo",
    accent: true,
  },
  {
    eyebrow: "Focus",
    title: "Human-friendly ML",
    description:
      "I translate dense research into tactile tools—things people can poke, prod, and learn from in seconds.",
  },
  {
    eyebrow: "Stack",
    title: "Vue 3 + Flask",
    description:
      "Modern Vue on the front, Python/Flask APIs on the back, sprinkled with PyTorch models trained in notebooks.",
  },
];

const focusAreas = [
  {
    title: "Rapid prototyping",
    description:
      "Ship small, opinionated tools quickly so I can learn from real interactions, not assumptions.",
  },
  {
    title: "Delightful UX",
    description:
      "The interface should teach users—even if it's their first time playing with machine learning.",
  },
  {
    title: "Transparent systems",
    description:
      "I document how data flows end-to-end so collaborators can pick up my work without guesswork.",
  },
];

const contactLinks = [
  {
    label: "Email",
    value: "luis@modelzoo.dev",
    url: "mailto:luis@modelzoo.dev",
  },
  {
    label: "GitHub",
    value: "github.com/luisfcd",
    url: "https://github.com/luisfcd",
  },
  {
    label: "LinkedIn",
    value: "linkedin.com/in/luisfcd",
    url: "https://www.linkedin.com/in/luisfcd",
  },
];

const scrollToContact = () => {
  const section = document.querySelector("#contact");
  if (section) {
    section.scrollIntoView({ behavior: "smooth" });
  }
};
</script>

<style scoped>
.home {
  max-width: 1100px;
  margin: 0 auto;
  padding: 4rem 1.5rem 5rem;
  display: flex;
  flex-direction: column;
  gap: 3.5rem;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.3em;
  font-size: 0.8rem;
  color: var(--muted-text);
  margin-bottom: 0.8rem;
}

.hero h1 {
  font-size: clamp(2.4rem, 6vw, 3.9rem);
  margin: 0;
}

.hero__text {
  font-size: 1.1rem;
  line-height: 1.7;
  margin: 1.25rem 0 2rem;
  color: var(--muted-text);
}

.hero__cta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.btn {
  border-radius: 999px;
  border: 1px solid transparent;
  padding: 0.85rem 1.8rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.btn:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.btn--primary {
  background: var(--accent);
  color: #030712;
  box-shadow: 0 15px 35px rgba(93, 140, 247, 0.3);
}

.btn--ghost {
  background: transparent;
  color: var(--text-color);
  border-color: rgba(255, 255, 255, 0.2);
}

.btn:hover {
  transform: translateY(-2px);
}

.highlights {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
}

.highlight {
  background: var(--card-bg);
  padding: 1.6rem;
  border-radius: 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  min-height: 220px;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.highlight--accent {
  background: rgba(93, 140, 247, 0.15);
  border-color: rgba(93, 140, 247, 0.4);
}

.highlight h3 {
  margin: 0;
}

.text-link {
  font-weight: 600;
  color: var(--accent);
}

.focus {
  background: rgba(8, 11, 19, 0.8);
  border-radius: 1.5rem;
  padding: 2.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.focus__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.focus-card {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.focus-card h4 {
  margin: 0 0 0.5rem;
}

.focus-card p {
  color: var(--muted-text);
  margin: 0;
  line-height: 1.6;
}

.section-heading h2 {
  margin: 0;
  font-size: 2.2rem;
}

.section-heading p {
  color: var(--muted-text);
  margin: 0.4rem 0 0;
  max-width: 620px;
  line-height: 1.6;
}

.contact {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 2.5rem;
  border-radius: 1.5rem;
  background: rgba(10, 17, 33, 0.95);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.contact__links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.contact__link {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 1rem;
  padding: 1.1rem 1.3rem;
  border: 1px solid transparent;
  transition: border-color 0.2s ease, transform 0.2s ease;
}

.contact__link:hover {
  border-color: rgba(93, 140, 247, 0.8);
  transform: translateY(-2px);
}

.contact__link span {
  color: var(--muted-text);
  display: block;
  margin-bottom: 0.2rem;
}

.contact__link strong {
  font-size: 1.05rem;
}

@media (max-width: 640px) {
  .home {
    padding: 3rem 1.25rem 4rem;
  }

  .focus,
  .contact {
    padding: 2rem 1.5rem;
  }
}
</style>
