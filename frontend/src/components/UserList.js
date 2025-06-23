import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import {
  Container,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Typography,
  Box,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { logout, isAdmin } = useAuth();
  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/users', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUsers(response.data);
    } catch (err) {
      if (err.response?.status === 401) {
        logout();
        navigate('/login');
      }
      setError(err.response?.data?.message || 'An error occurred');
    }
  };

  const handleDelete = async (userId) => {
    try {
      await axios.delete(`http://localhost:8000/api/users/${userId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchUsers();
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <Container>
      <Box sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h4" component="h1">
          Users List
        </Typography>
        <Button variant="contained" color="secondary" onClick={handleLogout}>
          Logout
        </Button>
      </Box>
      
      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Username</TableCell>
              {isAdmin() && <TableCell>Email</TableCell>}
              <TableCell>Created At</TableCell>
              {isAdmin() && <TableCell>Actions</TableCell>}
            </TableRow>
          </TableHead>
          <TableBody>
            {users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.username}</TableCell>
                {isAdmin() && <TableCell>{user.email}</TableCell>}
                <TableCell>
                  {new Date(user.created_at).toLocaleDateString()}
                </TableCell>
                {isAdmin() && (
                  <TableCell>
                    <Button
                      startIcon={<DeleteIcon />}
                      color="error"
                      onClick={() => handleDelete(user.id)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                )}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default UserList; 