<template>
  <div class="segment-selection-view">
    <SegmentSelector />
  </div>
</template>

<script setup>
  import SegmentSelector from '../components/SegmentSelector.vue';
</script>

<style scoped>
  .segment-selection-view {
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2rem 0;
  }
</style>
