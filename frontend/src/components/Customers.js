import React, { useState, useEffect } from 'react';

const Customers = () => {
    const [customers, setCustomers] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [itemsPerPage] = useState(10);
    const [newCustomer, setNewCustomer] = useState({
        company_name: '',
        industry: '',
        address: '',
        email: '',
        phone_number: '',
        lead_status: 'New',
    });

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        const response = await fetch('http://localhost:8000/customer/');
        const data = await response.json();
        setCustomers(data);
    };

    const handleCreateCustomer = async () => {
        const response = await fetch('http://localhost:8000/customer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newCustomer),
        });
        if (response.ok) {
            fetchCustomers();
            setNewCustomer({
                company_name: '',
                industry: '',
                address: '',
                email: '',
                phone_number: '',
                lead_status: 'New',
            });
        }
    };

    const handleDeleteCustomer = async (id) => {
        await fetch(`http://localhost:8000/customer/${id}`, {
            method: 'DELETE',
        });
        fetchCustomers();
    };

    const handleUpdateCustomer = async (id) => {
        // You'd implement a similar form and flow as the create handler.
        // For simplicity, this is left as an exercise.
    };

    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = customers.slice(indexOfFirstItem, indexOfLastItem);

    const totalPages = Math.ceil(customers.length / itemsPerPage);

    return (
        <div>
            <h1>Customers</h1>
            <table>
                <thead>
                    <tr>
                        <th>Company Name</th>
                        <th>Industry</th>
                        <th>Address</th>
                        <th>Email</th>
                        <th>Phone Number</th>
                        <th>Lead Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {currentItems.map((customer) => (
                        <tr key={customer.id}>
                            <td>{customer.company_name}</td>
                            <td>{customer.industry}</td>
                            <td>{customer.address}</td>
                            <td>{customer.email}</td>
                            <td>{customer.phone_number}</td>
                            <td>{customer.lead_status}</td>
                            <td>
                                <button onClick={() => handleUpdateCustomer(customer.id)}>Edit</button>
                                <button onClick={() => handleDeleteCustomer(customer.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div>
                <button
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(currentPage - 1)}
                >
                    Previous
                </button>
                <button
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(currentPage + 1)}
                >
                    Next
                </button>
            </div>

            <h2>Add New Customer</h2>
            <form onSubmit={(e) => e.preventDefault()}>
                <input
                    type="text"
                    value={newCustomer.company_name}
                    placeholder="Company Name"
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, company_name: e.target.value })
                    }
                />
                <input
                    type="text"
                    value={newCustomer.industry}
                    placeholder="Industry"
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, industry: e.target.value })
                    }
                />
                <input
                    type="text"
                    value={newCustomer.address}
                    placeholder="Address"
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, address: e.target.value })
                    }
                />
                <input
                    type="email"
                    value={newCustomer.email}
                    placeholder="Email"
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, email: e.target.value })
                    }
                />
                <input
                    type="text"
                    value={newCustomer.phone_number}
                    placeholder="Phone Number"
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, phone_number: e.target.value })
                    }
                />
                <select
                    value={newCustomer.lead_status}
                    onChange={(e) =>
                        setNewCustomer({ ...newCustomer, lead_status: e.target.value })
                    }
                >
                    <option value="New">New</option>
                    <option value="Connected">Connected</option>
                    <option value="Proposal">Proposal</option>
                    <option value="Client">Client</option>
                    <option value="Lost">Lost</option>
                </select>
                <button onClick={handleCreateCustomer}>Add Customer</button>
            </form>
        </div>
    );
};

export default Customers;
