<template>
    <div class="main-bg d-flex custom-flex align-center">
      <div
        v-if="!$vuetify.display.lg"
        class="text-white custom-main-heading"
        :class="!$vuetify.display.lg ? 'mt-10' : ''"
      >
        <h1
          class="font-avenir"
          :class="$vuetify.display.sm || $vuetify.display.md ? 'txt36' : 'txt32'"
        >
          Password
          <span
            class="text-deep-orange font-avenir"
            :class="
              $vuetify.display.sm || $vuetify.display.md ? 'txt36' : 'txt32'
            "
          >
            Manager
          </span>
        </h1>
      </div>
      <div>
      <v-sheet
        :width="$vuetify.display.lg ? '450' : '360'"
        class="custom-spacing custom-radius px-15 py-12"
        :class="!$vuetify.display.lg ? 'mt-10' : ''"
      >
        <h2>Create Account</h2>
        <div class="mt-2 mb-4 txt14">Register with a new account</div>
        <v-form ref="myForm" fast-fail @submit.prevent>
          <div v-for="(item, index) in inputList" :key="index">
            <div v-if="index <= 2">
              <v-text-field
                v-model="item.model"
                :label="item.label"
                :placeholder="item.placeholder"
                :rules="item.rules"
                :type="item.type"
                variant="solo"
              >
              </v-text-field>
            </div>
          </div>
          <div v-for="(item, index) in inputList" :key="index">
            <div v-if="index > 2">
              <v-text-field
                v-model="item.model"
                :label="item.label"
                :placeholder="item.placeholder"
                :rules="item.rules"
                :type="item.visible ? 'text' : item.type"
                :append-inner-icon="item.visible ? 'mdi-eye-off' : 'mdi-eye'"
                @click:append-inner="item.visible = !item.visible"
                variant="solo"
              >
              </v-text-field>
            </div>
          </div>
  
          <v-btn
            type="submit"
            @click="signupRequest"
            block
            :loading="loader"
            color="deep-orange"
            class="mt-2 text-capitalize"
            >Signup</v-btn
          >
        </v-form>
        <router-link :to="'login'" class="text-decoration-none primary-color">
          <div class="mt-3 mb-4 txt14 text-right">Back to Login</div>
        </router-link>
      </v-sheet>
      <div class="text-center">
      <v-btn
            v-if="!$vuetify.display.lg"
            @click="$router.push({path: '/'})"
            variant="outlined"
            color="deep-orange"
            class="mt-8 text-capitalize custom-360"
            >Go to Home</v-btn
          >
          </div>
      </div>
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
        <br>
        <div class="txt16 custom-width-title">
          Lets create an account in our system to register yourself.
        </div>
        <v-btn
            @click="$router.push({path: '/'})"
            block
            variant="outlined"
            color="deep-orange"
            class="mt-5 text-capitalize"
            >Go to Home</v-btn
          >
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue"
  import rules from "../constants/validation-rules.js"

  import { useRoute } from "vue-router"
  import { useRouter } from "vue-router"
  import useToast from '@/plugins/useToast.js'
  import axios from "axios"
  export default {
    setup() {
      const loader = ref(false)
      const myForm = ref('')
      const route = useRoute()
      const router = useRouter()
      const inputList = ref([
        {
          name: "firstName",
          label: "First Name",
          placeholder: "Enter your first name here",
          type: "text",
          class: "",
          cols: 12,
          col_md: 12,
          model: "",
          rules: [rules.firstNameRequired, rules.name_max_length],
        },
        {
          name: "lastName",
          label: "Last Name",
          placeholder: "Enter your last name here",
          type: "text",
          class: "",
          cols: 12,
          col_md: 12,
          model: "",
          rules: [rules.lastNameRequired, rules.name_max_length],
        },
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
        {
          name: "confirmPassword",
          label: "Confirm Password",
          placeholder: "Enter confirm password here",
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
  
      const signupRequest = () => {
        // check validations
        if(!inputList.value[0].model) {
          useToast("First name is required", "error")
          return
        }
        if(!inputList.value[1].model) {
          useToast("Last name is required", "error")
          return
        }
        if(!inputList.value[2].model) {
          useToast("Email is required", "error")
          return
        }
        if(!inputList.value[3].model) {
          useToast("Password is required", "error")
          return
        }
        if(inputList.value[3].model !== inputList.value[4].model) {
          useToast("Password did not match", "error")
          return
        }
        
        // button loader is ON
        loader.value = true
        
        const payload = {
          name: inputList.value[0].model + " " + inputList.value[1].model,
          email: inputList.value[2].model,
          password: inputList.value[3].model
        }
        console.log('ready signup payload ==============', payload)

        const appBaseURL = import.meta.env.VITE_API_URL

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: `${appBaseURL}create_account`,
          headers: { 
            'Content-Type': 'application/json'
          },
          data : payload
        };

        axios.request(config)
        .then((res) => {
          if(res.data.message == 'Account created successfully')
            {
              // show success message in snackbar
              useToast(res.data.message, "success")
              // route to login page
              router.push({path: "/login"});
            }
            else {
              console.log(res);
              useToast(res.data.message, "error");
            }
          })
        .catch((error) => {
            // show error message
            useToast(error.messae, "error")
          })
        .finally(() => {
            loader.value = false
          })
      }
  
      return {
        loader,
        myForm,
        route,
        router,
        inputList,
        signupRequest
      }
    },
  
    methods: {},
  }
  </script>
  
  <style scoped>
  :deep .v-field__field:focus-within {
    background-color: #e0e0e0 !important;
  }
  .custom-360 {
    width: 240px;
  }
  </style>
  