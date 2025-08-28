import { useState } from 'react';
import EmployeeTable from '../components/EmployeeTable';

const API_BASE = "http://127.0.0.1:8000";

export default function SearchPage() {
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
            const url = `${API_BASE}/search/all?keyword=${encodeURIComponent(keyword.trim())}`;
            const res = await fetch(url);
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
    <div>
        <h1>Nest Database Search</h1>

        <form onSubmit={handleSearch}>
            <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="What are you looking for?"
            />
            <button type="submit">Search</button>
            <button type="button" onClick={handleClear}>Clear</button>
        </form>

        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}

        {!loading && !error && searched && (
            <EmployeeTable employees={employees} />
        )}
    </div>
);

}
