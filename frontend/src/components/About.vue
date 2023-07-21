<template>
  <div class="main-bg">
    <Navbar />
    <div class="custom-spacing-container">
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
  </div>
</template>

<script>
import Navbar from "../layouts/Navbar.vue"
import fb from "../assets/images/fb.png"
import amazon from "../assets/images/amazon.png"
import youtube from "../assets/images/youtube.png"

export default {
  components: {
    Navbar,
  },
  setup() {
    return {
      fb,
      amazon,
      youtube
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
.custom-image-size {
  height: 100px;
  width: 340px;
  border-radius: 20px;
}
.custom-mt {
  margin-top: 220px;
}
</style>
