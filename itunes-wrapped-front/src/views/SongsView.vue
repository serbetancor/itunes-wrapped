<script setup lang="ts">
import library from '@/../../parser/2025-01-25/Formatted_Biblioteca_byTimePlayed_2025-01-25.json'
import type { Song } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'
import { ref } from 'vue'

const songs = ref<Song[]>(library.data)
</script>

<template>
  <div class="flex flex-col">
    <span v-for="(song, index) in songs" :key="song.id"
      >{{ index + 1 }} {{ song.name }} {{ formatMilliseconds(song.timePlayed) }}</span
    >
  </div>
</template>
