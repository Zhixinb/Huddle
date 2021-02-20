<template>
  
  <div>
    <v-app-bar app color="white" height="100">
        <v-avatar class="mr-3" color="grey lighten-5"  size="70" >
            <v-img contain max-height="70%" :src="logo"></v-img>
        </v-avatar>   
        <v-toolbar-title class="font-weight-black headline">HUDDLE</v-toolbar-title>
        <v-spacer />
        <v-btn color="primary" @click="redirectToLogin">Get Started</v-btn>   
    </v-app-bar>

    <v-img :max-height="'calc(100vh - ' + getTop() + 'px)'"
    src="https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1951&q=80"
    >
    <v-theme-provider dark>
        <v-container fill-height>
        <v-row align="center" class="white--text mx-auto" justify="center">
            <v-col class="white--text text-center" cols="12" tag="h1">
                <span :class="[$vuetify.breakpoint.smAndDown ? 'display-1' : 'display-2']" class="font-weight-light">
                    WELCOME TO
                </span>
                <br>
                <span :class="[$vuetify.breakpoint.smAndDown ? 'display-3': 'display-4']" class="font-weight-black" >
                    HUDDLE
                </span>
            </v-col>
            <v-btn  class="align-self-end" fab outlined @click="$vuetify.goTo('#features')">
                <v-icon>mdi-chevron-double-down</v-icon>
            </v-btn>
        </v-row>
        </v-container>
    </v-theme-provider>
    </v-img>

    <section id="features" class="grey lighten-3" >
    <div class="py-12"></div>

    <v-container class="text-center">
        <h2 class="display-2 font-weight-bold mb-3">HUDDLE FEATURES</h2>

        <v-responsive class="mx-auto mb-12" width="56">
            <v-divider class="mb-1"></v-divider>
            <v-divider></v-divider>
        </v-responsive>

        <v-row>
            <v-col v-for="({ icon, title, text }, i) in features" :key="i" cols="12" md="4">
                <v-card class="py-12 px-4" color="grey lighten-5" flat >
                <v-theme-provider dark>
                    <div>
                    <v-avatar color="primary" size="88">
                        <v-icon large v-text="icon"></v-icon>
                    </v-avatar>
                    </div>
                </v-theme-provider>

                <v-card-title class="justify-center font-weight-black text-uppercase" v-text="title"></v-card-title>

                <v-card-text class="subtitle-1" v-text="text">
                </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
    </section>
</div>
</template>

<script>
import logo from '../assets/logo-256x256.png'

export default {
    name: 'LandingPage',
    data() {
        return {
            logo: logo,
            features: [
            {
                icon: 'mdi-account-group-outline',
                title: 'Vibrant Community',
                text: 'Virtual presentation platform intended to create a more engaging environment for hosts and participants than existing platforms such as Powerpoint and Zoom.',
            },
            {
                icon: 'mdi-update',
                title: 'Endless Widgets',
                text: 'Provides interactive widgets and workspaces to allow hosts to seamlessly transition between lecturing and conducting activities with participants.',
            },
            {
                icon: 'mdi-shield-outline',
                title: 'Easy to Use',
                text: 'Gives users the ability to create simple games or complex models without needing prior coding experience, using an intuitive user interface.',
            }
            ]
        }
    },
    methods: {
        redirectToLogin() {
            this.$router.push({ name: 'Login'})
        },
        getTop() {
            return this.$vuetify.application.top
        }
    } 
}
</script>

<style>

</style>