import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

const SupplyChainDashboard = ({ metrics, state, costs }) => {
  return (
    <div className="w-full space-y-4">
      {/* Performance Metrics Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Key Performance Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={metrics}>
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
        </CardContent>
      </Card>

      {/* Inventory Levels */}
      <Card>
        <CardHeader>
          <CardTitle>Inventory Levels</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={state}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="supplier_inventory" name="Supplier" fill="#8884d8" />
                <Bar dataKey="manufacturer_inventory" name="Manufacturer" fill="#82ca9d" />
                <Bar dataKey="distributor_inventory" name="Distributor" fill="#ffc658" />
                <Bar dataKey="retail_inventory" name="Retail" fill="#ff8042" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>

      {/* Cost Analysis */}
      <Card>
        <CardHeader>
          <CardTitle>Cost Breakdown</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={costs}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="step" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="raw_material" name="Raw Material" stroke="#8884d8" />
                <Line type="monotone" dataKey="manufacturing" name="Manufacturing" stroke="#82ca9d" />
                <Line type="monotone" dataKey="distribution" name="Distribution" stroke="#ffc658" />
                <Line type="monotone" dataKey="holding" name="Holding" stroke="#ff8042" />
                <Line type="monotone" dataKey="backorder" name="Backorder" stroke="#ff0000" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SupplyChainDashboard;