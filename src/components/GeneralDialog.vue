<template>
  <div class="component-root">
    <button type="button" id="display-modal-btn" class="btn btn-primary" data-toggle="modal" data-target="#modal-wrapper" style="display: none;"></button>
    <div class="modal fade" id="modal-wrapper" tabindex="-1" aria-labelledby="modal-label" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title" id="modal-label">Modal title</h4>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default  {
  name: 'GeneralDialog'
};
</script>

<style scoped>
</style>