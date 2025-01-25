<script setup lang="ts">
import library from '@/../../parser/2025-01-25/Formatted_Biblioteca_byArtist_2025-01-25.json'
import type { Artist } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'
import { ref } from 'vue'

const artists = ref<Artist[]>(library.data)
</script>

<template>
  <div class="flex flex-col">
    <span v-for="(artist, index) in artists" :key="artist.id"
      >{{ index + 1 }} {{ artist.name }} {{ formatMilliseconds(artist.timePlayed) }}</span
    >
  </div>
</template>
