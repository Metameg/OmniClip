const affiliateChart = (function () {
    function getLabels() {
        let labels = ['January', 'February', 'March', 'April', 'May', 'June'];

        return labels
    }

    function getChartData() {
        const labels = getLabels();

        let chartData = {
            labels: labels,
            datasets: [{
                label: 'Sales',
                backgroundColor: 'rgb(54, 162, 235)',
                borderColor: 'rgb(54, 162, 235)',
                data: [10, 20, 30, 25, 35, 45],
            }]
        };

        return chartData;
    }

    // Private Variables and Functions
    function config(salesChartEle, chartData) {

        // Configuration for the chart
        const config = {
            type: 'line',
            data: chartData,
            options: {
                responsive: true,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Month'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: '($) Earnings'
                        }
                    }
                }
            }
        };

        // Initialize the chart
        var salesChart = new Chart(
            salesChartEle,
            config
        );
    }
    return {
        configureChart: function() {
            const salesChartEle = document.getElementById('sales-chart');
            
            const chartData = getChartData();
            config(salesChartEle, chartData);
            
            
        }
    }
})();

export default affiliateChart;