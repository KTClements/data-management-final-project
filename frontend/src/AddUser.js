import React, { useState } from 'react';
import axios from 'axios';

function AddUser() {
    const [user, setUser] = useState({
        user_id: '',
        name: '',
        rank: '',
        unit_number: '',
        star_number: '',
        department_id: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({ ...user, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://127.0.0.1:5000/add-user', user)
            .then(response => alert(response.data.message))
            .catch(error => console.error('Error adding user:', error));
    };

    return (
        <div>
            <h2>Add New User</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="user_id" placeholder="User ID" onChange={handleChange} required />
                <input type="text" name="name" placeholder="Name" onChange={handleChange} required />
                <input type="text" name="rank" placeholder="Rank" onChange={handleChange} />
                <input type="text" name="unit_number" placeholder="Unit Number" onChange={handleChange} />
                <input type="text" name="star_number" placeholder="Star Number" onChange={handleChange} />
                <input type="text" name="department_id" placeholder="Department ID" onChange={handleChange} required />
                <button type="submit">Add User</button>
            </form>
        </div>
    );
}

export default AddUser;