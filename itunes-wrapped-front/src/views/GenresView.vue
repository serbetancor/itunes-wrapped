<script setup lang="ts">
import library from '@/../../parser/current/Formatted_Biblioteca_byGenre.json'
import type { Genre } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'
import { ref } from 'vue'

const genres = ref<Genre[]>(library.data)
const topCount = ref<number>(5)
</script>

<template>
  <div class="flex flex-col items-center p-4">
    <input type="range" v-model="topCount" min="1" max="10" class="mb-4 w-64" />
    <span>Top {{ topCount }} genre{{ topCount > 1 ? 's' : '' }}</span>

    <div class="w-2/5 px-4">
      <h3 class="mb-2 text-lg font-bold">Ranking</h3>
      <ul class="divide-y">
        <li
          v-for="(genre, index) in genres.slice(0, topCount)"
          :key="genre.id"
          class="grid grid-cols-[auto_1fr_auto] gap-2 p-2 py-1 odd:bg-purple/10 even:bg-white"
        >
          <span class="font-semibold">#{{ index + 1 }}</span>
          <span>{{ genre.name }}</span>
          <span>{{ formatMilliseconds(genre.timePlayed) }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>
