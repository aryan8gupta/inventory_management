// Data for components
const statsData = {
    'Last 24 hour': {
      revenue: { value: '$42', change: 8 },
      customers: { value: '15', change: 12 },
      transactions: { value: '8', change: 5 },
      products: { value: '25', change: 3 },
    },
    'Last week': {
      revenue: { value: '$152', change: 16 },
      customers: { value: '80', change: -0.45 },
      transactions: { value: '37', change: 8 },
      products: { value: '120', change: 2 },
    },
    'Last month': {
      revenue: { value: '$612', change: 24 },
      customers: { value: '300', change: 15 },
      transactions: { value: '150', change: 12 },
      products: { value: '350', change: 5 },
    },
    'Last year': {
      revenue: { value: '$5,612', change: 45 },
      customers: { value: '7,513', change: 32 },
      transactions: { value: '4,637', change: 28 },
      products: { value: '1530', change: 15 },
    },
};

  
// Populate StatCard
function updateStats(range) {
    const data = statsData[range];
    if (!data) return;
    
    // Revenue
    document.getElementById('revenueValue').textContent = data.revenue.value;
    document.getElementById('revenueChange').textContent = `(${data.revenue.change}%)`;

    // Customers
    document.getElementById('customersValue').textContent = data.customers.value;
    document.getElementById('customersChange').textContent = `(${data.customers.change}%)`;

    // Transactions
    document.getElementById('transactionsValue').textContent = data.transactions.value;
    document.getElementById('transactionsChange').textContent = `(${data.transactions.change}%)`;

    // Products
    document.getElementById('productsValue').textContent = data.products.value;
    document.getElementById('productsChange').textContent = `(${data.products.change}%)`;
}


// Customer Growth
const customerGrowthData = [
    { name: "United States", percentage: 35, flag: "🇺🇸" },
    { name: "United Kingdom", percentage: 27, flag: "🇬🇧" },
];
const customerGrowthElement = document.getElementById('customerGrowth');
customerGrowthData.forEach(country => {
    const countryDiv = document.createElement('div');
    countryDiv.className = 'country-bar';
    countryDiv.innerHTML = `
    <span>${country.flag} ${country.name}</span>
    <div class="country-bar-fill" style="width: ${country.percentage}%"></div>
    <span>${country.percentage}%</span>
    `;
    customerGrowthElement.appendChild(countryDiv);
});

// Top Transactions
const topTransactionsData = [
    { customer: "Jenny Wilson", item: "Leather case bag & wallet", date: "12 Jan", purchase: "$2,548", status: "live order" },
    { customer: "John Doe", item: "Simple Tote Bag", date: "3 Jan", purchase: "$548", status: "completed" },
];
const topTransactionsElement = document.getElementById('topTransactions');
topTransactionsData.forEach(transaction => {
    const transactionDiv = document.createElement('div');
    transactionDiv.className = 'transaction-card';
    transactionDiv.innerHTML = `
    <div class="transaction-user">
        <img src="https://randomuser.me/api/portraits/men/1.jpg" alt="${transaction.customer}" />
        <div class="transaction-details">
        <p>${transaction.customer}</p>
        <p>${transaction.item}</p>
        </div>
    </div>
    <div>
        <p>${transaction.purchase}</p>
        <p>${transaction.date}</p>
        <span class="transaction-status">${transaction.status}</span>
    </div>
    `;
    topTransactionsElement.appendChild(transactionDiv);
});

// Top Products
const topProductsData = [
    { name: "Denim Jacket with White Feathers", image: "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?auto=format&fit=crop&w=200&h=200", sales: "240+" },
    { name: "Black Leather Jacket", image: "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=200&h=200", sales: "180+" },
];
const topProductsElement = document.getElementById('topProducts');
topProductsData.forEach(product => {
    const productCard = document.createElement('div');
    productCard.className = 'product-card';
    productCard.innerHTML = `
    <img src="${product.image}" alt="${product.name}" />
    <div class="product-overlay">
        <div class="product-info">
        <h4>${product.name}</h4>
        <p>Sales: ${product.sales}</p>
        </div>
    </div>
    `;
    topProductsElement.appendChild(productCard);
});


// Revenue Chart (Simple Bar Chart Example)

const revenueChartData = {
    'Last 24 hour': [
    { name: '12 AM', revenue: 400, ecommerce: 240 },
    { name: '4 AM', revenue: 300, ecommerce: 139 },
    { name: '8 AM', revenue: 500, ecommerce: 380 },
    { name: '12 PM', revenue: 280, ecommerce: 190 },
    { name: '4 PM', revenue: 590, ecommerce: 390 },
    { name: '8 PM', revenue: 350, ecommerce: 300 },
    { name: 'Now', revenue: 400, ecommerce: 380 },
    ],
    'Last week': [
    { name: 'Sun', revenue: 400, ecommerce: 240 },
    { name: 'Mon', revenue: 300, ecommerce: 139 },
    { name: 'Tue', revenue: 500, ecommerce: 380 },
    { name: 'Wed', revenue: 280, ecommerce: 190 },
    { name: 'Thu', revenue: 590, ecommerce: 390 },
    { name: 'Fri', revenue: 350, ecommerce: 300 },
    { name: 'Sat', revenue: 400, ecommerce: 380 },
    ],
    'Last month': [
    { name: 'Week 1', revenue: 1500, ecommerce: 1000 },
    { name: 'Week 2', revenue: 2000, ecommerce: 1500 },
    { name: 'Week 3', revenue: 1800, ecommerce: 1200 },
    { name: 'Week 4', revenue: 2400, ecommerce: 1800 },
    ],
    'Last year': [
    { name: 'Jan', revenue: 4000, ecommerce: 2400 },
    { name: 'Mar', revenue: 3000, ecommerce: 1398 },
    { name: 'May', revenue: 5000, ecommerce: 3800 },
    { name: 'Jul', revenue: 2800, ecommerce: 1908 },
    { name: 'Sep', revenue: 5900, ecommerce: 3800 },
    { name: 'Nov', revenue: 3500, ecommerce: 3000 },
    { name: 'Dec', revenue: 4000, ecommerce: 3800 },
    ]
};

function renderRevenueChart(timeRange) {
    const ctx = document.getElementById('revenueChartCanvas').getContext('2d');
    const data = revenueChartData[timeRange];

    if (!data) return;

    document.getElementById("chart-period").textContent = `${timeRange} revenue growth with in percentage`;

    if (window.revenueChartInstance) window.revenueChartInstance.destroy();

    window.revenueChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: data.map(d => d.name),
        datasets: [
        {
            label: 'Revenue',
            data: data.map(d => d.revenue),
            backgroundColor: '#3B82F6',
            borderRadius: 4
        },
        {
            label: 'Ecommerce',
            data: data.map(d => d.ecommerce),
            backgroundColor: '#93C5FD',
            borderRadius: 4
        }
        ]
    },
    options: {
        responsive: true,
        scales: {
        x: { grid: { display: false } },
        y: { grid: { display: true } }
        },
        plugins: {
        tooltip: {
            backgroundColor: '#fff',
            titleColor: '#000',
            bodyColor: '#000',
            borderColor: '#ddd',
            borderWidth: 1,
            cornerRadius: 8
        },
        legend: { display: false }
        }
    }
    });
}
// Add event listeners to time range buttons
document.querySelectorAll('.time-button').forEach(button => {
    button.addEventListener('click', () => {
    document.querySelectorAll('.time-button').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    renderRevenueChart(button.dataset.range);
    updateStats(button.dataset.range);
    });
});

renderRevenueChart('Last 24 hour'); // Default
updateStats("Last 24 hour");
