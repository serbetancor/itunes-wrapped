<script setup lang="ts">
import library from '@/../../parser/2025-01-25/Formatted_Biblioteca_byalbum_2025-01-25.json'
import type { Album } from '@/models/itunes'
import { formatMilliseconds } from '@/utils/itunes'
import { ref } from 'vue'

const albums = ref<Album[]>(library.data)
</script>

<template>
  <div class="flex flex-col">
    <span v-for="(album, index) in albums" :key="album.id"
      >{{ index + 1 }} {{ album.name }} {{ formatMilliseconds(album.timePlayed) }}</span
    >
  </div>
</template>
