import React, { useState, useEffect } from 'react';
import axios from 'axios';

function MDTList() {
    const [mdts, setMdts] = useState([]); // State to hold MDT data
    const [token, setToken] = useState(null); // JWT token for authentication

    // Fetch token for authentication (mocked for demonstration)
    useEffect(() => {
        axios.post('http://127.0.0.1:5000/login', { username: 'admin' })
            .then(response => {
                setToken(response.data.access_token);
            })
            .catch(error => console.error('Error fetching token:', error));
    }, []);

    useEffect(() => {
        if (token) {
            axios.get('http://127.0.0.1:5000/load-mdt-data', {
                headers: { Authorization: `Bearer ${token}` }
            })
            .then(response => {
                console.log(response.data);
                setMdts(response.data);
            })
            .catch(error => {
                console.error('Error fetching MDT data:', error);
                alert('Failed to fetch MDT data. Please try again later.');
            });
        }
    }, [token]);    

    const handleUpdate = () => {
        // Update the Returned tab
        axios.post('http://127.0.0.1:5000/update-returned-tab', mdts, {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then(() => {
                alert('Returned tab updated successfully!');
            })
            .catch(error => {
                console.error('Error updating Returned tab:', error);
                alert('Failed to update Returned tab.');
            });
    };

    const handleGenerateReport = () => {
        // Generate a CSV report for the Returned tab
        axios.get('http://127.0.0.1:5000/generate-report', {
            headers: { Authorization: `Bearer ${token}` }
        })
            .then(response => {
                alert(`Report generated successfully! Path: ${response.data.path}`);
            })
            .catch(error => {
                console.error('Error generating report:', error);
                alert('Failed to generate report.');
            });
    };

    return (
        <div>
            <h2>MDT Inventory</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Unit</th>
                        <th>Star #</th>
                        <th>PC Serial</th>
                        <th>PC Model</th>
                        <th>Aircard IP</th>
                        <th>PC Name</th>
                        <th>Term ID</th>
                        <th>Status</th> {/* Added Status column */}
                    </tr>
                </thead>
                <tbody>
                    {mdts.map((mdt, index) => (
                        <tr key={index}>
                            <td>{mdt.name}</td>
                            <td>{mdt.unit}</td>
                            <td>{mdt.star_number}</td>
                            <td>{mdt.pc_serial}</td>
                            <td>{mdt.pc_model}</td>
                            <td>{mdt.aircard_ip}</td>
                            <td>{mdt.pc_name}</td>
                            <td>{mdt.term_id}</td>
                            <td>{mdt.status || 'Active'}</td> {/* Default to Active if status is not provided */}
                        </tr>
                    ))}
                </tbody>
            </table>
            <div>
                <button onClick={handleUpdate} disabled={!token}>Update Returned Tab</button>
                <button onClick={handleGenerateReport} disabled={!token}>Generate Report</button>
            </div>
        </div>
    );
}

export default MDTList;