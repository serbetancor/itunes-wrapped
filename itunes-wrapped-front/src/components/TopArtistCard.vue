<script setup lang="ts">
import type { Artist } from '@/models/itunes'
import type { PropType } from 'vue'

import ArrowIcon from '@/assets/arrow.svg'
import HyphenIcon from '@/assets/hyphen.svg'
import NoImageIcon from '@/assets/no-image.svg'
import { formatMilliseconds } from '@/utils/itunes'

defineProps({
  artist: { required: true, type: Object as PropType<Artist> },
  index: { required: true, type: Number },
})
</script>

<template>
  <div class="flex h-96 w-1/5 flex-col items-center rounded-xl p-2 drop-shadow-xl">
    <span>{{ index + 1 }}</span>
    <img v-if="artist.image" class="w-32 rounded-full" :src="artist.image" />
    <NoImageIcon v-else class="w-32 rounded-full border p-2" />
    <span class="text-center font-bold">{{ artist.name }}</span>

    <div class="flex w-full justify-center gap-2">
      <span>{{ formatMilliseconds(artist.timePlayed) }}</span>
      <HyphenIcon v-if="artist.positionsGained === 0" class="w-4 text-center" />
      <ArrowIcon v-else class="w-4" :class="{ 'rotate-180': artist.positionsGained < 0 }" />
      <span class="text-right">{{ artist.positionsGained }}</span>
    </div>

    <div class="my-auto grid w-full grid-cols-2 place-items-center gap-y-2">
      <div
        v-for="song in artist.songs.slice(0, 4)"
        :key="song.id"
        class="flex w-5/6 cursor-pointer justify-center gap-2 rounded-2xl border border-gray-400 p-1 transition-shadow duration-300 hover:shadow-lg hover:shadow-gray-400"
      >
        <div class="flex flex-col items-center">
          <img v-if="song.image" class="h-6 w-6 rounded-full" :src="song.image" />
          <NoImageIcon v-else class="h-6 w-6 rounded-full border p-1" />
          <div
            class="flex gap-1"
            :class="{
              'text-red': song.positionsGained < 0,
              'text-green': song.positionsGained > 0,
            }"
          >
            <HyphenIcon v-if="song.positionsGained === 0" class="h-3 w-3 self-center" />
            <ArrowIcon
              v-else
              class="h-3 w-3 self-center"
              :class="{ 'rotate-180': song.positionsGained < 0 }"
            />
            <span class="self-center text-[10px]">{{ song.positionsGained }}</span>
          </div>
        </div>
        <span class="line-clamp-3 w-1/2 text-xs">{{ song.name }}</span>
      </div>
    </div>
  </div>
</template>
