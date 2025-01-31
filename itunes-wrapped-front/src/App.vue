<script setup lang="ts">
import { getRouter } from '@/router'

const topics = ['songs', 'albums', 'artists', 'genres']
</script>

<template>
  <div class="flex min-h-screen w-full flex-col bg-zinc-700 text-white">
    <div class="mt-12 flex h-fit w-full justify-center gap-4">
      <button
        v-for="topic in topics"
        :key="topic"
        class="text-gray border-blue hover:text-blue border-b p-2 text-lg transition-all duration-300 ease-in-out hover:scale-110 hover:cursor-pointer"
        @click="getRouter().push({ name: topic })"
      >
        <span>{{ topic }}</span>
      </button>
    </div>
    <router-view />
  </div>
</template>
