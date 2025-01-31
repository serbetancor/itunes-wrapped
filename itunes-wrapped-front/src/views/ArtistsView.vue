<script setup lang="ts">
import library from '@/../../parser/data/current/Formatted_Biblioteca_byArtist.json'
import { ref, computed } from 'vue'

import type { Artist } from '@/models/itunes'

import ArrowIcon from '@/assets/arrow.svg'
import HyphenIcon from '@/assets/hyphen.svg'
import NoImageIcon from '@/assets/no-image.svg'
import TopArtistCard from '@/components/TopArtistCard.vue'
import { formatMilliseconds } from '@/utils/itunes'

const artists = ref<Artist[]>(library.data)
const topCount = ref<number>(20)

const shownArtists = computed(() => artists.value.slice(0, topCount.value))
</script>

<template>
  <div class="flex flex-col items-center gap-4 p-4">
    <input type="range" v-model="topCount" min="1" max="400" class="mb w-64" />
    <span>Top {{ topCount }} artist{{ topCount > 1 ? 's' : '' }}</span>

    <div class="flex w-10/12 flex-col gap-4 px-4">
      <div class="flex gap-2">
        <TopArtistCard
          v-for="(artist, index) in shownArtists.slice(0, 5)"
          :key="artist.id"
          :artist
          :index
        />
      </div>

      <ul class="divide-y">
        <li
          v-for="(artist, index) in shownArtists.slice(5)"
          :key="artist.id"
          class="odd:bg-pink/10 grid min-h-12 grid-cols-[auto_auto_1fr_auto_auto] items-center gap-3 p-2 py-1"
        >
          <span class="w-4 font-semibold">{{ index + 6 }}</span>
          <img v-if="artist.image" class="w-10 rounded-full" :src="artist.image" />
          <NoImageIcon v-else class="w-10 rounded-full border p-2" />
          <span>{{ artist.name }}</span>
          <span>{{ formatMilliseconds(artist.timePlayed) }}</span>
          <div
            class="flex items-center"
            :class="{
              'text-red': artist.positionsGained < 0,
              'text-green': artist.positionsGained > 0,
            }"
          >
            <HyphenIcon v-if="artist.positionsGained === 0" class="w-4" />
            <ArrowIcon v-else class="w-4" :class="{ 'rotate-180': artist.positionsGained < 0 }" />
            <span class="w-5 text-right">{{ artist.positionsGained }}</span>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
