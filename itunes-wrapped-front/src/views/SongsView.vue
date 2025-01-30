<script setup lang="ts">
import library from '@/../../parser/data/current/Formatted_Biblioteca.json'
import { ref, computed } from 'vue'

import type { Song } from '@/models/itunes'

import ArrowIcon from '@/assets/arrow.svg'
import NoImageIcon from '@/assets/no-image.svg'
import { formatMilliseconds } from '@/utils/itunes'

const songs = ref<Song[]>(library.data)
const topCount = ref<number>(20)

const shownSongs = computed(() => songs.value.slice(0, topCount.value))

/*
const tooltip = ref<{ x: number; y: number; text: string; visible: boolean }>({
  text: '',
  visible: false,
  x: 0,
  y: 0,
})

const maxTimePlayed = computed(() => Math.max(...songs.value.map((s) => s.timePlayed)))


const circles = computed(() => {
  const maxRadius = 350 / Math.sqrt(topCount.value)
  return songs.value.slice(0, topCount.value).map((song, index) => {
    const radius = Math.sqrt(song.timePlayed / maxTimePlayed.value) * maxRadius
    const angle = (index / topCount.value) * Math.PI * 2
    const x = 375 + Math.cos(angle) * (350 - radius)
    const y = 375 + Math.sin(angle) * (350 - radius)

    const colors = ['fill-blue', 'fill-pink', 'fill-purple']
    const randomColor = colors[Math.floor(Math.random() * colors.length)]

    return {
      color: randomColor,
      id: song.id,
      name: song.name,
      radius,
      timePlayed: song.timePlayed,
      x,
      y,
    }
  })
})


const showTooltip = (event: MouseEvent, text: string) => {
  const container = (event.currentTarget as SVGElement).closest('div.relative') as HTMLDivElement
  if (container) {
    const rect = container.getBoundingClientRect()
    tooltip.value = {
      text,
      visible: true,
      x: event.clientX - rect.left + 5,
      y: event.clientY - rect.top - 35,
    }
  }
}

const hideTooltip = () => {
  tooltip.value.visible = false
}
*/
</script>

<template>
  <div class="flex flex-col items-center p-4">
    <input type="range" v-model="topCount" min="1" max="100" class="mb-4 w-64" />
    <span>Top {{ topCount }} song{{ topCount > 1 ? 's' : '' }}</span>
    <!--

    <div class="relative mt-4 flex w-3/4 justify-between">
      <svg viewBox="0 0 750 750" class="h-full w-1/2 rounded-lg border border-gray-300">
        <circle
          v-for="circle in circles"
          :key="circle.id"
          :cx="circle.x"
          :cy="circle.y"
          :r="circle.radius"
          :class="`${circle.color} opacity-80 transition-opacity hover:opacity-100`"
          @mousemove="(e) => showTooltip(e, circle.name)"
          @mouseleave="hideTooltip"
        />
      </svg>
      <div
        v-if="tooltip.visible"
        class="absolute rounded bg-black px-2 py-1 text-sm text-white shadow-lg"
        :style="{ top: `${tooltip.y}px`, left: `${tooltip.x}px` }"
      >
        {{ tooltip.text }}
      </div>
    -->

    <div class="w-1/2 px-4">
      <h3 class="mb-2 text-lg font-bold">Ranking</h3>

      <ul class="divide-y">
        <li
          v-for="(song, index) in shownSongs"
          :key="song.id"
          class="grid grid-cols-[auto_auto_1fr_auto_auto] items-center gap-3 p-2 py-1 odd:bg-pink/10 even:bg-white"
        >
          <span class="w-4 font-semibold">{{ index + 1 }}</span>
          <img v-if="song.image" class="w-10 rounded-full" :src="song.image" />
          <NoImageIcon v-else class="w-10 rounded-full border p-2" /> <span>{{ song.name }}</span>
          <span>{{ formatMilliseconds(song.timePlayed) }}</span>
          <div
            class="flex items-center"
            :class="{
              'text-red': song.positionsGained < 0,
              'text-green': song.positionsGained > 0,
            }"
          >
            <span v-if="song.positionsGained === 0" class="w-4 text-center">-</span>
            <ArrowIcon v-else class="w-4" :class="{ 'rotate-180': song.positionsGained < 0 }" />
            <span class="w-5 text-right">{{ song.positionsGained }}</span>
          </div>
        </li>
      </ul>
    </div>
    <!--
    </div>
    -->
  </div>
</template>
