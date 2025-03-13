import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  Legend, 
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const COLORS = ['#8884d8', '#82ca9d', '#ffc658', '#ff8042', '#0088FE'];

const SupplyChainDashboard = ({ data }) => {
  // Transform data for different visualizations
  const getPerformanceData = () => data.map((d, index) => ({
    step: index + 1,
    fillRate: d.metrics.fill_rate,
    inventoryTurnover: d.metrics.inventory_turnover,
    backorders: d.metrics.backorders
  }));

  const getInventoryData = () => data.map((d, index) => ({
    step: index + 1,
    supplier: d.state.supplier_inventory,
    manufacturer: d.state.manufacturer_inventory,
    distributor: d.state.distributor_inventory,
    retail: d.state.retail_inventory
  }));

  const getCostData = () => data.map((d, index) => ({
    step: index + 1,
    rawMaterial: d.costs.raw_material,
    manufacturing: d.costs.manufacturing,
    distribution: d.costs.distribution,
    holding: d.costs.holding,
    backorder: d.costs.backorder
  }));

  const getLatestMetrics = () => {
    const latest = data[data.length - 1];
    return [
      { name: 'Fill Rate', value: latest.metrics.fill_rate },
      { name: 'Inventory Turnover', value: latest.metrics.inventory_turnover },
      { name: 'Backorders', value: latest.metrics.backorders },
      { name: 'Avg Inventory', value: latest.metrics.average_inventory }
    ];
  };

  return (
    <div className="w-full space-y-4 p-4">
      <h1 className="text-2xl font-bold mb-6">Supply Chain Performance Dashboard</h1>

      {/* Performance Metrics */}
      <Card>
        <CardHeader>
          <CardTitle>Key Performance Metrics Over Time</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={getPerformanceData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" label={{ value: 'Time Step', position: 'bottom' }} />
                <YAxis yAxisId="left" label={{ value: 'Fill Rate / Turnover', angle: -90, position: 'insideLeft' }} />
                <YAxis yAxisId="right" orientation="right" label={{ value: 'Backorders', angle: 90, position: 'insideRight' }} />
                <Tooltip />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="fillRate" name="Fill Rate %" stroke="#8884d8" />
                <Line yAxisId="left" type="monotone" dataKey="inventoryTurnover" name="Inventory Turnover" stroke="#82ca9d" />
                <Line yAxisId="right" type="monotone" dataKey="backorders" name="Backorders" stroke="#ff7300" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Inventory Levels */}
      <Card>
        <CardHeader>
          <CardTitle>Inventory Levels Across Supply Chain</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={getInventoryData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" label={{ value: 'Time Step', position: 'bottom' }} />
                <YAxis label={{ value: 'Inventory Units', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="supplier" name="Supplier" fill="#8884d8" stackId="a" />
                <Bar dataKey="manufacturer" name="Manufacturer" fill="#82ca9d" stackId="a" />
                <Bar dataKey="distributor" name="Distributor" fill="#ffc658" stackId="a" />
                <Bar dataKey="retail" name="Retail" fill="#ff8042" stackId="a" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Cost Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Cost Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={getCostData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" label={{ value: 'Time Step', position: 'bottom' }} />
                <YAxis label={{ value: 'Cost Units', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="rawMaterial" name="Raw Material" stroke="#8884d8" />
                <Line type="monotone" dataKey="manufacturing" name="Manufacturing" stroke="#82ca9d" />
                <Line type="monotone" dataKey="distribution" name="Distribution" stroke="#ffc658" />
                <Line type="monotone" dataKey="holding" name="Holding" stroke="#ff8042" />
                <Line type="monotone" dataKey="backorder" name="Backorder" stroke="#ff0000" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Current Metrics Summary */}
      <Card>
        <CardHeader>
          <CardTitle>Current Performance Summary</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={getLatestMetrics()}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  label
                >
                  {getLatestMetrics().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SupplyChainDashboard;