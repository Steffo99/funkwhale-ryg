<template>
  <main class="main pusher" v-title="labels.title">
    <div class="ui vertical stripe segment">
      <section class="ui text container">
        <div v-if="isLoading" class="ui inverted active dimmer">
          <div class="ui loader"></div>
        </div>
        <template v-else>
          <router-link :to="{name: 'settings'}">
            <translate translate-context="Content/Applications/Link">Back to settings</translate>
          </router-link>
          <h2 class="ui header">
            <translate translate-context="Content/Applications/Title">Application details</translate>
          </h2>
          <div class="ui form">
            <p>
              <translate translate-context="Content/Application/Paragraph/">
                Application ID and secret are really sensitive values and must be treated like passwords. Do not share those with anyone else.
              </translate>
            </p>
            <div class="field">
              <label><translate translate-context="Content/Applications/Label">Application ID</translate></label>
              <copy-input :value="application.client_id" />
            </div>
            <div class="field">
              <label><translate translate-context="Content/Applications/Label">Application secret</translate></label>
              <copy-input :value="application.client_secret" />
            </div>
          </div>
          <h2 class="ui header">
            <translate translate-context="Content/Applications/Title">Edit application</translate>
          </h2>
          <application-form @updated="application = $event" :app="application" />
        </template>
      </section>
    </div>
  </main>
</template>

<script>
import axios from "axios"

import ApplicationForm from "@/components/auth/ApplicationForm"

export default {
  props: ['id'],
  components: {
    ApplicationForm
  },
  data() {
    return {
      application: null,
      isLoading: false,
    }
  },
  created () {
    this.fetchApplication()
  },
  methods: {
    fetchApplication () {
      this.isLoading = true
      let self = this
      axios.get(`oauth/apps/${this.id}/`).then((response) => {
        self.isLoading = false
        self.application = response.data
      }, error => {
        self.isLoading = false
        self.errors = error.backendErrors
      })
    },
  },
  computed: {
    labels() {
      return {
        title: this.$pgettext('Content/Applications/Title', "Edit application")
      }
    },
  }
}
</script>
