import { useState } from 'react';
import EmployeeTable from '../components/EmployeeTable';
import "../styles.css";
import nestImage from "../components/NEST-Horizontal-Logo-01-1030x321.png";

const API_BASE = "http://localhost:8000";

export default function SearchPage({ password}) {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [keyword, setKeyword] = useState("");
    const [searched, setSearched] = useState(false);
    const [showDebug, setShowDebug] = useState(false);

    const handleSearch = async (e) => {
        if (e) e.preventDefault();
        if (!keyword.trim()) return;

        setLoading(true);
        setError(null);
        setSearched(true);
    
        try {
            const url = `${API_BASE}/search/1.0?keyword=${encodeURIComponent(keyword.trim())}`;
            const res = await fetch(url, {
                headers: {
                    Authorization: "Basic " + btoa(`user:${password}`),
                },
            });
            if (!res.ok) throw new Error(`Request failed ${res.status}`);
            
            const data = await res.json();
            setEmployees(Array.isArray(data?.employees) ? data.employees : []);  
        } catch (err) {
            console.error(err);
            setError(err.message || "Search failed");
            setEmployees([]);
        } finally {
            setLoading(false);
        }
};

const handleClear = () => {
    setKeyword("");
    setEmployees([]);
    setError(null);
    setSearched(false);
    setShowDebug(false);
};

return (
    <div className="search-container">
        <img src={nestImage} alt="Nest Logo" className="nest-logo"/>
        <div className="search-box">
            <h1>Nest Database Search</h1>
            <form onSubmit={handleSearch} className="search-form">
                <input
                    type="text"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    placeholder="What are you looking for?"
                />
                <button type="submit" id="search-button">Search</button>
                <button type="button" id="clear-button" onClick={handleClear}>Clear</button>
            </form>

            {loading && <p>Loading...</p>}
            {error && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && searched && (
                <EmployeeTable employees={employees} />
            )}
        </div>
    </div>
);

}
