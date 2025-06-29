import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  LinearProgress,
} from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import axios from 'axios';

export function Dashboard({ user }) {
  const [analytics, setAnalytics] = useState({
    total_clients: 0,
    total_visits: 0,
    total_proposals: 0,
    total_sales: 0,
  });

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/analytics');
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const chartData = [
    { name: 'Clients', value: analytics.total_clients },
    { name: 'Visits', value: analytics.total_visits },
    { name: 'Proposals', value: analytics.total_proposals },
  ];

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Sales Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary">
                Total Clients
              </Typography>
              <Typography variant="h3" component="div">
                {analytics.total_clients}
              </Typography>
              <LinearProgress variant="determinate" value={(analytics.total_clients / 100) * 100} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary">
                Total Visits
              </Typography>
              <Typography variant="h3" component="div">
                {analytics.total_visits}
              </Typography>
              <LinearProgress variant="determinate" value={(analytics.total_visits / 100) * 100} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary">
                Total Proposals
              </Typography>
              <Typography variant="h3" component="div">
                {analytics.total_proposals}
              </Typography>
              <LinearProgress variant="determinate" value={(analytics.total_proposals / 100) * 100} />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="text.secondary">
                Total Sales
              </Typography>
              <Typography variant="h3" component="div">
                ${analytics.total_sales}
              </Typography>
              <LinearProgress variant="determinate" value={(analytics.total_sales / 100000) * 100} />
            </CardContent>
          </Card>
        </Grid>

        {/* Bar Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Activity Overview
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#1976d2" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
