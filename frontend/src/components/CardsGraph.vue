<template>
    <div>
        <div v-if="chartData" class="graph">
            <Bar :data="chartData" :chart-options="chartOptions"  />
        </div>
        <WaitComponent v-else />
        
    </div>
    
</template>
  
<script>
import WaitComponent from '../components/Wait.vue'
import { Bar, Line} from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
    name: 'CardGraph',
    components: { Bar, WaitComponent },
    props: {
        chartData: {
            type: Object
        },
        chartOptions: {
            type: Object,
            default: () => { }
        }
    }
}
</script>

<style>

.graph{
    width: 500px;
    height: 300px;
}

</style>