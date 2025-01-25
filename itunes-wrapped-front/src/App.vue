<script setup lang="ts">
import { getRouter } from '@/router'

const topics = ['songs', 'albums', 'artists', 'genres']
</script>

<template>
  <div class="h-full w-full bg-white">
    <div class="mt-12 flex h-fit w-full justify-center gap-4">
      <button
        v-for="topic in topics"
        :key="topic"
        class="text-gray border-b border-blue p-2 text-lg transition-all duration-300 ease-in-out hover:scale-110 hover:text-blue"
        @click="getRouter().push({ name: topic })"
      >
        <span>{{ topic }}</span>
      </button>
    </div>
    <router-view />
  </div>
</template>
