import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

// Simple Card Component
const Card = ({ title, children }) => (
  <div className="bg-white rounded-lg shadow-lg p-4">
    <div className="mb-4">
      <h2 className="text-xl font-semibold">{title}</h2>
    </div>
    <div>{children}</div>
  </div>
);

// Dashboard Component
const SupplyChainDashboard = ({ data }) => {
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

  return (
    <div className="w-full space-y-4">
      {/* Performance Metrics */}
      <Card title="Key Performance Metrics">
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={getPerformanceData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="step" />
              <YAxis yAxisId="left" />
              <YAxis yAxisId="right" orientation="right" />
              <Tooltip />
              <Legend />
              <Line yAxisId="left" type="monotone" dataKey="fillRate" name="Fill Rate %" stroke="#8884d8" />
              <Line yAxisId="left" type="monotone" dataKey="inventoryTurnover" name="Inventory Turnover" stroke="#82ca9d" />
              <Line yAxisId="right" type="monotone" dataKey="backorders" name="Backorders" stroke="#ff7300" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Inventory Levels */}
      <Card title="Inventory Levels">
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={getInventoryData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="step" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="supplier" name="Supplier" fill="#8884d8" />
              <Bar dataKey="manufacturer" name="Manufacturer" fill="#82ca9d" />
              <Bar dataKey="distributor" name="Distributor" fill="#ffc658" />
              <Bar dataKey="retail" name="Retail" fill="#ff8042" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>

      {/* Cost Analysis */}
      <Card title="Cost Analysis">
        <div className="h-96">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={getCostData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="step" />
              <YAxis />
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
      </Card>
    </div>
  );
};

// Demo Component
const SupplyChainDemo = () => {
  const [simulationData, setSimulationData] = useState([]);

  useEffect(() => {
    // Generate sample data
    const sampleData = Array.from({ length: 5 }, (_, step) => ({
      metrics: {
        fill_rate: 90 + Math.random() * 10,
        inventory_turnover: 4 + Math.random(),
        backorders: Math.floor(Math.random() * 5),
        average_inventory: 100 + Math.random() * 20
      },
      state: {
        supplier_inventory: 80 + Math.random() * 40,
        manufacturer_inventory: 40 + Math.random() * 20,
        distributor_inventory: 50 + Math.random() * 20,
        retail_inventory: 30 + Math.random() * 20
      },
      costs: {
        raw_material: 1000 + Math.random() * 200,
        manufacturing: 1500 + Math.random() * 300,
        distribution: 500 + Math.random() * 100,
        holding: 200 + Math.random() * 50,
        backorder: 100 + Math.random() * 100
      }
    }));
    setSimulationData(sampleData);
  }, []);

  if (simulationData.length === 0) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-xl">Loading simulation data...</div>
      </div>
    );
  }

  return (
    <div className="p-4 bg-gray-100 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Supply Chain Simulation Dashboard</h1>
      <SupplyChainDashboard data={simulationData} />
    </div>
  );
};

export default SupplyChainDemo;