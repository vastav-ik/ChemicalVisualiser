import React, { useState, useEffect } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";
import { Chart as ChartJS } from "chart.js/auto";

const Dashboard = ({ token, setToken }) => {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [rawData, setRawData] = useState([]);
  const [showData, setShowData] = useState(false);

  const getAuthHeaders = () => ({
    headers: { Authorization: `Token ${token}` },
  });

  const fetchHistory = async () => {
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/api/history/`,
        getAuthHeaders(),
      );
      setHistory(res.data);
    } catch (err) {
      console.error("Error fetching history:", err);
      if (err.response && err.response.status === 401) {
        handleLogout();
      }
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/upload/`,
        formData,
        {
          headers: {
            ...getAuthHeaders().headers,
            "Content-Type": "multipart/form-data",
          },
        },
      );
      setData(res.data);
      fetchHistory();
      fetchRawData(res.data.id);
    } catch (err) {
      alert("Upload Failed!");
      console.error(err);
      if (err.response && err.response.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  const loadAnalysis = (item) => {
    setData(item);
    fetchRawData(item.id);
  };

  const fetchRawData = async (id) => {
    try {
      const res = await axios.get(
        `${process.env.REACT_APP_API_URL}/api/analysis/${id}/data/`,
        getAuthHeaders(),
      );
      setRawData(res.data);
    } catch (err) {
      console.error("Error fetching raw data:", err);
    }
  };

  const handleLogout = () => {
    setToken("");
    localStorage.removeItem("token");
  };

  const getStats = () => data.summary || data;

  const chartData = data
    ? {
        labels: Object.keys(getStats().type_counts),
        datasets: [
          {
            label: "Equipment Count",
            data: Object.values(getStats().type_counts),
            backgroundColor: "rgba(54, 162, 235, 0.6)",
          },
        ],
      }
    : null;

  const handleDownloadPDF = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}/api/analysis/${data.id}/pdf/`,
        {
          headers: { Authorization: `Token ${token}` },
          responseType: "blob",
        },
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `analysis_report_${data.id}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("PDF Download failed", err);
      if (err.response && err.response.status === 401) handleLogout();
    }
  };

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Dashboard</h2>
        <button onClick={handleLogout} className="btn btn-danger btn-sm">
          Logout
        </button>
      </div>

      <div className="row">
        <div className="col-md-4">
          <div className="card mb-3">
            <div className="card-header">Upload CSV</div>
            <div className="card-body">
              <input
                type="file"
                className="form-control mb-2"
                onChange={(e) => setFile(e.target.files[0])}
              />
              <button
                onClick={handleUpload}
                className="btn btn-primary w-100"
                disabled={loading}
              >
                {loading ? "Processing..." : "Analyze"}
              </button>
            </div>
          </div>

          <div className="card">
            <div className="card-header">History (Last 5)</div>
            <ul className="list-group list-group-flush">
              {history.map((item) => (
                <li
                  key={item.id}
                  className="list-group-item list-group-item-action"
                  onClick={() => loadAnalysis(item)}
                  style={{ cursor: "pointer" }}
                >
                  <small>{new Date(item.uploaded_at).toLocaleString()}</small>
                  <br />
                  <span className="badge bg-secondary">ID: {item.id}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="col-md-8">
          {data ? (
            <>
              <div className="card mb-3">
                <div className="card-header d-flex justify-content-between">
                  <span>Results (ID: {data.id})</span>
                  <div>
                    <button
                      className="btn btn-info btn-sm me-2"
                      onClick={() => setShowData(!showData)}
                    >
                      {showData ? "Hide" : "Show"} Data
                    </button>
                    <button
                      onClick={handleDownloadPDF}
                      className="btn btn-success btn-sm"
                    >
                      PDF Report
                    </button>
                  </div>
                </div>
                <div className="card-body">
                  <div className="row text-center mb-3">
                    <div className="col">
                      <h6>Avg Pressure</h6>
                      <p>{getStats().avg_pressure} Pa</p>
                    </div>
                    <div className="col">
                      <h6>Avg Temp</h6>
                      <p>{getStats().avg_temp} °C</p>
                    </div>
                    <div className="col">
                      <h6>Total</h6>
                      <p>{getStats().total_count}</p>
                    </div>
                  </div>
                  <div style={{ height: "300px" }}>
                    <Bar
                      data={chartData}
                      options={{ maintainAspectRatio: false }}
                    />
                  </div>
                </div>
              </div>

              {showData && rawData.length > 0 && (
                <div className="card">
                  <div
                    className="card-body"
                    style={{ maxHeight: "400px", overflowY: "auto" }}
                  >
                    <h5>Raw Data</h5>
                    <table className="table table-sm table-striped">
                      <thead>
                        <tr>
                          {Object.keys(rawData[0]).map((k) => (
                            <th key={k}>{k}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {rawData.map((row, i) => (
                          <tr key={i}>
                            {Object.values(row).map((val, j) => (
                              <td key={j}>{val}</td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="alert alert-light text-center">
              Please upload a file or select a record from history.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
