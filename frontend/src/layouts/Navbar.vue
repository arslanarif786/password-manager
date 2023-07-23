<template>
  <div class="d-flex justify-space-between">
    <h1 v-if="$vuetify.display.sm || $vuetify.display.md || $vuetify.display.lg || $vuetify.display.xl" class="text-white mt-3 ml-7 custom-text-size font-symbol">
      Password <span class="text-deep-orange font-avenir"> Manager </span>
    </h1>
    <h1 v-else-if="$vuetify.display.xs" class="text-white mt-3 ml-7 custom-text-size font-symbol">
        PS<span class="text-deep-orange font-avenir">Manager</span>
    </h1>
    <div v-if="token" class="text-white mt-6 mr-7 d-flex">
      <span
        class="mr-6 cursor-pointer custom-primary-hover"
        @click="$router.push({ path: '/login' })"
      >
        Signin
      </span>
      <span
        class="cursor-pointer custom-primary-hover"
        @click="$router.push({ path: '/signup' })"
      >
        Signup
      </span>
    </div>
    <div v-else class="text-white mr-4 d-flex" :class="$vuetify.display.smAndUp ? 'mt-8' : 'mt-7'">
      <span
        class="mr-6 cursor-pointer custom-primary-hover"
        @click="$router.push({ path: '/dashboard' })"
      >
        Dashboard
      </span>
    </div>
  </div>
</template>

<script setup>
const token = JSON.parse(localStorage.getItem('token'))
</script>

<style scoped>
.custom-text-size {
  font-size: 2rem;
}
</style>
