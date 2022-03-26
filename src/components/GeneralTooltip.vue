<template>
    <div class="popper-tooltip" role="tooltip" ref="ref_tooltip">
      {{ data.tooltip }}
      <div class="popper-arrow" data-popper-arrow></div>
    </div>
</template>

<script setup>
import { ref, reactive, onUpdated, computed } from 'vue'
import { createPopper } from "@popperjs/core"

const props = defineProps({
  target: {
    default: ref(null)
  },
  placement: {
    type: String,
    default: 'bottom'
  },
  callback: {
    type: Function,
    default: null
  },
  callbackParam: {
    default: null
  }
})

const ref_tooltip = ref(null);

const data = reactive({
  tooltip: ''
})

const targetEl = computed(() => {
  return props.target;
})

const showEvents = ['mouseenter', 'focus'];
const hideEvents = ['mouseleave', 'blur'];

onUpdated(() => {
  const target = targetEl.value;
  const tooltip = ref_tooltip.value;

  const popperInstance = createPopper(target, tooltip, {
    placement: props.placement,
    modifiers: [
      {
        name: 'offset',
        options: {
          offset: [0, 8],
        },
      },
    ],
  })

  const show = async () => {
    if(!data.tooltip){
      data.tooltip = await props.callback(props.callbackParam);
    }
    tooltip.setAttribute('data-show', '');
    popperInstance.setOptions({
      modifiers: [{ name: 'eventListeners', enabled: true }],
    })
    popperInstance.update();
    setTimeout(hide, 2000);
  }

  const hide = () => {
    tooltip.removeAttribute('data-show');
    popperInstance.setOptions({
      modifiers: [{ name: 'eventListeners', enabled: false }],
    })
  }

  showEvents.forEach(event => {
    target.addEventListener(event, show);
  })

  hideEvents.forEach(event => {
    target.addEventListener(event, hide);
  })
})
</script>

<style scoped>
.popper-tooltip {
  background: #333;
  color: white;
  font-weight: bold;
  padding: 4px 8px;
  font-size: 13px;
  border-radius: 4px;
  display: none;
}

.popper-tooltip[data-show] {
  display: block;
}

.popper-arrow,
.popper-arrow::before {
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
}

.popper-arrow {
  visibility: hidden;
}

.popper-arrow::before {
  visibility: visible;
  content: '';
  transform: rotate(45deg);
}

.popper-tooltip[data-popper-placement^='top'] > .popper-arrow {
  bottom: -4px;
}

.popper-tooltip[data-popper-placement^='bottom'] > .popper-arrow {
  top: -4px;
}

.popper-tooltip[data-popper-placement^='left'] > .popper-arrow {
  right: -4px;
}

.popper-tooltip[data-popper-placement^='right'] > .popper-arrow {
  left: -4px;
}
</style>
