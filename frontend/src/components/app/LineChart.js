import { Scatter, mixins } from 'vue-chartjs'
import "chartjs-plugin-colorschemes";

const { reactiveProp } = mixins
// Technically a scatter plot, but Line charts cannot plot datapoints with varying differences in X
export default {
  extends: Scatter,
  mixins: [reactiveProp],
  props: ['chartdata'],
  data () {
    return {
        options: {
            scales: {
              xAxes: [{
                type: 'time',
                time: {
                    parser: "HH:mm",
                    unit: 'hour',
                    unitStepSize: 1,
                    displayFormats: {
                      'minute': 'HH:mm', 
                      'hour': 'HH:mm', 
                      min: '00:00',
                      max: '23:59'
                    },
                } 
              }]
            },
            plugins: {
              colorschemes: {        
                scheme: 'brewer.Paired12'     
              }        
            },
            legend: {
              position: 'bottom',
              labels: {
                  boxWidth: 20,
                  padding: 20
              }
            }
          }
    }
  },
  mounted () {
    // this.chartData is created in the mixin.
    // If you want to pass options please create a local options object
 
    this.renderChart(this.chartData, this.options)
  }
}