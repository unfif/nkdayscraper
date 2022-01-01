<template>
  <button type="button" id="display-modal-btn" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#modal-wrapper" style="display: none;"></button>
  <div class="modal fade" id="modal-wrapper" tabindex="-1" aria-labelledby="modal-title" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h4 class="modal-title" id="modal-title">Modal title</h4>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import '@popperjs/core'
import 'bootstrap'
</script>

<style scoped>
</style>
