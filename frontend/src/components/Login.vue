<template>
    <div class="main-bg d-flex custom-flex align-center">
      <div
        v-if="!$vuetify.display.lg"
        class="text-white custom-main-heading"
        :class="!$vuetify.display.lg ? 'mt-10' : ''"
      >
        <h1 class="font-avenir" :class="$vuetify.display.sm || $vuetify.display.md ? 'txt36' : 'txt32'">
          Password
          <span class="text-deep-orange font-avenir" :class="$vuetify.display.sm || $vuetify.display.md ? 'txt36' : 'txt32'"> Manager </span>
        </h1>
      </div>
      <v-sheet
        :width="$vuetify.display.lg ? '450' : '340'"
        :height="$vuetify.display.lg ? '400' : '420'"
        class="custom-spacing custom-radius px-15 py-12"
        :class="!$vuetify.display.lg ? 'mt-10' : ''"
      >
        <h2>Login</h2>
        <div class="mt-2 mb-4 txt14">
          Enter your credentials to access your account
        </div>
        <v-form ref="myForm" fast-fail @submit.prevent>
          <v-text-field
            v-model="inputList[0].model"
            :label="inputList[0].label"
            :placeholder="inputList[0].placeholder"
            :rules="inputList[0].rules"
            :type="inputList[0].type"
            variant="solo"
          >
          </v-text-field>
          <v-text-field
            v-model="inputList[1].model"
            :label="inputList[1].label"
            :placeholder="inputList[1].placeholder"
            :rules="inputList[1].rules"
            :type="inputList[1].visible ? 'text' : inputList[1].type"
            :append-inner-icon="inputList[1].visible ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="inputList[1].visible = !inputList[1].visible"
            variant="solo"
          >
          </v-text-field>
          <v-btn
            type="submit"
            @click="loginRequest"
            block
            :loading="loader"
            color="deep-orange"
            class="mt-2 text-capitalize"
            >Login</v-btn
          >
        </v-form>
        <router-link :to="'signup'" class="text-decoration-none primary-color">
          <div class="mt-3 mb-4 txt14 text-center">
            Create new account
          </div>
        </router-link>
      </v-sheet>
      <div class="text-white custom-main-title">
        <h1 class="font-avenir txt60">
          Password
          <span class="text-deep-orange font-avenir txt60"> Manager </span>
        </h1>
        <div class="txt16 custom-width-title mt-5">
          A password manager is a technology that helps internet users create,
          save, manage and use passwords across different online services. Many
          online services require a username and password to create an account and
          gain access to a specific service.
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  import rules from "../constants/validation-rules.js"
  import API from "../services/API"
  import { useRoute } from "vue-router"
  export default {
    setup() {
      const loader = ref(false)
      const myForm = ref('')
      const route = useRoute()
      const inputList = ref([
        {
          name: "email",
          label: "Email",
          placeholder: "Enter your email here",
          type: "email",
          class: "",
          cols: 12,
          col_md: 12,
          model: "",
          rules: [rules.emailRequired, rules.email],
        },
        {
          name: "password",
          label: "Password",
          placeholder: "Enter your password here",
          type: "password",
          class: "mt-3",
          cols: 12,
          col_md: 12,
          visible: false,
          model: "",
          rules: [
            rules.passwordRequired,
            rules.password_length,
            rules.password_max_length,
          ],
        },
      ])
  
      const loginRequest = () => {
        // inputValidations()
        // set loader true
        const payload = {
          email: inputList.value[0].model,
          password: inputList.value[1].model
        }
        console.log('ready login payload ==============', payload)
        API.post("login", payload)
          .then(() => {
            // set local storage user keys
            // show success message while snackbar
            // route to dashboard page
          })
          .catch(() => {
            // show error message
          })
          .finally(() => {
            // set loader false
          })
      }
  
      const inputValidations = async () => {
        const { valid } = await myForm.value.validate()
        if (valid) alert('Form is valid')
      }
  
      return {
        loader,
        myForm,
        route,
        inputList,
        loginRequest
      }
    }
  }
  </script>
  
  <style scoped>
  :deep .v-field__field:focus-within {
    background-color: #e0e0e0 !important;
  }
  </style>
  