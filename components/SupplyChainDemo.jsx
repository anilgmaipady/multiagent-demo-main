import React, { useState, useEffect } from 'react';
import SupplyChainDashboard from './SupplyChainDashboard';

const SupplyChainDemo = () => {
  const [simulationData, setSimulationData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // In a real application, this would be an API call to your Python backend
        // For demo purposes, we'll generate sample data
        const sampleData = generateSampleData();
        setSimulationData(sampleData);
        setIsLoading(false);
      } catch (err) {
        setError('Failed to fetch simulation data');
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  const generateSampleData = () => {
    // Generate 5 time steps of sample data
    return Array.from({ length: 5 }, (_, step) => ({
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
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading simulation data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl text-red-500">{error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6">
        <h1 className="text-3xl font-bold mb-8 px-4">Supply Chain Simulation Dashboard</h1>
        <SupplyChainDashboard data={simulationData} />
      </div>
    </div>
  );
};

export default SupplyChainDemo;