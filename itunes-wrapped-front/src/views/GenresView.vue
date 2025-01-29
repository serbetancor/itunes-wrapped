<script setup lang="ts">
import library from '@/../../parser/current/Formatted_Biblioteca_byGenre.json'
import { ref, computed } from 'vue'

import type { Genre } from '@/models/itunes'

import ArrowIcon from '@/assets/arrow.svg'
import { formatMilliseconds } from '@/utils/itunes'

const genres = ref<Genre[]>(library.data)
const topCount = ref<number>(15)

const shownGenres = computed(() => genres.value.slice(0, topCount.value))
</script>

<template>
  <div class="flex flex-col items-center p-4">
    <input type="range" v-model="topCount" min="1" max="15" class="mb-4 w-64" />
    <span>Top {{ topCount }} genre{{ topCount > 1 ? 's' : '' }}</span>

    <div class="w-1/2 px-4">
      <h3 class="mb-2 text-lg font-bold">Ranking</h3>
      <ul class="divide-y">
        <li
          v-for="(genre, index) in shownGenres"
          :key="genre.id"
          class="grid grid-cols-[auto_1fr_auto_auto] gap-2 p-2 py-1 odd:bg-purple/10 even:bg-white"
        >
          <span class="font-semibold">{{ index + 1 }}</span>
          <span>{{ genre.name }}</span>
          <span>{{ formatMilliseconds(genre.timePlayed) }}</span>
          <div
            class="flex items-center"
            :class="{
              'text-red': genre.positionsGained < 0,
              'text-green': genre.positionsGained > 0,
            }"
          >
            <span v-if="genre.positionsGained === 0" class="w-4 text-center">-</span>
            <ArrowIcon v-else class="w-4" :class="{ 'rotate-180': genre.positionsGained < 0 }" />
            <span class="w-5 text-right">{{ genre.positionsGained }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
