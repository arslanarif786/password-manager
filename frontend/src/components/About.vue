<template>
  <div class="main-bg">
    <Navbar />

    <!-- For Desktop Web Screen -->
    <div v-if="$vuetify.display.lgAndUp" class="custom-spacing-container">
      <div class="text-white text-center font-main-title txt100">
        Password <span class="text-deep-orange font-main-title txt100">Manager</span>
      </div>
      <div class="text-white text-center mt-10 txt16">
        A password manager is an indispensable tool in today's digital age;
        <br />
        It is designed to alleviate the burden of managing and
        <br />
        <span class="text-deep-orange font-sans-serif txt32">
          securing multiple passwords
        </span>
      </div>

      <div class="d-flex justify-center custom-mt w-full">
        <img :src="fb" alt="img" class="custom-image-size mr-10"/>
        <img :src="amazon" alt="img" class="custom-image-size mx-16"/>
        <img :src="youtube" alt="img" class="custom-image-size ml-10"/>
      </div>
    </div>

    <!-- For Tablet and Mobile Screen -->
    <div
      v-else
      class="d-flex flex-column align-center"
      :class="$vuetify.display.smAndUp ? 'custom-home-tab' : 'custom-home-mob'">
      <div>
        <img :src="fingerprint" alt="img" class="custom-logo-size"/>
      </div>
      <br>
      <div class="text-white text-center font-sans-serif txt16 mb-0">
        It is designed to alleviate the burden of managing and
      </div>
      <span
        class="text-deep-orange font-sans-serif mt-0"
        :class="$vuetify.display.smAndUp ? 'txt24' : 'txt20'"
      >
        securing multiple passwords
      </span>
      <div class="d-flex flex-column">
        <img :src="fb" alt="img" class="custom-tab-mob-image-size mt-16 mb-10"/>
        <img :src="amazon" alt="img" class="custom-tab-mob-image-size mb-10"/>
        <img v-if="$vuetify.display.smAndUp" :src="youtube" alt="img" class="custom-tab-mob-image-size mb-10"/>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "../layouts/Navbar.vue"
import fb from "../assets/images/fb.png"
import amazon from "../assets/images/amazon.png"
import youtube from "../assets/images/youtube.png"
import fingerprint from "../assets/images/print.png"

export default {
  components: {
    Navbar,
  },
  setup() {
    return {
      fb,
      amazon,
      youtube,
      fingerprint
    };
  },
};
</script>

<style scoped>
:deep .v-field__field:focus-within {
  background-color: #e0e0e0 !important;
}

@media screen and (min-width: 1100px) {
  .custom-spacing-container {
    padding: 50px 150px;
  }
}

@media only screen and (min-width: 768px) and (max-width: 1100px) {
  .custom-spacing-container {
    padding: 50px 50px;
  }
}

@media screen and (max-width: 768px) {
  .custom-spacing-container {
    padding: 30px 25px;
  }
}
@media screen and (max-width: 500px) {
  .custom-spacing-container {
    padding: 30px 0;
  }
}
.v-responsive {
  max-width: 230px
}
.custom-home-tab {
  padding: 150px 50px;
}
.custom-home-mob {
  padding: 70px 50px;
}
.custom-image-size {
  height: 100px;
  width: 340px;
  border-radius: 20px;
}
.custom-tab-mob-image-size {
  height: 90px;
  width: 270px;
  border-radius: 20px;
}
.custom-logo-size {
  height: 100px;
  width: 100px;
  border-radius: 6px;
}
.custom-mt {
  margin-top: 220px;
}
</style>
