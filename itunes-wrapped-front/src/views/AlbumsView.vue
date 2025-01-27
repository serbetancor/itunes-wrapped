<script setup lang="ts">
import library from '@/../../parser/current/Formatted_Biblioteca_byalbum.json'
import { ref } from 'vue'

import type { Album } from '@/models/itunes'

import ArrowIcon from '@/assets/arrow.svg'
import { formatMilliseconds } from '@/utils/itunes'

const albums = ref<Album[]>(library.data)
const topCount = ref<number>(5)
</script>

<template>
  <div class="flex flex-col items-center p-4">
    <input type="range" v-model="topCount" min="1" max="30" class="mb-4 w-64" />
    <span>Top {{ topCount }} album{{ topCount > 1 ? 's' : '' }}</span>

    <div class="w-2/5 px-4">
      <h3 class="mb-2 text-lg font-bold">Ranking</h3>
      <ul class="divide-y">
        <li
          v-for="(album, index) in albums.slice(0, topCount)"
          :key="album.id"
          class="grid grid-cols-[auto_1fr_auto_auto] items-center gap-2 p-2 py-1 odd:bg-pink/10 even:bg-white"
        >
          <span class="font-semibold">#{{ index + 1 }}</span>
          <span>{{ album.name }}</span>
          <span>{{ formatMilliseconds(album.timePlayed) }}</span>
          <div
            class="flex items-center"
            :class="{
              'text-red': album.positionsGained < 0,
              'text-green': album.positionsGained > 0,
            }"
          >
            <span v-if="album.positionsGained === 0" class="w-4 text-center">-</span>
            <ArrowIcon v-else class="w-4" :class="{ 'rotate-180': album.positionsGained < 0 }" />
            <span class="w-5 text-right">{{ album.positionsGained }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
