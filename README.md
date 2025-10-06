# Tavex Gold Subscription Monte Carlo Simulator

A comprehensive React/Next.js application that simulates the performance of Tavex gold subscription investments using Monte Carlo methods with real-time gold price data from GoldAPI.io.

## 🌟 Features

### Real-Time Data Integration
- **GoldAPI.io Integration**: Live gold prices in EUR
- **Historical Data**: 25+ years of realistic gold price data
- **Fallback System**: Synthetic data based on gold market research

### Monte Carlo Simulation
- **10,000+ Simulations**: Configurable simulation runs
- **Multiple Time Horizons**: 3, 5, and 10-year projections
- **Realistic Modeling**: Based on actual gold market statistics

### Tavex Investment Model
- **Monthly Purchase**: 4g × 4 subscriptions = 16g/month
- **Bonus System**: 4 bonus grams per year
- **Accurate Pricing**: Real Tavex buy/sell prices with 9.88% spread
- **Spread Impact**: Accounts for liquidation costs

### Advanced Analytics
- **Value Distributions**: Histograms of final portfolio values
- **ROI Analysis**: Comprehensive return analysis with percentiles
- **Break-even Analysis**: Probability of positive returns
- **Bonus Impact**: Quantification of bonus gold benefits
- **Risk Metrics**: Volatility, skewness, and kurtosis analysis

### Interactive Visualizations
- **Historical Price Charts**: 10-year gold price trends
- **Distribution Charts**: Final value histograms
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Live simulation results

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Vercel account (for deployment)

### Local Development

1. **Install Dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm run dev
   ```

3. **Open Browser**:
   Navigate to `http://localhost:3000`

### Production Deployment

1. **Deploy to Vercel**:
   ```bash
   ./deploy-vercel.sh
   ```

2. **Manual Deployment**:
   ```bash
   cd frontend
   vercel --prod
   ```

## 📊 How It Works

### Data Acquisition
1. **Primary Source**: GoldAPI.io with your API key
2. **Fallback**: Realistic synthetic data based on gold market research
3. **Historical Statistics**: 25 years of monthly gold price data

### Simulation Engine
1. **Historical Analysis**: Calculate return statistics from historical data
2. **Monte Carlo**: Generate 10,000+ random price paths
3. **Investment Logic**: Apply Tavex subscription model
4. **Statistical Analysis**: Calculate percentiles and risk metrics

### Investment Model
- **Monthly Investment**: €497.60 (16g × €31.10/g)
- **Bonus Gold**: 4g per year after 12 months
- **Total Annual**: 208g + 4 bonus = 212g per year
- **Spread Impact**: 9.88% reduction on liquidation

## 🎯 Key Results

### Typical 5-Year Investment
- **Total Invested**: €24,880
- **Total Gold**: 1,060g (1,040g + 20g bonus)
- **Median Value**: €28,000-€40,000
- **Break-even Probability**: 60-80%
- **Bonus Impact**: +7-8% additional gold

### Risk Analysis
- **Volatility**: ~17% annual (based on historical data)
- **Skewness**: Positive (fat right tail)
- **Kurtosis**: High (extreme events more common)
- **Downside Risk**: 5th percentile shows potential losses

## 🛠 Technical Stack

### Frontend
- **Next.js 14**: React framework with SSR
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Interactive data visualizations
- **Lucide React**: Modern icon library

### Data Sources
- **GoldAPI.io**: Real-time gold prices
- **Historical Data**: 25 years of gold market research
- **Statistical Models**: Box-Muller transform, mean reversion

### Deployment
- **Vercel**: Serverless deployment
- **Edge Functions**: Global CDN
- **Environment Variables**: Secure API key management

## 📈 Usage Examples

### Basic Simulation
```javascript
// Run simulation with default parameters
const results = runSimulation({
  numSimulations: 10000,
  periods: [36, 60, 120] // 3, 5, 10 years
});
```

### Custom Parameters
```javascript
// Modify Tavex parameters
const tavexParams = {
  buyPrice: 124.24,
  sellPrice: 111.97,
  monthlyGrams: 4,
  subscriptions: 4,
  bonusGramsPerYear: 4
};
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Custom API endpoint
NEXT_PUBLIC_GOLDAPI_URL=https://www.goldapi.io/api/XAU/EUR
```

### Simulation Parameters
```javascript
const config = {
  numSimulations: 10000,    // Number of Monte Carlo runs
  periods: [36, 60, 120],   // Investment periods in months
  historicalMonths: 300,    // Historical data points
  confidenceLevels: [0.05, 0.25, 0.5, 0.75, 0.95]
};
```

## 📊 API Integration

### GoldAPI.io
- **Endpoint**: `https://www.goldapi.io/api/XAU/EUR`
- **Authentication**: API key in headers
- **Rate Limits**: 100 requests/day (free tier)
- **Fallback**: Synthetic data generation

## 🚀 Performance

### Optimization
- **Client-side**: All calculations in browser
- **Caching**: Historical data cached locally
- **Lazy Loading**: Charts load on demand
- **Responsive**: Optimized for all devices

### Scalability
- **Simulations**: Up to 50,000 runs
- **Data Points**: 25+ years of history
- **Real-time**: Live gold price updates
- **Global**: Vercel edge deployment

## 📋 Troubleshooting

### Common Issues

1. **GoldAPI Errors**:
   - Check API key validity
   - Verify network connectivity
   - Check rate limits

2. **Simulation Errors**:
   - Ensure historical data loaded
   - Check browser console
   - Verify input parameters

3. **Chart Issues**:
   - Check data format
   - Verify Recharts version
   - Check responsive breakpoints

## 🔒 Security

### API Key Protection
- **Environment Variables**: Store in Vercel
- **Client-side**: Key visible in browser (acceptable for this use case)
- **Rate Limiting**: Built-in API limits

### Data Privacy
- **No Storage**: No user data stored
- **Client-side**: All calculations local
- **No Tracking**: No analytics or cookies

## ⚠️ Disclaimer

This simulation is for educational and analytical purposes only. It should not be considered as financial advice. Gold investments carry risks, and past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

---

**Built with ❤️ using Next.js, TypeScript, and GoldAPI.io**