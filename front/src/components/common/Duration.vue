<template>
  <span>
    <translate translate-context="Content/*/Paragraph"
      v-if="durationData.hours > 0"
      :translate-params="{minutes: durationData.minutes, hours: durationData.hours}">%{ hours } h %{ minutes } min</translate>
    <translate translate-context="Content/*/Paragraph"
      v-else
      :translate-params="{minutes: durationData.minutes}">%{ minutes } min</translate>
  </span>
</template>
<script>
import {secondsToObject} from '@/filters'

export default {
  props: ['seconds'],
  computed: {
    durationData () {
      return secondsToObject(this.seconds)
    }
  }
}
</script>
