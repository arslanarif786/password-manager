/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#ff5722',
          secondary: '#5CBBF6',
        },
      },
    },
  },
  // breakpoint: {
  //   thresholds: {
  //     xs: 650,
  //     sm: 1297,
  //     md: 1383,
  //     lg: 1457,
  //     xl: 1920
  //   },
  // },
})
