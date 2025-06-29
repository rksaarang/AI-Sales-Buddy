// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard script loaded');
    
    // Fetch analytics data
    fetch('/api/analytics')
        .then(response => {
            console.log('API response status:', response.status);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Received analytics data:', data);
            // Check if we have data
            if (!data) {
                console.error('No data received:', data);
                showErrorMessage('No data received from server');
                return;
            }

            // Handle empty data case
            if (!data.sector_counts?.length && !data.region_counts?.length) {
                console.log('No notes found, showing empty charts');
                
                // Initialize empty Sector Chart
                const sectorCtx = document.getElementById('sectorChart');
                if (sectorCtx) {
                    console.log('Initializing empty sector chart');
                    const sectorChart = new Chart(sectorCtx, {
                        type: 'bar',
                        data: {
                            labels: ['No Data'],
                            datasets: [{
                                label: 'Sector Distribution',
                                data: [0],
                                backgroundColor: ['#CCCCCC'],
                                borderColor: ['#CCCCCC'],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'top',
                                },
                                title: {
                                    display: true,
                                    text: 'Sector Distribution'
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }

                // Initialize empty Region Chart
                const regionCtx = document.getElementById('regionChart');
                if (regionCtx) {
                    console.log('Initializing empty region chart');
                    const regionChart = new Chart(regionCtx, {
                        type: 'bar',
                        data: {
                            labels: ['No Data'],
                            datasets: [{
                                label: 'Region Distribution',
                                data: [0],
                                backgroundColor: ['#CCCCCC'],
                                borderColor: ['#CCCCCC'],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'top',
                                },
                                title: {
                                    display: true,
                                    text: 'Region Distribution'
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
            } else {
                console.log('Initializing charts with data:', data);
                // Initialize Sector Chart with data
                const sectorCtx = document.getElementById('sectorChart');
                if (sectorCtx) {
                    console.log('Sector data:', data.sector_counts);
                    const sectorChart = new Chart(sectorCtx, {
                        type: 'bar',
                        data: {
                            labels: data.sector_counts.map(item => item.sector),
                            datasets: [{
                                label: 'Sector Distribution',
                                data: data.sector_counts.map(item => item.count),
                                backgroundColor: [
                                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                                ],
                                borderColor: [
                                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'top',
                                },
                                title: {
                                    display: true,
                                    text: 'Sector Distribution'
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }

                // Initialize Region Chart with data
                const regionCtx = document.getElementById('regionChart');
                if (regionCtx) {
                    console.log('Region data:', data.region_counts);
                    const regionChart = new Chart(regionCtx, {
                        type: 'bar',
                        data: {
                            labels: data.region_counts.map(item => item.region),
                            datasets: [{
                                label: 'Region Distribution',
                                data: data.region_counts.map(item => item.count),
                                backgroundColor: [
                                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                                ],
                                borderColor: [
                                    '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                                ],
                                borderWidth: 1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: {
                                    position: 'top',
                                },
                                title: {
                                    display: true,
                                    text: 'Region Distribution'
                                }
                            },
                            scales: {
                                y: {
                                    beginAtZero: true
                                }
                            }
                        }
                    });
                }
            }
        })
        .catch(error => {
            console.error('Error loading analytics:', error);
            showErrorMessage('Error loading charts. Please try refreshing the page.');
        });
});

// Helper function to show error messages
function showErrorMessage(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'alert alert-danger mt-3';
    errorDiv.textContent = message;
    document.querySelector('.row').appendChild(errorDiv);
}
