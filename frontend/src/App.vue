<template>
  <div id="app">
    <header class="site-nav">
      <router-link class="site-nav__brand" to="/">
        Luis F. Chumpitaz Diaz
      </router-link>
      <div class="site-nav__links">
        <router-link class="site-nav__link" to="/">Home</router-link>
        <a
          class="site-nav__link site-nav__link--external"
          :href="MODEL_ZOO_URL"
          target="_blank"
          rel="noopener"
        >
          Model Zoo ↗
        </a>
      </div>
    </header>
    <router-view />
  </div>
</template>

<script setup>
import { MODEL_ZOO_URL } from "@/constants/links";
</script>

<style>
:root {
  --page-bg: linear-gradient(180deg, #050505, #11121f 60%, #0b101a);
  --card-bg: rgba(10, 17, 30, 0.85);
  --text-color: #f8fbff;
  --muted-text: #adbbd9;
  --accent: #5d8cf7;
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: var(--page-bg);
  color: var(--text-color);
}

#app {
  min-height: 100vh;
}

.site-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  position: sticky;
  top: 0;
  background: rgba(5, 6, 10, 0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  z-index: 10;
}

.site-nav__brand {
  font-weight: 700;
  font-size: 1.1rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
}

.site-nav__links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.site-nav__link {
  font-weight: 600;
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  color: var(--muted-text);
  transition: color 0.2s ease, background 0.2s ease;
}

.site-nav__link.router-link-active {
  color: var(--text-color);
}

.site-nav__link--external {
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.site-nav__link:hover {
  color: var(--text-color);
  background: rgba(93, 140, 247, 0.15);
}

a {
  color: inherit;
}

a:hover {
  color: var(--accent);
}

@media (max-width: 640px) {
  .site-nav {
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem 1.25rem;
  }
}
</style>
