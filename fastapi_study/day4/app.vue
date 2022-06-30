<script setup lang="ts">
const { data: r } = useAsyncData('index', () => useApi())
</script>
<template>
  <div>
    <h1>Hello</h1>
    <p>{{ r.greeting }}</p>
  </div>
</template>
