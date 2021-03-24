<template>
  <v-container fluid pa-0>
    <div class="col-md-6 offset-md-3">
        <v-card>
            <h1 class="pb-6 text-center">Page Visits</h1>
            <line-chart :chart-data="pageVisitCollection" :styles="myStyles"></line-chart>
        </v-card>
        <br/>
        <v-card>
            <h1 class="pb-6 text-center">Average User Session (minutes) Per Page</h1>
            <line-chart :chart-data="userSessionCollection" :styles="myStyles"></line-chart>
        </v-card>
        <br/>
        <v-card>
            <h1 class="pb-6 text-center">UI Interactions</h1>
            <line-chart :chart-data="uiClickCollection" :styles="myStyles"></line-chart>
        </v-card>        
    </div>
  </v-container>
</template>

<script>
import dbHelper, { db } from '../db'
import LineChart from '@/components/app/LineChart.js'
import 'firebase/firestore'
import sessionTracking from '@/mixins/sessionTracking'
import moment from 'moment'


export default {
    name: 'Analytics',
    components: {
      LineChart
    },
    data:() => ({        
        metric: [],
        usersession: [],
        pageVisitCollection: {},
        userSessionCollection: {},
        uiClickCollection: {}
    }),
    firestore: {
        metric: db.collection('metric'),
        usersession: db.collection('usersession')
    },
    created() {
        dbHelper.logMetric(this.$options.name)
    },
    watch: {
        metric (newMetric) {
            
            let dataSets = this.extractMetrics(newMetric)
            
            this.pageVisitCollection = {     
                datasets: [
                    {
                    label: "Landing Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true, 
                    data: dataSets["LandingPage"]
                    },
                    {
                    label: "Analytics Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["Analytics"]
                    },
                    {
                    label: "Home Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["Home"]
                    },
                    {
                    label: "Login Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true, 
                    data: dataSets["Login"]
                    },
                    {
                    label: "Workspace Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["Workspace"]
                    },
                    {
                    label: "ErrorPage Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ErrorPage"]
                    }
                ]
            }

            this.uiClickCollection = {     
                datasets: [                   
                    {
                    label: "Logout Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["LogoutBtn"]
                    },
                    {
                    label: "Permission Added",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["PermissionAdded"]
                    },
                    {
                    label: "Permission Removed",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["PermissionRemoved"]
                    },
                    {
                    label: "Create Room Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["CreateRoomBtn"]
                    },
                    {
                    label: "Join Room Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomBtn"]
                    },
                    {
                    label: "Join Room Success",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomSuccess"]
                    },
                    {
                    label: "Join Room Error",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomError"]
                    },
                    {
                    label: "Signin Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["SigninBtn"]
                    },
                    {
                    label: "Signup Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["SignupBtn"]
                    },
                    {
                    label: "Component Created",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ComponentCreated"]
                    },
                    {
                    label: "Connection Created",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ConnectionCreated"]
                    }
                ]
            }
        },
        usersession (newUserSession) {
            let dataSets = this.extractUserSession(newUserSession)

            this.userSessionCollection = {     
                datasets: [
                    {
                    label: "Home",
                    fill: false,
                    tension: 0.1,
                    showLine: true, 
                    data: dataSets["Home"]
                    },
                    {
                    label: "LandingPage",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["LandingPage"]
                    },
                    {
                    label: "Login",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["Login"]
                    },{
                    label: "Workspace",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["Workspace"]
                    },{
                    label: "Analytics",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["Analytics"]
                    },{
                    label: "ErrorPage",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["ErrorPage"]
                    },
                ]
            }
        }
    },
    methods: {
      extractMetrics(newMetric) {
          let dataSets = {}

          newMetric.forEach(metricItem => {
                // Setup an empty array for each metric to push to
                if (!(metricItem.metric in dataSets)) {
                    dataSets[metricItem.metric] = []
                }
                dataSets[metricItem.metric].push({x: moment(metricItem.timestamp_bin), y: metricItem.counter})  
          })

          return dataSets
      },
      extractUserSession(newUserSession) {
            let dataSets = {}
            newUserSession.forEach(userSessionItem => {
                // Setup an empty array for each metric to push to
                if (!(userSessionItem.page in dataSets)) {
                    dataSets[userSessionItem.page] = {}
                }

                let page = dataSets[userSessionItem.page]
                if (!page.hasOwnProperty(userSessionItem.timestamp_bin)) {
                    page[userSessionItem.timestamp_bin] = {accumulator: 0, cnt: 0}
                } 

                page[userSessionItem.timestamp_bin] = {accumulator: page[userSessionItem.timestamp_bin].accumulator + userSessionItem.elapsed_time_total, 
                                                       cnt: page[userSessionItem.timestamp_bin].cnt + 1}
            })

            let result = {}
            for (var page in dataSets) {
                if (dataSets.hasOwnProperty(page)) {
                    // console.log(page + "->" + JSON.stringify(dataSets[page]))
                    
                    if (!( page in result)) {
                        result[page] = []
                    }

                    let timeseries = dataSets[page]
                    for (var timestamp_bin in timeseries) {
                        if (timeseries.hasOwnProperty(timestamp_bin)) {
                            // console.log(timestamp_bin + "->" + JSON.stringify(timeseries[timestamp_bin]))
                            let values = timeseries[timestamp_bin]
                            let accumulator = values.accumulator
                            let cnt = values.cnt
                            if (cnt != 0) {
                                // console.log("acc:" + accumulator + ", cnt:" + cnt + ", result:" + accumulator / cnt)
                                // Divide 60000 for conversion from millisecond to minutes (due to Date.now() for session tracking)
                                result[page].push({x: moment(timestamp_bin), y: (accumulator / cnt) / 60000})
                            }
                        }
                    }
                }
            }
          return result
      }
    },
    mixins: [sessionTracking],
    computed: {
        myStyles () {
            return {
                height: "80%",
                width: "80%",
                margin: "auto",
                position: 'relative'
            }
        }
    }
}
</script>

<style>

</style>