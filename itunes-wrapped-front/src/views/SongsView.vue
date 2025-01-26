<script setup lang="ts">
import { ref, computed } from 'vue'
import library from '@/../../parser/current/Formatted_Biblioteca_byTimePlayed.json'
import type { Song } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'

const songs = ref<Song[]>(library.data)
const topCount = ref<number>(5)
const tooltip = ref<{ x: number; y: number; text: string; visible: boolean }>({
  x: 0,
  y: 0,
  text: '',
  visible: false,
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

    console.log(index, song, song.timePlayed)

    return {
      id: song.id,
      name: song.name,
      radius,
      x,
      y,
      timePlayed: song.timePlayed,
      color: randomColor,
    }
  })
})

const showTooltip = (event: MouseEvent, text: string) => {
  const container = (event.currentTarget as SVGElement).closest('div.relative') as HTMLDivElement
  if (container) {
    const rect = container.getBoundingClientRect()
    tooltip.value = {
      x: event.clientX - rect.left + 5,
      y: event.clientY - rect.top - 35,
      text,
      visible: true,
    }
  }
}

const hideTooltip = () => {
  tooltip.value.visible = false
}
</script>

<template>
  <div class="flex flex-col items-center p-4">
    <input type="range" v-model="topCount" min="1" max="10" class="mb-4 w-64" />
    <span>Top {{ topCount }} song{{ topCount > 1 ? 's' : '' }}</span>

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

      <div class="w-2/5 px-4">
        <h3 class="mb-2 text-lg font-bold">Ranking</h3>

        <ul class="divide-y">
          <li
            v-for="(song, index) in songs.slice(0, topCount)"
            :key="song.id"
            class="grid grid-cols-[auto_1fr_auto] gap-2 p-2 py-1 odd:bg-blue/10 even:bg-white"
          >
            <span class="font-semibold">#{{ index + 1 }}</span>
            <span>{{ song.name }}</span>
            <span>{{ formatMilliseconds(song.timePlayed) }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
