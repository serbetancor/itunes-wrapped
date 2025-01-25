<script setup lang="ts">
import library from '@/../../parser/2025-01-25/Formatted_Biblioteca_byGenre_2025-01-25.json'
import type { Genre } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'
import { ref } from 'vue'

const genres = ref<Genre[]>(library.data)
</script>

<template>
  <div class="flex flex-col">
    <span v-for="(genre, index) in genres" :key="genre.id"
      >{{ index + 1 }} {{ genre.name }} {{ formatMilliseconds(genre.timePlayed) }}</span
    >
  </div>
</template>
