<template>
  <v-app>
    <v-navigation-drawer
      fixed
      v-model="drawer"
      app
    >
      <v-list>
        <v-list-tile
          v-for="(page, index) in pages"
          :key="index"
          @click="linkto(page.link)"
        >
          <v-list-tile-content>
            <v-list-tile-title>{{ page.title }}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import Data from './data';
import { UtilMixin } from './util';

export default Vue.extend({
  mixins: [UtilMixin],
  data: function () {
    return {
      drawer: false,
      pages: Data.pages
    }
  }
});
</script>